import sys, os, pwd, grp, signal
from resource_management import *

class Client(Script):
  def install(self, env):
    self.configure(env)
    import client_params as params

    # Add repos to yum
    for repo in os.listdir(params.files_dir+'repos/'):
      if not os.path.isfile('/etc/yum.repos.d/' + repo):
        Execute('cp ' + params.files_dir+'repos/' + repo + ' /etc/yum.repos.d/')
    self.install_packages(env)

    Execute(params.commands['install'])

  def status(self, env): raise ClientComponentHasNoStatus()

  def configure(self, env):
    import client_params as params
    env.set_params(params)

if __name__ == "__main__":
  Client().execute()
