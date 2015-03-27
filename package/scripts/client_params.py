#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *

# server configurations
config = Script.get_config()
pid_file = config['configurations']['ipython-env']['pid_file']

prefix = 'cd /tmp; '
stack_dir = '/var/lib/ambari-agent/cache/stacks/HDP/2.2/services/ipython-stack/package/'
files_dir = stack_dir + 'files/'
scripts_dir = stack_dir + 'scripts/'

install = prefix + 'sh ' + scripts_dir + 'python27_install.sh ' + files_dir
commands = {'install': install}
