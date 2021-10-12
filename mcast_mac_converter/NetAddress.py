#!/usr/bin/python

###############################################################################
# File: NetAddress.py
# Author: Nicholas Russo
# Description: This file includes a class that represents a generic network
#  address. Basic operations such as retrieving an octet or measuring the
#  number of octets are defined here. Specific implementations of network
#  addresses can use these basic functions.
###############################################################################

import abc

# Defines a generic network address object
class NetAddress(object):
    __metaclass__ = abc.ABCMeta

    # Constructor stores each byte separately in an array after parsing the
    #  input string according to a child-defined method. Perform lower-bound
    #  error-checking on the address length to ensure it is non-negative.
    def __init__(self, inputString, addrLen):
        self._octet = self._parseInputString(inputString)
        if addrLen < 0:
            raise ValueError("addrLen is negative: " + str(addrLen))
        self._addrLen = addrLen

    # Consumes the "inputString" parameter and turns it into a list of octets
    #  for use with arithmetic functions. Implemented by child classes since
    #  network addresses have variable formatting
    @abc.abstractmethod
    def _parseInputString(self, inputString):
        return

    # Splits the specified string "inputString" using delimeter "delim"
    #  and expects to see a list of strings of length "numOctets". This
    #  method includes built-in error checking for null references
    #  and malformed network addresses. Child constructors can use this
    #  to validate input before building the objects. Method returns
    #  the list of substrings, assuming there are no errors.
    def _splitInputString(self, inputString, delim, numOctets):

        # Test for a null reference; raise error
        if inputString is None or len(inputString) == 0:
            raise AttributeError("inputString is None or empty")

        # Split the string into pieces based on
        stringOctets = inputString.split(delim)

        # There should be exactly "numOctets" octets in the address
        if len(stringOctets) != numOctets:
            raise ValueError(
                "Incorrect number of octets: " + str(len(stringOctets))
            )

        # Method success; return the list of substrings
        return stringOctets

    # If a valid index, return the non-canonically referenced result
    def getOctet(self, octet):

        # Test validity of the octet index
        if octet >= 1 and octet <= len(self._octet):
            return self._octet[octet - 1]
        else:
            # Index out of bounds condition, return -1 to signal error
            # TODO: Could raise an error alternatively
            return -1

    def _setOctet(self, octet, value):

        # Test validity of the octet index and the value.
        #  If either is invalid, make no change.
        if (octet >= 1 and octet <= len(self._octet)) and (
            value >= 0 and value <= 255
        ):
            self._octet[octet - 1] = value

    # Returns the address length (aka prefix length) of the given address
    def getAddrLen(self):
        return self._addrLen

    # Returns the last host address in the subnet, effectively the same
    #  as getNetwork() except with all 1s in the host address TODO
    def getEndOfSubnet(self):
        raise NotImplementedError()

    # Returns the beginning of the network range (the "network")
    #  based on the address length (e.g. 10.4.6.68/28 -> 10.4.6.64/28)
    def getNetwork(self):

        # Create a copy of the original object for modification
        prefix = self

        # Determine the number of octets to totally clear; this simplifies
        #  operations since we don't have to iterate over bits if the
        #  entire byte needs to be zero
        octetsToClear = self.getHostLen() / 8
        for i in range(octetsToClear, 0, -1):
            prefix._setOctet((len(self) + 1) - i, 0)

        # If all octets were cleared completely, the addrLen was 0
        #  so there is nothing more to do. Return now to avoid errors
        if octetsToClear > len(self) - 1:
            return prefix

        # Identify the current octet where further bitwise clearing
        #  may need to be done
        currentOctet = len(self) - octetsToClear

        # Find the remainder of bits not cleanly divisible by 8 where
        #  manual iteration over the bits is necessary in a given byte
        remainingBitsToClear = self.getHostLen() % 8

        # Raise 2^bits and end up with a number 1<=x<=2^(maxPrefLen)
        #  Subtracting 1 reveals the bits that need to be cleared.
        #  Currently the mask is the opposite of what we need it to be, so
        #  use XOR to flip the bits by XOR'ing with all ones (11111111)
        mask = (pow(2, remainingBitsToClear) - 1) ^ 0xFF

        # At this point, the mask should be something like 11110000 where
        #  the ones are contiguous on the left and zeroes are contiguous
        #  on the right. Perform bitwise AND to clean low-order bits
        # prefix._octet[ currentOctet - 1 ] = self.getOctet( currentOctet ) & mask
        prefix._setOctet(currentOctet, self.getOctet(currentOctet) & mask)

        # Return the network prefix; note that "self" was never modified
        return prefix

    # Returns the host length of a given address
    @abc.abstractmethod
    def getHostLen(self):
        return

    # Return true if the "bitIndex" bit of the "byteIndex" byte is set
    # The parameters must be canonical (bits 0-7, bytes 0-5)
    def _isBitset(self, bitIndex, byteIndex):
        byteValue = self._octet[byteIndex]
        bitValue = pow(2, 7 - bitIndex)
        return byteValue & bitValue == bitValue

    # Implements the len() function for a NetAddress by returning
    #  the number of octets (bytes) in the address
    def __len__(self):
        return len(self._octet)

    # Return the network address in an easy-to-read format.
    #  Note that some protocols may have multiple accesspable types
    #  of human-readable representations, but at a minimum, one must
    #  be implemented by every child class
    @abc.abstractmethod
    def toString(self):
        return

    # Defines the action taken when this object is treated like a string.
    #  In this case, invokes the abstract toString() method implemented
    #  in the child classes.
    def __str__(self):
        return self.toString()

    # Test for unicast addressing; returns true if the address is unicast
    @abc.abstractmethod
    def isUnicast(self):
        return

    # Test for multicast addressing; returns true if the address is multicast
    @abc.abstractmethod
    def isMulticast(self):
        return
