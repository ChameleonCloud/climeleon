import argparse
import operator
import re
import sys

from keystoneauth1 import adapter, loading, session
from keystoneauth1.identity import v3

import logging
logging.basicConfig(level=logging.INFO)

class BaseCommand:
    description = None

    @classmethod
    def main(cls):
        cls(sys.argv[1:])

    def __init__(self, argv=None):
        self.args = self.parse_args(argv)

        self.auth = loading.cli.load_from_argparse_arguments(self.args)
        self.session = loading.session.load_from_argparse_arguments(
            self.args, auth=self.auth)
        # Wrap session in adapter that sets interface/region
        self.session = adapter.Adapter(
            session=self.session, interface=self.args.os_interface,
            region_name=self.args.os_region_name)

        self.log = logging.getLogger(__name__)

        self.run()

    def run(self):
        pass

    def parse_args(self, argv):
        argv = sys.argv[1:]

        parser = argparse.ArgumentParser(description=self.description)
        loading.cli.register_argparse_arguments(
            parser, argv, default='password')
        loading.session.register_argparse_arguments(parser)
        loading.adapter.register_argparse_arguments(parser)

        return parser.parse_args()
