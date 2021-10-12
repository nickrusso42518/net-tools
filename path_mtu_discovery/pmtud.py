#!/usr/bin/env python

"""
Author: Nick Russo (njrusmc@gmail.com)
Purpose: Discover the Maximum Transmission Unit (MTU) towards a
specified destination IPv4 or IPv6 address. This does not rely on
ICMP unreachables and should work in any environment where the
target responds to ICMP echo-requests and where the transport
network allows the transmission of ping traffic.
"""


import argparse
import sys
from scapy.packet import Raw
from scapy.layers.inet import IP, ICMP
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest
from scapy.sendrecv import sr1


def find_mtu(lower, upper, retry, timeout, dest_ip):
    """
    Recursive binary search implementation to MTU towards the
    "dest_ip" target address. The "lower" and "upper" integer inputs
    bound the algorithm and can be tuned for better performance.
    The "retry" and "timeout" integer inputs govern how many packets
    to send and how long to wait for a response, respectively.
    """

    # Base case; when upper exceeds lower, we are done
    if upper < lower:
        return upper

    # Compute midpoint value with floor division
    mid = (upper + lower) // 2
    print(f"MTU {mid} (lower {lower} / upper {upper}) ..", end="", flush=True)

    # Send ICMP echo-request (ping) and await a single echo-reply
    for _ in range(retry):
        pkt = _make_ping(dest_ip, mid)
        print(".", end="", flush=True)
        resp = sr1(pkt, verbose=0, timeout=timeout)
        if resp is not None:
            break

    # Received echo-reply; search between mid and upper (MTU must be bigger)
    if resp is not None and _is_icmp_echo_reply(resp):
        print(" OK!")
        return find_mtu(mid + 1, upper, retry, timeout, dest_ip)

    # No echo-reply; search between low and mid (MTU must be smaller)
    print(" FAIL!")
    return find_mtu(lower, mid - 1, retry, timeout, dest_ip)


def _is_icmp_echo_reply(resp):
    """
    Returns true if the response packet is an IPv4 or IPv6 ICMP echo-reply.
    Also, it tests to ensure the "More Fragments" flag is unset. Some IP stacks
    incorrectly ignore the "Don't Fragment" flag and will fragment anyway,
    creating a false positive. For IPv6, ensure that the next-hop is ICMPv6
    (58) and not a Fragment Header (44).
    """

    if resp.version == 4:
        return resp.type == 0 and resp.code == 0 and resp.flags & 0x1 == 0

    if resp.version == 6:
        return resp.type == 129 and resp.code == 0 and resp.nh == 58

    raise ValueError(f"Invalid IP version: {resp.version}")


def _make_ping(dest_ip, mid):
    """
    Given a destination IP address and midpoint (MTU) value, construct
    either an IPv4 or IPv6 ICMP echo-request. The total IP packet size
    is guaranteed to be equal to the midpoint value to ensure an
    accurate MTU test. The payload of each packet is padded with the
    ASCII letter "M" to signify MTU discovery, making these packets easier
    to identify when capturing packets to troubleshoot.
    """

    # If the dest_ip contains a colon, it must be IPv6 (40 IPv6 + 8 ICMP)
    if ":" in dest_ip:
        pkt = IPv6(dst=dest_ip) / ICMPv6EchoRequest(data="M" * (mid - 48))

    # No colon in dest_ip; assume it is IPv4 (20 IPv4 + 8 ICMP)
    else:
        pkt = IP(dst=dest_ip, flags=0x2) / ICMP() / Raw("M" * (mid - 28))

    # Perform packet size sanity check and return packet
    assert len(pkt) == mid
    return pkt


def _process_args():
    """
    Process command line arguments. The default values are listed in the code
    and are accessible using "-h". Note that the default "lower" value is
    1280, the minimum IPv6 MTU. If you want to test MTUs smaller than this
    for IPv4 (minimum 576), you must specify it manually. An "expected_mtu"
    value of 0 disables post-discovery MTU verification, which is often only
    useful for CI testing to trigger failures in validation environments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--lower", type=int, help="lower bound MTU in bytes", default=1280
    )
    parser.add_argument(
        "-u", "--upper", type=int, help="upper bound MTU in bytes", default=9000
    )
    parser.add_argument(
        "-r", "--retry", type=int, help="per-MTU probe retries", default=1
    )
    parser.add_argument(
        "-t", "--timeout", type=int, help="probe timeout in seconds", default=1
    )
    parser.add_argument(
        "-e", "--expected_mtu", type=int, help="MTU value to verify", default=0
    )
    parser.add_argument(
        "-d", "--dest_ip", type=str, help="target IPv4/v6", default="8.8.8.8"
    )
    return parser.parse_args()


if __name__ == "__main__":

    # Process CLI arguments and display them in dictionary form
    dict_args = vars(_process_args())
    print("Script inputs:")
    for key, value in dict_args.items():
        print(f"  - {key}: {value}")
    print()

    # Discover and display the final MTU
    expected_mtu = dict_args.pop("expected_mtu")
    mtu = find_mtu(**dict_args)
    print(f"FINAL MTU: {mtu} bytes")

    # If an expected value was specified, perform comparison
    if expected_mtu > 0 and expected_mtu != mtu:
        print(f"** {mtu} does not match expected MTU of {expected_mtu}")
        sys.exit(1)
