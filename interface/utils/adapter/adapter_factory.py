from .adapter.docker_adapter import DockerAdapter
from .adapter.shell_adapter import ShellAdapter

class AdapterFactory():
   def create_adapter(self, targetclass):
      return globals()[targetclass]()


