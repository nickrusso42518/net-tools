#!/usr/bin/python

###############################################################################
# File: IPv6Address.py
# Author: Nicholas Russo
# Description: This file includes a class that represents an IPv4 address.
#  Specific IPv6 operations, such as testing unicast/multicast or printing
#  string versions of the address are supported. More basic operations such as
#  retrieving an octet or measuring the number of octets are defined in the
#  parent class (NetAddress).
###############################################################################

from NetAddress import NetAddress

# Defines an IPv6 address, inheriting from NetAddress
class IPv6Address(NetAddress):

    # Invokes the parent constructor to build the network address, which
    #  performs most of the heavy lifting. Performs upper-bound checking
    #  on the address length to ensure it is not greater than 128. Note
    #  that the parent constructor performs lower-bound checking already.
    def __init__(self, inputString, addrLen=128):
        if addrLen > 128:
            raise ValueError("addrLen is greater than 128: " + str(addrLen))
        NetAddress.__init__(self, inputString, addrLen)

    # Implements the abstract method defined in NetAddress. Breaks a
    #  fully-extended EUI IPv6 address into a list of 16 integers; this
    #  list is returned from the method
    def _parseInputString(self, inputString):

        # Split the input string into 8 separate double-octets; any errors
        #  raised by this method are passed up the recursion stack
        ipStringOctets = self._splitInputString(inputString, ":", 8)

        # Iterate over all of the substrings, which should be
        #  16-bit unsigned integers
        integerOctets = []
        for ipStringOctet in ipStringOctets:

            # Test for valid range 0 <= x <= 65535
            current = int(ipStringOctet, 16)
            if current < 0 or current > 65535:
                # Range invalid; raise error
                raise ValueError("current out of range: " + str(current))

            # We don't really care about the double-octets; they need to
            #  be split in half and stored as individual bytes. Use bitwise
            #  operations to complete this

            # Clear the high order 8 bits by ANDing with 0000000011111111
            currentLowOrder8bits = current & 255

            # Right shift all of the bits 8 places to get the high order 8 bits
            currentHighOrder8bits = current >> 8

            # Run another set of sanity checks to ensure the values are valid
            if currentLowOrder8bits < 0 or currentLowOrder8bits > 255:
                raise ValueError(
                    "currentLowOrder8bits out of range: "
                    + str(currentLowOrder8bits)
                )

            if currentHighOrder8bits < 0 or currentHighOrder8bits > 255:
                raise ValueError(
                    "currentHighOrder8bits out of range: "
                    + str(currentHighOrder8bits)
                )

            # Ranges are valid; add them to list
            integerOctets.append(currentHighOrder8bits)
            integerOctets.append(currentLowOrder8bits)

        # Final sanity check; there should be exactly 16 octets in the list
        if len(integerOctets) != 16:
            raise ValueError(
                "len( integerOctets ) is not 16:" + str(len(integerOctets))
            )

        # Return the list of integer octets after parsing.
        #  This typically will be returned to the parent's constructor
        return integerOctets

    # Returns the host length of a given address. In this case, it
    #  is 128 minus the prefix length, which identifies how many
    #  bits are used for the host address
    def getHostLen(self):
        return 128 - self.getAddrLen()

    # Return the IPv6 address in fully extended EUI format
    # (xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx)
    def toString(self):

        # Start with an empty string
        octetLength = len(self._octet)
        ipv6String = ""

        # Iterate over all of the octets
        for i in range(0, octetLength):

            # Build the octet in "xx" format an append it to the main string
            ipv6String += str(hex(self._octet[i])[2:].zfill(2))

            # Be sure to add the colon every other time an octet is added
            #  The only exception is not adding a trailing colon
            if i % 2 == 1 and (i < octetLength - 1):
                ipv6String += ":"

        return ipv6String

    # Test for unicast addressing; returns true if the first octet is not 0xFF
    def isUnicast(self):
        return self._octet[0] != 0xFF

    # Test for multicast addressing; returns true if the first octet is 0xFF
    def isMulticast(self):
        return self._octet[0] == 0xFF

    # Test for 6to4 tunneling; returns true if the first 2 octets are 0x2001
    def is6to4(self):
        return self._octet[0] == 0x20 and self._octet[1] == 0x02

    # Test for unique local addressing (ULA), used for intranets
    #  Returns true if the first otet is 0xFEBF through 0xFEBF (FE80::/10)
    def isLinkLocalAddress(self):
        return (
            self._octet[0] == 0xFE
            and self._octet[1] >= 0x80
            and self._octet[1] <= 0xBF
        )

    # Test for link local addressing (LLA), used for link-level communications
    #  Returns true if the first otet is 0xFC or 0xFD (FC00::/7)
    def isUniqueLocalAddress(self):
        return self._octet[0] == 0xFC or self._octet[0] == 0xFD
