import os, pwd, grp, signal
from resource_management import *

def add_repos(repo_dir, install_dir):
  for repo in os.listdir(repo_dir):
    add_repo(repo_dir, repo, install_dir)

def add_repo(repo_dir, repo, install_dir):
  if not os.path.isfile(install_dir + repo):
    Execute('cp ' + repo_dir + repo + ' ' + install_dir)

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
