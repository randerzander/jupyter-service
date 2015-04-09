from resource_management import *
import ambari_helpers as helpers

class Master(Script):
  def install(self, env):
    self.configure(env)
    import master_params as params

    # Add OS repos and install OS packages
    helpers.add_repos(params.repo_dir, params.os_repo_dir)
    self.install_packages(env)

    # Create user and group if they don't exist
    for user in params.linux_users: helpers.create_linux_user(user, user)
    for user in params.hdfs_users: helpers.create_hdfs_user(user)

    # Iterate through and run install commands defined in params
    for command in params.commands: Execute(command)

  def stop(self, env):
    import status_params as params
    env.set_params(params)
    helpers.stop(params.pid_file)
 
  def start(self, env):
    import master_params as params
    env.set_params(params)
    Execute(params.start_command, user=params.user)

  def status(self, env):
    import status_params as params
    env.set_params(params)
    check_process_status(params.pid_file)

  def configure(self, env):
    import master_params as params
    env.set_params(params)

if __name__ == "__main__":
  Master().execute()
