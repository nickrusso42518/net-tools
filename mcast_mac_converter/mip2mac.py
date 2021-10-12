#!/usr/bin/python

###############################################################################
# File: mip2mac.py
# Author: Nicholas Russo
# Description: Simple utility to convert a multicast IPv4 address to its
#  corresponding multicast MAC address (EUI). IPv4 multicast addresses are
#  supplied as CLI arguments.
###############################################################################

from IPv4Address import IPv4Address
from MACAddress import MACAddress
import sys

# Utiltiy that concerts a dotted-decimal IPv4 address into an EUI formatted MAC
#  For those less *nix inclined, files that contain multicast IP addresses
#  (one per row) can be fed into this utility as shown below:
#  cat mip2mac.inputfile | xargs python mip2mac.py
def mip2mac(args):

    # Test for CLI arguments (first element is the script name)
    if len(args) < 2:
        # No arguments were supplied; print usage help and exit
        print("Usage:   mip2mac mip1 mip2 mipn")
        print("Example: mip2mac 239.1.1.1 239.2.2.2")
        return 1

    # MIPs have been supplied; remove the script name and iterate over MIPs
    args.pop(0)
    for mipArg in args:

        # Creat an IPv4Address object by parsing the CLI argument string
        mip = IPv4Address(mipArg)

        # If the MIP isn't multicast, this script doesn't make sense; skip this
        if not mip.isMulticast():
            continue

        # First IP address octet means nothing (per RFC 1112)
        macInputString = "01:00:5E:" + str(
            hex(mip.getOctet(2) % 128)[2:].zfill(2)
        )
        macInputString += ":" + str(hex(mip.getOctet(3))[2:].zfill(2))
        macInputString += ":" + str(hex(mip.getOctet(4))[2:].zfill(2))

        # Create a MAC address object and print it as a string
        mac = MACAddress(macInputString)
        print(mac)


###############################################################################
# Execution starts here; capture any command line arguments
mip2mac(sys.argv)
