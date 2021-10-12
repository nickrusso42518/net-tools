#!/usr/bin/python

###############################################################################
# File: IPv6Address_Test.py
# Author: Nicholas Russo
# Description: This file includes a class that represents a test case specific
#  to IPv6 addressing. Each of the methods defined in IPv6Address are tested
#  here. This is meant to serve as a regression test for that class.
###############################################################################

from NetAddress_Test import NetAddress_Test
from IPv6Address import IPv6Address
import unittest

# Defines an IPv6 address test case, inheriting from NetAddress test case
class IPv6Address_Test(NetAddress_Test):

    # Invokes the static method defined in NetAddress_Test to build a test suite
    #  Effectively, this just passes up the class name to the parent.
    @staticmethod
    def buildTestSuite():
        return NetAddress_Test.buildTestSuite(IPv6Address_Test)

    # Implements the abstract method defined in NetAddress_Test to add a pool
    #  of IPv6 addresses for testing.
    def populateNetAddressList(self):
        self.getNetAddressList().append(
            IPv6Address("2001:0db8:0000:0000:0004:0003:0002:0001", 64)
        )
        self.getNetAddressList().append(
            IPv6Address("FF00:0000:0000:0000:0000:0000:0000:0001")
        )
        self.getNetAddressList().append(
            IPv6Address("FF00:0000:0000:0000:0000:000a:000b:000c", 0)
        )
        self.getNetAddressList().append(
            IPv6Address("2002:beef:cafe:0000:0000:0000:0000:0001", 40)
        )
        self.getNetAddressList().append(
            IPv6Address("FD00:0000:0000:0000:0000:0000:0000:0001", 80)
        )
        self.getNetAddressList().append(
            IPv6Address("FEAA:0000:0000:0000:0000:000a:000b:000c", 96)
        )

    # Performs a general constructor test to ensure it can tolerate invalid
    #  inputs by raising the proper errors. This is not specific to a method
    #  offered by the class but is required to be implemented by the base class
    def test_invalidInstances(self):

        # Build tuples of invalid input strings and address lengths
        bogusInputStrings = (
            None,
            "",
            "clown",
            "2001:0db8:0000:0000:0000:0000:0000"
            "2001:0db8:0000:0000:0000:0000:0000:"
            "2001:0db8:0000:0000:0000:0000:0000:0000:FFFF",
            "2001:0db8:0000:0000:0000:0000:0000:-1",
            "2001:0db8:0000:0000:0000:0000:0000:GGGG",
        )

        bogusAddrLens = (-1, 129)

        # Iterate over the list of invalid input strings
        for bogusInputString in bogusInputStrings:
            try:
                # Attempt to build the object
                IPv6Address(bogusInputString)

                # If the loop completes successfully, an error was not raised
                #  which is indicative of a test failure
                isErrorRaised = False

            except (AttributeError, ValueError) as e:
                # Error was raised; this is expected
                isErrorRaised = True

            finally:
                # Ensure the error was raised
                self.assertTrue(isErrorRaised)

        # Iterate over the list of invalid address lengths
        for bogusAddrLen in bogusAddrLens:
            try:
                # Attempt to build the object
                IPv6Address(
                    "2001:0db8:0000:0000:0000:0000:0000:0000", bogusAddrLen
                )

                # If the loop completes successfully, an error was not raised
                #  which is indicative of a test failure
                isErrorRaised = False

            except ValueError:
                # Error was raised; this is expected
                isErrorRaised = True

            finally:
                # Ensure the error was raised
                self.assertTrue(isErrorRaised)

    # Tests the isUnicast() function within the IPv6Address class.
    #  The method under test returns true if the IPv6 address is unicast.
    def test_isUnicast(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) >= 0x1 and ip.getOctet(1) <= 0xFE:
                self.assertTrue(ip.isUnicast())
            else:
                self.assertFalse(ip.isUnicast())

    # Tests the isMulticast() function within the IPv6Address class
    #  The method under test returns true if the IPv6 address is multicast.
    def test_isMulticast(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) == 0xFF:
                self.assertTrue(ip.isMulticast())
            else:
                self.assertFalse(ip.isMulticast())

    # Tests the is6to4() function within the IPv6Address class
    #  The method under test returns true if the IPv6 address begins
    #  with 0x2002, which is reserved for 6to4 tunneling
    def test_is6to4(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) == 0x20 and ip.getOctet(2) == 0x02:
                self.assertTrue(ip.is6to4())
            else:
                self.assertFalse(ip.is6to4())

    # Tests the isLinkLocalAddress() function within the IPv6Address class
    #  The method under test returns true if the IPv6 address begins
    #  is within FE80::/10 (0xFE80 - 0xFEBF in the first 2 octets)
    def test_isLinkLocalAddress(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) == 0xFE and (
                ip.getOctet(2) >= 0x80 and ip.getOctet(2) <= 0xBF
            ):
                self.assertTrue(ip.isLinkLocalAddress())
            else:
                self.assertFalse(ip.isLinkLocalAddress())

    # Tests the isUniqueLocalAddress() function within the IPv6Address class
    #  The method under test returns true if the IPv6 address begins
    #  is within FC00::/7 (0xFC or 0xFD in the first octet)
    def test_isUniqueLocalAddress(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) == 0xFC or ip.getOctet(1) == 0xFD:
                self.assertTrue(ip.isUniqueLocalAddress())
            else:
                self.assertFalse(ip.isUniqueLocalAddress())

    # Tests the toString() function within the IPv6Address class
    #  The method under test returns a string representation of the IPv6
    #  address in fully extended EUI format
    #  (xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx)
    def test_toString(self):
        for ip in self.getNetAddressList():

            # Convert the IP address to a string, then split it using
            #  the colon ":" character as a delimiter. The result is
            #  a list of 8 double-octets (16 octets total)
            ipString = ip.toString()
            ipStringOctets = ipString.split(":")

            # There should be exactly 8 double-octets in the address
            self.assertTrue(len(ipStringOctets) == 8)

            # Iterate over all of the octets generated by toString()
            #  that were split apart. Compare those to the actual integer
            #  octets within the IP address; everything should match
            i = 1
            for ipStringOctet in ipStringOctets:

                # Break the double-octet into two individual octets
                #  (e.g. split "2001" into "20" and "01")
                #  Then, convert the first and second halves into hex integers
                firstHalfHex = int(ipStringOctet[:2], 16)
                secondHalfHex = int(ipStringOctet[2:], 16)

                # Ensure the parsed octets match the values in memory
                self.assertTrue(firstHalfHex == ip.getOctet(i))
                self.assertTrue(secondHalfHex == ip.getOctet(i + 1))

                # Increment the iterator by 2 since two assertions are
                #  performed on each double-octet (one per octet)
                i += 2
