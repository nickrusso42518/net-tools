#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collect IPv6 management loopbacks from the BGP table and
create an Ansible inventory from it.
"""

import sys
from ipaddress import IPv6Network
from netmiko import Netmiko
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


def main(mgmt_prefix):
    """
    Execution starts here.
    """

    # Create an IPv6 network object to test subnet containment later
    mgmt_net = IPv6Network(mgmt_prefix)

    # Create netmiko SSH connection handler to access the device
    conn = Netmiko(
        host="192.0.2.1",
        username="cisco",
        password="cisco",
        device_type="cisco_ios",
    )

    # Should be using "show bgp ipv6 unicast" but code has bug
    # https://github.com/CiscoTestAutomation/genieparser/issues/362
    resp = conn.send_command("show bgp all", use_genie=True)
    v6_rte = resp["vrf"]["default"]["address_family"]["ipv6 unicast"]["routes"]

    # Initialize Ansible YAML inventory dictionary
    ansible_inv = {"all": {"children": {"remotes": {"hosts": {}}}}}

    # Iterate over all collected BGP prefixes
    for index, prefix in enumerate(v6_rte.keys()):

        # Create an IPv6 network representing the specific prefix
        prefix_net = IPv6Network(prefix.lower())

        # Test for subnet containment and for /128 mask
        if prefix_net.subnet_of(mgmt_net) and prefix.endswith("/128"):

            # Assemble inventory item and update inventory dict
            prefix_str = DoubleQuotedScalarString(prefix_net.network_address)
            ansible_inv["all"]["children"]["remotes"]["hosts"].update(
                {f"node_{index + 1}": {"ansible_host": prefix_str}}
            )
            print(prefix_str)

    # Close connection when finished
    conn.disconnect()

    # Instantiate the YAML object, preserving quotes and
    # using explicit start (---) and end (...) markers
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.explicit_start = True
    yaml.explicit_end = True

    # Dump the Ansible inventory to a new file for use later
    with open("bgp_hosts.yml", "w") as handle:
        yaml.dump(ansible_inv, handle)


if __name__ == "__main__":

    # If an IPv6 prefix isn't specified, use RFC3849 documentation prefix
    if len(sys.argv) < 2:
        main("2001:db8::/32")

    # IPv6 prefix was specified; extract and convert to lowercase
    else:
        main(sys.argv[1].lower())
