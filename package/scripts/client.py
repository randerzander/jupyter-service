import sys, os, pwd, grp, signal
from resource_management import *
import ambari_helpers as helpers

class Client(Script):
  def install(self, env):
    self.configure(env)
    import client_params as params

    # Add repos to yum
    helpers.add_repos(params.repo_dir, params.os_repo_dir)
    self.install_packages(env)

    for command in params.commands: Execute(command)

  def status(self, env): raise ClientComponentHasNoStatus()

  def configure(self, env):
    import client_params as params
    env.set_params(params)

if __name__ == "__main__":
  Client().execute()
