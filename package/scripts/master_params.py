#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *

# server configurations
config = Script.get_config()

# Notebook service configs
# TODO - add port configuration
user = config['configurations']['ipython-config']['ipython.user']
group = config['configurations']['ipython-config']['ipython.group']
log_dir = config['configurations']['ipython-config']['log.dir']
pid_file = config['configurations']['ipython-env']['pid_file']
pid_dir = '/'.join(pid_file.split('/')[0:-1])

root_dir = '/home/'+user
mkdirs=[root_dir, root_dir+'/notebooks', pid_dir, log_dir]

bash_profile = user.lower() + '/.bashrc'
if user.lower() != 'root': bash_profile = '/home/' + bash_profile

stack_dir = '/var/lib/ambari-agent/cache/stacks/HDP/2.2/services/ipython-stack/package/'
files_dir = stack_dir + 'files/'
scripts_dir = stack_dir + 'scripts/'

# Spark configs
num_executors = str(config['configurations']['ipython-config']['num.executors'])
executor_memory = str(config['configurations']['ipython-config']['executor.memory'])

ipynb_install = 'sh ' + scripts_dir + 'ipynb_install.sh ' + root_dir + ' ' + files_dir
start_cmd = 'source ' + bash_profile + '; sh ' + scripts_dir + 'start.sh'
start_args = ['"'+root_dir+'/spark/bin/pyspark --master yarn-client --num-executors '+num_executors+' --executor-memory '+executor_memory+' --matplotlib"', log_dir + '/notebook.log', pid_file]
commands = {'install': ipynb_install, 'start': start_cmd + ' ' + ' '.join(start_args)}
