import os, pwd, grp, signal, platform
from resource_management import *

def package_dir(): return os.path.realpath(__file__).split('/package')[0] + '/package/'

def add_repos():
  distribution = platform.linux_distribution()[0].lower()
  #TODO: add ubuntu
  if distribution in ['centos', 'redhat'] :
    repo_dir = package_dir()+'files/repos/rhel6/'
    os_repo_dir = '/etc/yum.repos.d/'

  for repo in os.listdir(repo_dir):
    if not os.path.isfile(os_repo_dir + repo):
      Execute('cp ' + repo_dir+repo + ' ' + os_repo_dir)

def create_linux_user(user, group):
  try: pwd.getpwnam(user)
  except KeyError: Execute('useradd ' + user)
  try: grp.getgrnam(group)
  except KeyError: Execute('groupadd ' + group)

def create_hdfs_user(user):
  Execute('hadoop fs -mkdir -p /user/'+user, user='hdfs')
  Execute('hadoop fs -chown ' + user + ' /user/'+user, user='hdfs')
  Execute('hadoop fs -chgrp ' + user + ' /user/'+user, user='hdfs')

def stop(pid_file):
  with open(pid_file, 'r') as fp:
    try:os.kill(int(fp.read().strip()), signal.SIGTERM)
    except OSError: pass

