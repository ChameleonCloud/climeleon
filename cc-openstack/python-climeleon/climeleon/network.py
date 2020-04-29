from operator import itemgetter

from climeleon.base import BaseCommand

class NetworkDeleteCommand(BaseCommand):
    description = "Tear down a network, including routers and subnets."

    def register_args(self, parser):
        parser.add_argument("--segment")
        parser.add_argument("--network")

    def run(self):
        neutron = self.neutron()

        if self.args.segment is not None:
            network = self._find_network(neutron, {
                "provider:segmentation_id": self.args.segment
            })
        elif self.args.network is not None:
            network = neutron.get_network(self.args.network)
        else:
            raise ValueError("Missing either segment ID or network ID")

        # Find ports
        ports = self._list_for_network(neutron, network, "ports")

        # Abort if there are nova ports, this means there are running instances
        if any(p.get("device_owner") == "compute:nova" for p in ports):
            raise ValueError("Network has running instances!")

        router_ports = [
            p for p in ports
            if p["device_owner"] == "network:router_interface"
        ]

        # Detach subnets from router(s)
        for p in router_ports:
            self.log.info("Deleting router interface {}".format(p["id"]))
            neutron.remove_interface_router(p["device_id"], {
                "port_id": p["id"]
            })

        subnets = self._list_for_network(neutron, network, "subnets")

        for s in subnets:
            self.log.info("Deleting subnet {}".format(s["id"]))
            neutron.delete_subnet(s["id"])

        self.log.info("Deleting network {}".format(network["id"]))
        neutron.delete_network(network["id"])

        for p in router_ports:
            router_id = p["device_id"]
            other_router_ports = neutron.list_ports(
                device_id=router_id,
                device_owner=p["device_owner"]
            ).get("ports")
            if not other_router_ports:
                self.log.info("Removing router gateway")
                neutron.remove_gateway_router(router_id)
                self.log.info("Removing router {}".format(router_id))
                neutron.delete_router(router_id)



    def _find_network(self, neutron, params):
        networks = neutron.list_networks(**params).get("networks")

        if not networks:
            raise ValueError("Could not find network for {}".format(params))

        return networks[0]

    def _list_for_network(self, neutron, network, name):
        network_id = network.get("id")
        getter = getattr(neutron, "list_{}".format(name))
        return getter(network_id=network_id).get(name)


class NetworkSegmentStatusCommand(BaseCommand):
    description = """
    Display the current Neutron networks assigned for each VLAN. The name of
    network and its owning project are also displayed.
    """

    def run(self):
        neutron = self.neutron()
        networks = neutron.list_networks().get("networks")

        rows = []
        rows.append([
            "physical_network",
            "segmentation_id",
            "name",
            "project_id"
        ])
        for n in sorted(networks, key=itemgetter("provider:segmentation_id")):
            rows.append([
                n["provider:physical_network"],
                str(n["provider:segmentation_id"]),
                n["name"],
                n["project_id"]
            ])

        widths = [max(map(len, col)) for col in zip(*rows)]
        for row in rows:
            print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
