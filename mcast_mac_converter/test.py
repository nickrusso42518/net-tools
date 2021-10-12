#!/usr/bin/python

###############################################################################
# File: test.py
# Author: Nicholas Russo
# Description: This file can be executed from the CLI (python test.py) to
#  run all appropriate unit tests for all classes within this project. The
#  user can specify the TestRunner verbosity level as a CLI argument as well.
###############################################################################

from IPv4Address_Test import IPv4Address_Test
from IPv6Address_Test import IPv6Address_Test
from MACAddress_Test import MACAddress_Test
import unittest
import sys
import os

# Responsible for creating test-related objects and executing test suites
def test(args):

    # Determines how verbose to make the output from the test
    # 0 (quiet): you just get the total numbers of tests executed and the global result
    # 1 (default): you get the same plus a dot for every successful test or a F for every failure
    # 2 (verbose): you get the help string of every test and the result
    if len(args) < 2:
        # No argument supplied; assume default
        testVerbosity = 1
    else:
        # An argument was supplied; test for validity
        # If validity check fails, assume default
        try:
            testVerbosity = int(args[1].strip())
        except:
            testVerbosity = 1

    # Create a list of all test suites, typically one per network address test case
    testSuiteList = [
        IPv4Address_Test.buildTestSuite(),
        IPv6Address_Test.buildTestSuite(),
        MACAddress_Test.buildTestSuite(),
    ]

    # Create test runner to execute each test suite in series with the proper
    #  level of verbosity

    testRunner = unittest.TextTestRunner(verbosity=testVerbosity)

    # Iterate over all of the test suites, run each one in series
    for testSuite in testSuiteList:
        testRunner.run(testSuite)


###############################################################################
# Execution starts here; capture any command line arguments
###############################################################################
test(sys.argv)
