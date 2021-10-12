#!/usr/bin/python

###############################################################################
# File: mip2mac6.py
# Author: Nicholas Russo
# Description: Simple utility to convert a multicast IPv6 address to its
#  corresponding multicast MAC address (EUI). IPv6 multicast addresses are
#  supplied as CLI arguments.
###############################################################################

from IPv6Address import IPv6Address
from MACAddress import MACAddress
import sys

# Utiltiy that concerts an extended EUI IPv6 address into an EUI formatted MAC
#  For those less *nix inclined, files that contain multicast IP addresses
#  (one per row) can be fed into this utility as shown below:
#  cat mip2mac6.inputfile | xargs python mip2mac6.py
def mip2mac6(args):

    # Test for CLI arguments (first element is the script name)
    if len(args) < 2:
        # No arguments were supplied; print usage help and exit
        print("Usage:   mip2mac6 mip1 mip2 mipn")
        print("Example: mip2mac6 ff00:0000:0000:0000:0000:0000:0000:0001")
        return 1

    # MIPs have been supplied; remove the script name and iterate over MIPs
    args.pop(0)
    for mipArg in args:

        # Creat an IPv6Address object by parsing the CLI argument string
        mip = IPv6Address(mipArg)

        # If the MIP isn't multicast, this script doesn't make sense; skip this
        if not mip.isMulticast():
            continue

        # return MACAddress( [ 0x33, 0x33, ipv6.getOctet(13), ipv6.getOctet(14), ipv6.getOctet(15), ipv6.getOctet(16) ] )

        # First 12 IPv6 address octet mean nothing (per RFC 2464)
        #  The last 4 octets (13 through 16)
        macInputString = "33:33"
        for i in range(13, 17):
            macInputString += ":" + str(hex(mip.getOctet(i))[2:].zfill(2))

        # Create a MAC address object and print it as a string
        mac = MACAddress(macInputString)
        print(mac)


###############################################################################
# Execution starts here; capture any command line arguments
mip2mac6(sys.argv)
