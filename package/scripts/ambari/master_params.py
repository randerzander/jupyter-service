#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import ambari_helpers as helpers

# server configurations
config = Script.get_config()

# Notebook service configs
user = config['configurations']['jupyter-env']['jupyter.user']
log_dir = config['configurations']['jupyter-env']['log.dir']
pid_file = config['configurations']['jupyter-env']['pid.file']
pid_dir = '/'.join(pid_file.split('/')[0:-1])
jupyter_port = str(config['configurations']['jupyter-env']['jupyter.port'])
spark_home = config['configurations']['jupyter-env']['spark.home']

package_dir = helpers.package_dir()
files_dir = package_dir + 'files/'
scripts_dir = package_dir + 'scripts/'
root_dir = '/home/'+user

linux_users = [user]
hdfs_users = [user]

# Commands executed in order in master.py
commands = []
# First create all needed dirs
mkdirs=[root_dir, root_dir+'/notebooks', pid_dir, log_dir, root_dir+'/.ipython']
for dir in mkdirs: commands.append('mkdir -p ' + dir)

# Jupyter config script
commands.append(' '.join(['sh', scripts_dir+'shell/jupyter_setup.sh', root_dir, files_dir, spark_home, jupyter_port]))

# Set ownership of all directories to proper users
for dir in mkdirs:
  commands.append('chown -R ' + user + ' ' + dir)
  commands.append('chgrp -R ' + user + ' ' + dir)

start_args = ['"ipython notebook --profile default --ipython-dir '+root_dir+'/.ipython --notebook-dir '+root_dir+'/notebooks"', log_dir + '/server.log', pid_file]
start_command = 'source ~/.bashrc; sh ' + scripts_dir + 'shell/start.sh ' + ' '.join(start_args)
