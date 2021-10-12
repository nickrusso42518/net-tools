#!/usr/bin/python

###############################################################################
# File: MACAddress.py
# Author: Nicholas Russo
# Description: This file includes a class that represents a MAC address.
#  Specific MAC operations, such as testing unicast/multicast or printing
#  string versions of the address are supported. More basic operations such as
#  retrieving an octet or measuring the number of octets are defined in the
#  parent class (NetAddress).
###############################################################################

from NetAddress import NetAddress

# Defines a MAC address, inheriting from NetAddress
class MACAddress(NetAddress):

    # Invokes the parent constructor to build the network address, which
    #  performs most of the heavy lifting. Performs upper-bound checking
    #  on the address length to ensure it is not greater than 48. Note
    #  that the parent constructor performs lower-bound checking already.
    #  MAC addresses typically don't have "address lengths", but by
    #  inheritance, it is supported anyway.
    def __init__(self, inputString, addrLen=48):
        if addrLen > 48:
            raise ValueError("addrLen is greater than 48: " + str(addrLen))

        NetAddress.__init__(self, inputString, addrLen)

    # Implements the abstract method defined in NetAddress. Breaks an
    #  EUI-formatted MAC address into a list of 6 integers; this
    #  list is returned from the method
    def _parseInputString(self, inputString):

        # Split the input string into 6 separate octets; any errors
        #  raised by this method are passed up the recursion stack
        ipStringOctets = self._splitInputString(inputString, ":", 6)

        # Iterate over all of the substrings, which should be
        #  8-bit unsigned integers
        integerOctets = []
        for ipStringOctet in ipStringOctets:

            # Test for valid range 0 <= x <= 255
            current = int(ipStringOctet, 16)
            if current < 0 or current > 255:
                # Range invalid; raise error
                raise ValueError("current out of range: " + str(current))

            # Range valid; add current to list
            integerOctets.append(current)

        # Final sanity check; there should be exactly 4 octets in the list
        if len(integerOctets) != 6:
            raise ValueError(
                "len( integerOctets ) is not 6:" + str(len(integerOctets))
            )

        # Return the list of integer octets after parsing.
        #  This typically will be returned to the parent's constructor
        return integerOctets

    # Returns the host length of a given address. In this case, it
    #  is 48 minus the prefix length, which identifies how many
    #  bits are used for the host address
    def getHostLen(self):
        return 48 - self.getAddrLen()

    # Return the MAC address in EUI format (xx:xx:xx:xx:xx:xx)
    def toString(self):

        # Start with an empty string
        macString = ""
        macStringLen = len(self._octet)

        # Iterate over all of the octets
        for i in range(0, macStringLen):

            # Build the octet in "xx" format an append it to the main string
            macString += str(hex(self._octet[i])[2:].zfill(2))

            # Be sure to add the colon every time an octet is added
            #  The only exception is not adding a trailing colon
            if i < (macStringLen - 1):
                macString += ":"

        return macString

    # Return the MAC address in Cisco format (xxxx.xxxx.xxxx)
    def toStringCisco(self):

        # Start with an empty string
        octetLength = len(self._octet)
        macString = ""

        # Iterate over all of the octets
        for i in range(0, octetLength):

            # Build the octet in "xx" format an append it to the main string
            macString += str(hex(self._octet[i])[2:].zfill(2))

            # Be sure to add the period every other time an octet is added
            #  The only exception is not adding a trailing period
            if i % 2 == 1 and (i < octetLength - 1):
                macString += "."

        return macString

    # Defines the action taken when this object is treated like a string.
    #  In this case, invokes the toString() method
    def __str__(self):
        return self.toString()

    # Return true if the seventh bit of the first byte is set
    def isULset(self):
        return self._isBitset(6, 0)

    # Return true if the eigth bit of the first byte is set
    def isIGset(self):
        return self._isBitset(7, 0)

    # Test for multicast MAC addressing (I/G clear)
    def isUnicast(self):
        return not self.isIGset()

    # Test for multicast MAC addressing (I/G set)
    def isMulticast(self):
        return self.isIGset()
