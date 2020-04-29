from climeleon.base import BaseCommand

class NetworkDeleteCommand(BaseCommand):
    description = "Tear down a network, including routers and subnets."

    def run(self):
        self.log.info("Running")
