#!/usr/bin/python

###############################################################################
# File: IPv4Address_Test.py
# Author: Nicholas Russo
# Description: This file includes a class that represents a test case specific
#  to IPv4 addressing. Each of the methods defined in IPv4Address are tested
#  here. This is meant to serve as a regression test for that class.
###############################################################################

from NetAddress_Test import NetAddress_Test
from IPv4Address import IPv4Address
import unittest

# Defines an IPv4 address test case, inheriting from NetAddress test case
class IPv4Address_Test(NetAddress_Test):

    # Invokes the static method defined in NetAddress_Test to build a test suite
    #  Effectively, this just passes up the class name to the parent.
    @staticmethod
    def buildTestSuite():
        return NetAddress_Test.buildTestSuite(IPv4Address_Test)

    # Implements the abstract method defined in NetAddress_Test to add a pool
    #  of IPv4 addresses for testing.
    def populateNetAddressList(self):
        self.getNetAddressList().append(IPv4Address("1.2.3.4", 32))
        self.getNetAddressList().append(IPv4Address("223.20.30.40", 24))
        self.getNetAddressList().append(IPv4Address("224.17.24.17", 16))
        self.getNetAddressList().append(IPv4Address("239.7.5.16", 8))
        self.getNetAddressList().append(IPv4Address("255.239.238.237", 0))
        self.getNetAddressList().append(IPv4Address("20.54.55.68", 22))
        self.getNetAddressList().append(IPv4Address("20.54.55.68", 28))
        self.getNetAddressList().append(IPv4Address("20.54.55.68", 11))
        self.getNetAddressList().append(IPv4Address("20.54.55.68", 4))

    # Performs a general constructor test to ensure it can tolerate invalid
    #  inputs by raising the proper errors. This is not specific to a method
    #  offered by the class but is required to be implemented by the base class
    def test_invalidInstances(self):

        # Build tuples of invalid input strings and address lengths
        bogusInputStrings = (
            None,
            "",
            "clown",
            "1",
            "1.2",
            "1.2.3",
            "1.2.3.",
            "1.2.3.256",
            "1.2.-3.0",
        )

        bogusAddrLens = (-1, 33)

        # Iterate over the list of invalid input strings
        for bogusInputString in bogusInputStrings:
            try:
                # Attempt to build the object
                IPv4Address(bogusInputString)

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
                IPv4Address("1.2.3.4", bogusAddrLen)

                # If the loop completes successfully, an error was not raised
                #  which is indicative of a test failure
                isErrorRaised = False

            except ValueError:
                # Error was raised; this is expected
                isErrorRaised = True

            finally:
                # Ensure the error was raised
                self.assertTrue(isErrorRaised)

    # Tests the isUnicast() function within the IPv4Address class.
    #  The method under test returns true if the IPv4 address is unicast.
    def test_isUnicast(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) >= 1 and ip.getOctet(1) <= 223:
                self.assertTrue(ip.isUnicast())
            else:
                self.assertFalse(ip.isUnicast())

    # Tests the isMulticast() function within the IPv4Address class
    #  The method under test returns true if the IPv4 address is multicast.
    def test_isMulticast(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) >= 224 and ip.getOctet(1) <= 239:
                self.assertTrue(ip.isMulticast())
            else:
                self.assertFalse(ip.isMulticast())

    # Tests the isExperimental() function within the IPv4Address class
    #  The method under test returns true if the IPv4 address is experimental.
    def test_isExperimental(self):
        for ip in self.getNetAddressList():
            if ip.getOctet(1) >= 240 and ip.getOctet(1) <= 255:
                self.assertTrue(ip.isExperimental())
            else:
                self.assertFalse(ip.isExperimental())

    # Tests the toString() function within the IPv4Address class
    #  The method under test returns a string representation of the IPv4
    #  address in dotted-decimal format (xx.xx.xx.xx)
    def test_toString(self):
        for ip in self.getNetAddressList():

            # Convert the IP address to a string, then split it using
            #  the period "." character as a delimiter. The result is
            #  a list of 4 octets.
            ipString = ip.toString()
            ipStringOctets = ipString.split(".")

            # There should be exactly 4 octets in the address
            self.assertTrue(len(ipStringOctets) == 4)

            # Iterate over all of the octets generated by toString()
            #  that were split apart. Compare those to the actual integer
            #  octets within the IP address; everything should match
            i = 1
            for ipStringOctet in ipStringOctets:
                self.assertTrue(int(ipStringOctet) == ip.getOctet(i))
                i += 1

    # Tests the toStringHex() function within the IPv4Address class
    #  The method under test returns a string representation of the IPv4
    #  address in contiguous hex format with the leading "0x" (0xaabbccdd)
    def test_toStringHex(self):
        for ip in self.getNetAddressList():

            # Convert the IP address to a string, then break it apart
            #  into 4 separate octets stored separately. The result is
            #  a list of 4 strings. The leading "0x" is removed.
            ipString = ip.toStringHex()

            # Ensure the string begins with "0x"
            self.assertTrue(ipString[:2] == "0x")

            # Remove the leading "0x" to evaluate the octets
            #  There should be exactly 8 remaining characters in the string
            ipString = ipString[2:]
            self.assertTrue(len(ipString) == 8)

            # Store each octet in a list of 2-character strings
            ipStringOctets = [
                ipString[:2],
                ipString[2:4],
                ipString[4:6],
                ipString[6:],
            ]

            # Iterate over all of the octets generated by toString()
            #  that were split apart. Compare those to the actual integer
            #  octets within the IP address; everything should match
            i = 1
            for ipStringOctet in ipStringOctets:

                # Sanity check; ensure each element in the list is exactly 2
                #  characters in length
                self.assertTrue(len(ipStringOctet) == 2)

                # Ensure the integer version of the string equals the integer
                #  currently stored in memory
                self.assertTrue(int(ipStringOctet, 16) == ip.getOctet(i))
                i += 1
