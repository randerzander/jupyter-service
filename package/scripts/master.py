import sys, os, pwd, grp, signal
from resource_management import *

class Master(Script):
  def install(self, env):
    self.configure(env)
    import master_params as params

    # Create all necessary directories
    for dir in params.mkdirs: Execute('mkdir -p ' + dir)

    # Add repos to yum
    for repo in os.listdir(params.files_dir+'repos/'):
      if not os.path.isfile('/etc/yum.repos.d/' + repo):
        Execute('cp ' + params.files_dir+'repos/' + repo + ' /etc/yum.repos.d/')
    self.install_packages(env)

    # Create user and group if they don't exist
    self.create_linux_user(params.user, params.group)
    self.create_hdfs_user(params.user)

    Execute(params.commands['install'])

    # Change ownership of necessary files back to params.user
    for dir in params.mkdirs: self.set_ownership(params.user, params.group, dir)

  def stop(self, env):
    import status_params as params
    env.set_params(params)
    with open(params.pid_file, 'r') as fp:
      os.kill(int(fp.read().strip()), signal.SIGTERM)
      
  def start(self, env):
    import master_params as params
    env.set_params(params)
    Execute(params.commands['start'], user=params.user)

  def status(self, env):
    import status_params as params
    env.set_params(params)
    check_process_status(params.pid_file)

  def configure(self, env):
    import master_params as params
    env.set_params(params)

  def set_ownership(self, user, group, dir):
    Execute('chown -R ' + user + ' ' + dir)
    Execute('chgrp -R ' + group + ' ' + dir)

  def create_linux_user(self, user, group):
    try: pwd.getpwnam(user)
    except KeyError: Execute('useradd ' + user)
    try: grp.getgrnam(group)
    except KeyError: Execute('groupadd ' + group)

  def create_hdfs_user(self, user):
    Execute('hadoop fs -mkdir -p /user/'+user, user='hdfs')
    Execute('hadoop fs -chown ' + user + ' /user/'+user, user='hdfs')
    Execute('hadoop fs -chgrp ' + user + ' /user/'+user, user='hdfs')

if __name__ == "__main__":
  Master().execute()
