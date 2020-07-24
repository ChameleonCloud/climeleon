import argparse
import operator
import re
import sys

from blazarclient.client import Client as BlazarClient
from glanceclient.client import Client as GlanceClient
from gnocchiclient.v1.client import Client as GnocchiClient
from ironicclient import client as IronicClient
from keystoneauth1 import adapter, loading, session
from keystoneauth1.identity import v3
from keystoneclient.v3.client import Client as KeystoneClient
from neutronclient.v2_0.client import Client as NeutronClient
from novaclient.client import Client as NovaClient

import logging
logging.basicConfig(level=logging.INFO)

IRONIC_CLIENT_VERSION = 1


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

        self.auth = loading.cli.load_from_argparse_arguments(self.args)
        self.session = loading.session.load_from_argparse_arguments(
            self.args, auth=self.auth)
        # Wrap session in adapter that sets interface/region
        self.session = adapter.Adapter(
            session=self.session, interface=self.args.os_interface,
            region_name=self.args.os_region_name)

        self.log = logging.getLogger(__name__)


    def blazar(self):
        return BlazarClient("1",
            service_type="reservation",
            session=self.session)

    def glance(self):
        return GlanceClient("2", session=self.session)

    def gnocchi(self):
        session_options = dict(auth=self.session.session.auth)
        adapter_options = dict(interface=self.session.interface,
                               region_name=self.session.region_name)
        return GnocchiClient(
            adapter_options=adapter_options, session_options=session_options
        )

    def ironic(self):
        return IronicClient.get_client(
            IRONIC_CLIENT_VERSION,
            session=self.session,
            region_name=self.session.region_name,
            # Ironic client defaults to 1.9 currently,
            # "latest" will be latest the API supports
            os_ironic_api_version='latest'
        )

    def keystone(self):
        return KeystoneClient(
            session=self.session,
            interface=self.session.interface,
            region_name=self.session.region_name
        )

    def neutron(self):
        return NeutronClient(session=self.session)

    def nova(self):
        return NovaClient("2", session=self.session)

    def parse_args(self, argv):
        argv = sys.argv[1:]

        parser = argparse.ArgumentParser(description=self.description)
        loading.cli.register_argparse_arguments(
            parser, argv, default='password')
        loading.session.register_argparse_arguments(parser)
        loading.adapter.register_argparse_arguments(parser)

        self.register_args(parser)

        return parser.parse_args()

    def run(self):
        pass

    def register_args(self, parser):
        pass
