#!/usr/bin/env python
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
from resource_management import *
import os

# server configurations
config = Script.get_config()

package_dir = os.path.realpath(__file__).split('/package')[0] + '/package/'
files_dir = package_dir + 'files/'
scripts_dir = package_dir + 'scripts/'

distribution = platform.linux_distribution()[0].lower()
if distribution in ['centos', 'redhat'] :
  repo_dir = files_dir+'repos/rhel6/'
  os_repo_dir = '/etc/yum.repos.d/'

commands = ['cd /tmp; sh ' + scripts_dir + 'python27_install.sh ' + files_dir]
