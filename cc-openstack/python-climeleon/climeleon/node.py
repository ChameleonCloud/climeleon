#!/usr/bin/env python
"""
node-assign-switch-ids

Intended as a migration script for https://collab.tacc.utexas.edu/issues/17386, but could
be useful later. Exists mostly as documentation and perhaps example code that can be re-used.
"""
from argparse import FileType
from dracclient.client import DRACClient
import operator
import re

from climeleon.base import BaseCommand

IRONIC_CLIENT_VERSION = 1


class NodeAssignSwitchIDsCommand(BaseCommand):

    @staticmethod
    def uc_assignment_strategy(cls, node, port):
        # Names are like c01, nc24.
        # Strip prefix and cast as integer.
        if node.name.startswith('nc'):
            link = port.local_link_connection
            switch_info = link["switch_info"]
            if switch_info == "chameleon-corsa1":
                start_id = 100
            elif switch_info == "chameleon-corsa2":
                start_id = 132
            else:
                raise ValueError((
                    "Cannot figure out new port ID for node {}: unknown switch {}"
                    .format(node.uuid, switch_info)
                ))
            return start_id + int(re.sub(r'^P ', '', link["port_id"]))
        elif node.name.startswith('c'):
            return 200 + int(re.sub(r'^[a-z]+', '', node.name))
        else:
            raise ValueError("Cannot figure out new port ID for node {}".format(node.uuid))

    @staticmethod
    def tacc_assignment_strategy(cls, node, port):
        link = port.local_link_connection
        switch_info = link["switch_info"]

        if switch_info == "roc-ax35-sw1":
            start_id = 100
            return start_id + int(re.sub(r'^P ', '', link["port_id"]))
        else:
            raise ValueError((
                "Cannot figure out new port ID for node {}: unknown switch {}"
                .format(node.uuid, switch_info)
            ))

    REGION_STRATEGIES = {
        "CHI@TACC": tacc_assignment_strategy,
        "CHI@UC": uc_assignment_strategy,
    }

    def run(self):
        region_name = self.args.os_region_name
        ironic = self.ironic()

        ports_for_update = []

        for node in ironic.node.list(sort_key='name'):
            ports = ironic.port.list(detail=True, node=node.uuid)

            if not ports:
                self.log.error("No ports found for node {}".format(node.uuid))
                continue

            port = ports[0]
            switch_info = port.local_link_connection["switch_info"]
            port_id = port.local_link_connection["port_id"]

            assignment_strategy = self.REGION_STRATEGIES.get(region_name)

            if not assignment_strategy:
                self.log.error("No port assignment strategy found!")
                continue

            try:
                switch_id = assignment_strategy(node, port)
            except:
                self.log.exception("Failed to assign switch_id for node")
                continue

            if int(port.local_link_connection["switch_id"].replace(":", "")) != switch_id:
                ports_for_update.append(dict(
                    node=node, uuid=port.uuid,
                    switch_id=switch_id, switch_info=switch_info, port_id=port_id
                ))

            # Ensure other secondary ports have switch_id unset
            for p in ports[1:]:
                link = p.local_link_connection
                if int(link["switch_id"].replace(":", "")) != 0:
                    ports_for_update.append(dict(
                        node=node, uuid=p.uuid,
                        switch_id=0, switch_info=link["switch_info"], port_id=link["port_id"]
                    ))

        for p in sorted(ports_for_update, key=lambda p: p["node"].name):
            node = p["node"]
            node_uuid = node.uuid
            node_name = node.name
            port_uuid = p["uuid"]
            padded_switch_id = str(p["switch_id"]).zfill(16)

            patch = [
                dict(
                    path="/local_link_connection/switch_id",
                    value=padded_switch_id,
                    op="replace"
                )
            ]

            try:
                force_maintenance = not node.maintenance

                if force_maintenance:
                    ironic.node.set_maintenance(node_uuid, True,
                        maint_reason="node-assign-switch-ids: updating local_link_connection")

                ironic.port.update(port_uuid, patch)

                if force_maintenance:
                    ironic.node.set_maintenance(node_uuid, False)

                self.log.info("{} port {} [{}:{}] updated to switch_id={}".format(
                    node_name, port_uuid, p["switch_info"], p["port_id"], padded_switch_id))
            except:
                self.log.exception("failed to update port {}".format(p["uuid"]))


class NodeRotateIPMIPasswordCommand(BaseCommand):

    FACTORY_PASSWORD = "calvin"

    def register_args(self, parser):
        parser.add_argument("nodes", metavar="NODE", nargs="+")
        parser.add_argument("--password-file", type=FileType("r"),
                            required=True)
        parser.add_argument("--old-password-file", type=FileType("r"))

    def run(self):
        new_password = self.args.password_file.read().strip()
        self.args.password_file.close()

        if self.args.old_password_file:
            old_password = self.args.old_password_file.read().strip()
            self.args.old_password_file.close()
        else:
            # TODO: maybe depends if we can detect BMC vendor
            old_password = self.FACTORY_PASSWORD

        ironic = self.ironic()
        nodes = ironic.node.list(detail=True)

        def find_node(name_or_id):
            matching = [
                n for n in nodes
                if n.uuid == name_or_id or n.name == name_or_id
            ]
            if matching:
                return matching[0]
            else:
                raise ValueError("No node matched '{}'".format(name_or_id))

        for n in self.args.nodes:
            node = find_node(n)
            node_id = node.uuid

            if node.provision_state not in ["active", "available"]:
                raise ValueError(
                    "Node {} in invalid provision state".format(node_id))

            self.log.info("Processing {} ({}):".format(node_id, node.name))

            if not node.maintenance:
                ironic.node.set_maintenance(
                    node.id, True, maint_reason="Updating IPMI password")
                self.log.info("  Put node into maintenance mode")

            try:
                driver_info = node.driver_info
                ipmi_username = driver_info.get("ipmi_username")
                ipmi_address = driver_info.get("ipmi_address")
                ipmi_password = old_password

                drac = DRACClient(
                    host=ipmi_address, username=ipmi_username,
                    password=ipmi_password)

                # TODO: we just assume it's the root user (id=1)
                drac.set_idrac_settings({
                    "Users.1#Password": new_password
                })
                self.log.info("  Updated iDRAC password")

                new_driver_info = driver_info.copy()
                new_driver_info.update(ipmi_password=new_password)
                ironic.node.update(node.id, driver_info=new_driver_info)
                self.log.info("  Updated Ironic node ipmi_password")

                # Test that the connection works
                boot_dev = ironic.node.get_boot_device(node_id)
                assert "boot_device" in boot_dev
            except:
                self.log.exception("  Failed to update password")
                break
            finally:
                # Restore original maintenance state
                if not node.maintenance:
                    ironic.node.set_maintenance(node.id, False)
                    self.log.info("  Reverted node maintenance state")
