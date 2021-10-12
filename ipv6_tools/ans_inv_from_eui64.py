#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Converts a list of MAC addresses into their IPv6 EUI-64
addresses. Prints the resulting EUI-64 addresses to stdout and creates
and Ansible YAML inventory for future configuration management.
"""

import sys
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


def main(v6_prefix):
    """
    Execution begins here.
    """

    # Load MAC addresses from file
    with open("input_macs.txt", "r") as handle:
        lines = handle.readlines()

    # Initialize Ansible YAML inventory dictionary
    ansible_inv = {"all": {"children": {"remotes": {"hosts": {}}}}}

    # Iterate over the lines read from file
    for index, line in enumerate(lines):

        # Clean up the line; remove whitespace and delimeters
        mac = line.strip().lower()
        for delim in ["-", ":", "."]:
            mac = mac.replace(delim, "")

        # If MAC is invalid, skip it and continue with the next MAC
        if not is_valid_mac(mac):
            continue

        # Build the low-order 64 bits of the IPv6 address
        host_addr = f"{mac[:4]}:{mac[4:6]}ff:fe{mac[6:8]}:{mac[8:]}"

        # Flip the 7th bit of first byte (3rd bit of second nibble) using xor
        flip = hex(int(host_addr[1], 16) ^ 2)[-1]

        # Re-assemble host bits with flipped bit plus IPv6 prefix
        eui64_addr = f"{v6_prefix}{host_addr[:1]}{flip}{host_addr[2:]}"

        # Display MAC address and newly-computed EUI-64 IPv6 address
        print(mac, eui64_addr)

        # Update the Ansible inventory dict with new host. The hostname
        # will be "node_" plus the entire MAC address (user can modify).
        # The IPv6 address is the address to which Ansible connects and
        # the original MAC is retained for documentation/troubleshooting
        ansible_inv["all"]["children"]["remotes"]["hosts"].update(
            {
                f"node_{index + 1}": {
                    "ansible_host": DoubleQuotedScalarString(eui64_addr),
                    "original_mac": DoubleQuotedScalarString(mac),
                }
            }
        )

    # Instantiate the YAML object, preserving quotes and
    # using explicit start (---) and end (...) markers
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.explicit_start = True
    yaml.explicit_end = True

    # Dump the Ansible inventory to a new file for use later
    with open("eui64_hosts.yml", "w") as handle:
        yaml.dump(ansible_inv, handle)


def is_valid_mac(mac):
    """
    There are three criteria for a MAC to be valid. Additional checks
    may be added in the future.
      1. Exactly 12 bytes
      2. Only hex digits
      3. 8th bit of the first byte is 0 (ensures unicast only)
    """
    return len(mac) == 12 and int(mac, 16) > 0 and int(mac[1], 16) & 1 == 0


if __name__ == "__main__":

    # If an IPv6 prefix isn't specified, use RFC3849 documentation prefix
    if len(sys.argv) < 2:
        main("2001:db8::")

    # IPv6 prefix was specified; extract and convert to lowercase
    else:
        main(sys.argv[1].lower())
