import argparse
import operator
import re
import sys

import chi

import logging
logging.basicConfig(level=logging.INFO)


class BaseCommand:
    description = None

    @classmethod
    def main(cls):
        instance = cls(sys.argv[1:])
        try:
            instance.run()
        except:
            instance.log.exception("Aborted")
            sys.exit(1)
        sys.exit(0)

    def __init__(self, argv=None):
        self.args = self.parse_args(argv)
        self.session = chi.session()
        self.log = logging.getLogger(__name__)

    def blazar(self):
        return chi.blazar(session=self.session)

    def glance(self):
        return chi.glance(session=self.session)

    def gnocchi(self):
        return chi.gnocchi(session=self.session)

    def ironic(self):
        return chi.ironic(session=self.session)

    def keystone(self):
        return chi.keystone(session=self.session)

    def neutron(self):
        return chi.neutron(session=self.session)

    def nova(self):
        return chi.nova(session=self.session)

    def parse_args(self, argv):
        argv = sys.argv[1:]
        parser = argparse.ArgumentParser(description=self.description)

        self.register_args(parser)

        return parser.parse_args()

    def run(self):
        pass

    def register_args(self, parser):
        pass
