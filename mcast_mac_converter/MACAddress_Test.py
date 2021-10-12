#!/usr/bin/python

###############################################################################
# File: MACAddress_Test.py
# Author: Nicholas Russo
# Description: This file includes a class that represents a test case specific
#  to MAC addressing. Each of the methods defined in MACAddress are tested
#  here. This is meant to serve as a regression test for that class.
###############################################################################

from NetAddress_Test import NetAddress_Test
from MACAddress import MACAddress
import unittest

# Defines an MAC address test case, inheriting from NetAddress test case
class MACAddress_Test(NetAddress_Test):

    # Invokes the static method defined in NetAddress_Test to build a test suite
    #  Effectively, this just passes up the class name to the parent.
    @staticmethod
    def buildTestSuite():
        return NetAddress_Test.buildTestSuite(MACAddress_Test)

    # Implements the abstract method defined in NetAddress_Test to add a pool
    #  of MAC addresses for testing.
    def populateNetAddressList(self):
        self.getNetAddressList().append(MACAddress("01:22:33:44:55:66", 0))
        self.getNetAddressList().append(MACAddress("03:22:33:44:55:FF", 24))
        self.getNetAddressList().append(MACAddress("00:22:33:44:55:66", 28))
        self.getNetAddressList().append(MACAddress("FF:FF:FF:FF:FF:FF"))

    # Performs a general constructor test to ensure it can tolerate invalid
    #  inputs by raising the proper errors. This is not specific to a method
    #  offered by the class but is required to be implemented by the base class
    def test_invalidInstances(self):

        # Build tuples of invalid input strings and address lengths
        bogusInputStrings = (
            None,
            "",
            "clown",
            "01:22:33:44:55",
            "01:22:33:44:55:",
            "01:22:33:44:55:66:77",
            "01:22:33:44:55:-1",
            "01:22:33:44:55:gg",
        )

        bogusAddrLens = (-1, 49)

        # Iterate over the list of invalid input strings
        for bogusInputString in bogusInputStrings:
            try:
                # Attempt to build the object
                MACAddress(bogusInputString)

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
                MACAddress("11:22:#3:44:55:66", bogusAddrLen)

                # If the loop completes successfully, an error was not raised
                #  which is indicative of a test failure
                isErrorRaised = False

            except ValueError:
                # Error was raised; this is expected
                isErrorRaised = True

            finally:
                # Ensure the error was raised
                self.assertTrue(isErrorRaised)

    # Tests the isUnicast() function within the MACAddress class.
    #  The method under test returns true if the MAC address is unicast.
    def test_isUnicast(self):
        for mac in self.getNetAddressList():
            if mac.getOctet(1) & 1 == 0:
                self.assertTrue(mac.isUnicast())
            else:
                self.assertFalse(mac.isUnicast())

    # Tests the isMulticast() function within the MACAddress class
    #  The method under test returns true if the MAC address is multicast.
    def test_isMulticast(self):
        for mac in self.getNetAddressList():
            if mac.getOctet(1) & 1 == 1:
                self.assertTrue(mac.isMulticast())
            else:
                self.assertFalse(mac.isMulticast())

    # Tests the isIGset() function within the MACAddress class
    #  The method under test returns true if I/G bit is set
    #  The logic is effectively identical to isMulticast() since
    #  the I/G bit set indicates that a MAC address is multicast.
    def test_isIGset(self):
        for mac in self.getNetAddressList():
            if mac.getOctet(1) & 1 == 1:
                self.assertTrue(mac.isIGset())
            else:
                self.assertFalse(mac.isIGset())

    # Tests the isIGset() function within the MACAddress class
    #  The method under test returns true if U/L bit is set
    def test_isULset(self):
        for mac in self.getNetAddressList():
            if mac.getOctet(1) & 2 == 2:
                self.assertTrue(mac.isULset())
            else:
                self.assertFalse(mac.isULset())

    # Tests the toString() function within the MACAddress class
    #  The method under test returns a string representation of the MAC
    #  address in EUI format (xx:xx:xx:xx:xx:xx)
    def test_toString(self):
        for mac in self.getNetAddressList():

            # Convert the MAC address to a string, then split it using
            #  the colon ":" character as a delimiter. The result is
            #  a list of 6 octets.
            macString = mac.toString()
            macStringOctets = macString.split(":")

            # There should be exactly 6 octets in the address
            self.assertTrue(len(macStringOctets) == 6)

            # Iterate over all of the octets generated by toString()
            #  that were split apart. Compare those to the actual integer
            #  octets within the MAC address; everything should match
            i = 1
            for macStringOctet in macStringOctets:
                self.assertTrue(int(macStringOctet, 16) == mac.getOctet(i))
                i += 1

    # Tests the toStringCisco() function within the MACAddress class
    #  The method under test returns a string representation of the MAC
    #  address in Cisco format (xxxx.xxxx.xxxx)
    def test_toStringCisco(self):
        for mac in self.getNetAddressList():

            # Convert the MAC address to a string, then split it using
            #  the period "." character as a delimiter. The result is
            #  a list of 3 double-octets.
            macString = mac.toStringCisco()
            macStringOctets = macString.split(".")

            # There should be exactly 3 double-octets in the address
            self.assertTrue(len(macStringOctets) == 3)

            # Iterate over all of the octets generated by toString()
            #  that were split apart. Compare those to the actual integer
            #  octets within the IP address; everything should match
            i = 1
            for macStringOctet in macStringOctets:

                # Break the double-octet into two individual octets
                #  (e.g. split "2001" into "20" and "01")
                #  Then, convert the first and second halves into hex integers
                firstHalfHex = int(macStringOctet[:2], 16)
                secondHalfHex = int(macStringOctet[2:], 16)

                # Ensure the parsed octets match the values in memory
                self.assertTrue(firstHalfHex == mac.getOctet(i))
                self.assertTrue(secondHalfHex == mac.getOctet(i + 1))

                # Increment the iterator by 2 since two assertions are
                #  performed on each double-octet (one per octet)
                i += 2
