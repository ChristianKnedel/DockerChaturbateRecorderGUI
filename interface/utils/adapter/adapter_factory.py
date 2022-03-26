from .adapter.docker_adapter import DockerAdapter

class AdapterFactory():
   def create_adapter(self, targetclass):
      return globals()[targetclass]()


