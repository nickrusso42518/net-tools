# IPv6 Tools
This directory contains a variety of IPv6 tools, most of which relate to
a DHCPv6 prefix delegation solution I designed for a customer. These
are meant to be simple and standalone tools focused on solving problems
rather than academic examples of software perfection.

  * [EUI64 Ansible Inventory Maker](#eui64-ansible-inventory-maker)
  * [BGP Ansible Inventory Maker](#bgp-ansible-inventory-maker)
  * [Cisco IOS EEM Boot Script](#cisco-ios-eem-boot-script)
  * [Testing](#testing)

## EUI64 Ansible Inventory Maker
The `ans_inv_from_eui64.py` script takes a list of MAC addresses in a plain
text file named `macs.txt` with one MAC address per line. Any common format
or mix of delimeters is acceptable, including hyphens (`-`), colons (`:`),
or periods (`.`) between the hexadecimal characters.

There are two forms of output.
  1. Prints the original MAC addresses followed by the EUI64 IPv6 address
     derived from that MAC address on a singleline. This information is
     written to standard output as a quick visual check. Those that do not
     use Ansible may benefit from these quick conversions when applied to
     other use-cases.
  2. Generates a `eui64_hosts.yml` file which conforms to the Ansible YAML
     inventory standard. Each MAC address is represented by a new node using
     the EUI64 IPv6 address as the `ansible_host` parameter for connectivity.

You can optionally pass in the IPv6 management prefix to script as a
command line argument. If no argument is supplied, the script uses the RFC3849
documentation prefix of `2001:db8::` in front of every EUI64 IPv6 address. The
prefix should be a plain string to be prepended to the EUI64 IPv6 address and
should *not* contain a prefix-length using `/` notation.

## BGP Ansible Inventory Maker
The `ans_inv_from_bgp.py` is similar to the EUI64 script except dynamically
extracts management loopbacks from the IPv6 BGP table. IPv6 /128 routes that
are contained (ie, are subnets of) a larger management prefixes are
printed to stdout and are captured in an Ansible inventory file titled
`bgp_hosts.yml`.

Just like the EUI64 script, you can optionally supply the IPv6 management
prefix via CLI argument. If omitted, `2001:db8::/32` is used. Because these
prefixes could be variable length (unlike EUI64), you can supply a prefix
length using slash notation.

You can edit the script to include your specific router IP/hostname, along
with username/password credentials for SSH. Be sure to target a router that
has a "full view" of all management loopbacks, such as a core switch or
WAN aggregation device.

## Cisco IOS EEM Boot Script
The `ios_eem_script.txt` file is a reference configuration for Cisco IOS devices
that contains a relatively complex Embedded Event Manager (EEM) script. The
script performs two key tasks upon initial boot when necessary:
  1. Update the hostname to a unique string based on the device's serial number
  2. Update the Loopback0 IPv6 address to use /128 prefix-length while
     preserving the EUI64 IPv6 address already applied

Expressed in rough Python pseudo-code:

```
if not hostname.startswith("REMOTE-"):
    hostname = f"REMOTE-{device.sn}"
    loopback0.ipv6 = loopback0.ipv6.replace("64", "128")
```


## Testing
A GNU `Makefile` is used to automate testing with the following targets:
  * `lint`: Runs `yamllint` and `pylint` linters, and the `black` formatter
  * `run`: Performs test runs of all locally executable scripts
  * `clean`: Deletes any artifacts, such as `.pyc` and `hosts.yml` files
  * `all`: Default target that runs the sequence `clean lint run`
