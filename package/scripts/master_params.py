#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import os

# server configurations
config = Script.get_config()

# Notebook service configs
# TODO - add port configuration
user = config['configurations']['jupyter-config']['jupyter.user']
log_dir = config['configurations']['jupyter-config']['log.dir']
pid_file = config['configurations']['jupyter-env']['pid_file']
pid_dir = '/'.join(pid_file.split('/')[0:-1])

# Spark configs
num_executors = str(config['configurations']['jupyter-config']['num.executors'])
executor_memory = str(config['configurations']['jupyter-config']['executor.memory'])

package_dir = os.path.realpath(__file__).split('/package')[0] + '/package/'
files_dir = package_dir + 'files/'
scripts_dir = package_dir + 'scripts/'
root_dir = '/home/'+user

distribution = platform.linux_distribution()[0].lower()
#TODO: add ubuntu
if distribution in ['centos', 'redhat'] :
  repo_dir = files_dir+'repos/rhel6/'
  os_repo_dir = '/etc/yum.repos.d/'

bash_profile = user.lower() + '/.bashrc'
if user.lower() != 'root': bash_profile = '/home/' + bash_profile

linux_users = [user]
hdfs_users = [user]

# Commands executed in order in master.py
commands = []
# First create all needed dirs
mkdirs=[root_dir, root_dir+'/notebooks', pid_dir, log_dir, root_dir+'/.ipython']
for dir in mkdirs: commands.append('mkdir -p ' + dir)
# Install script
commands.append('sh ' + scripts_dir + 'jupyter_setup.sh ' + root_dir + ' ' + files_dir)
# Set ownership of all directories to proper users
for dir in mkdirs:
  commands.append('chown -R ' + user + ' ' + dir)
  commands.append('chgrp -R ' + user + ' ' + dir)

start_args = ['"pyspark --master yarn --executor-memory '+executor_memory+' --num-executors '+num_executors+'"', log_dir + '/notebook.log', pid_file]
start_command = 'source ' + bash_profile + '; sh ' + scripts_dir + 'start.sh ' + ' '.join(start_args)
