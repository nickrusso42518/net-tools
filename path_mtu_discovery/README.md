# Path MTU Discovery
This directory contains a script that can discovery the Maximum
Transmission Unit (MTU) along a routed path even when ICMP unreachables
are disabled in the network. It uses a modified binary search algorithm
and supports both IPv4 and IPv6.

## Operations
The script uses "sane defaults" and has 6 self-explanatory modifiers:

```
$ python pmtud.py
Script inputs:
  - lower: 1280
  - upper: 9000
  - retry: 1
  - timeout: 1
  - expected_mtu: 0
  - dest_ip: 8.8.8.8

MTU 5140 (lower 1280 / upper 9000) ... FAIL!
MTU 3209 (lower 1280 / upper 5139) ... FAIL!
MTU 2244 (lower 1280 / upper 3208) ... FAIL!
MTU 1761 (lower 1280 / upper 2243) ... FAIL!
MTU 1520 (lower 1280 / upper 1760) ... FAIL!
MTU 1399 (lower 1280 / upper 1519) ... OK!
MTU 1459 (lower 1400 / upper 1519) ... OK!
MTU 1489 (lower 1460 / upper 1519) ... OK!
MTU 1504 (lower 1490 / upper 1519) ... FAIL!
MTU 1496 (lower 1490 / upper 1503) ... OK!
MTU 1500 (lower 1497 / upper 1503) ... OK!
MTU 1502 (lower 1501 / upper 1503) ... FAIL!
MTU 1501 (lower 1501 / upper 1501) ... FAIL!
FINAL MTU: 1500 bytes

$ echo $?
0
```

You can adjust any or all of the modifiers using the syntax below. Note that
when the `expected_mtu` is 0, the script always returns 0 (success) if the
discovery process completes without raising any exceptions. When the
`expected_mtu` is non-zero, the specified value is compared to the discovered
MTU for equality. If they match, the script returns 0 (success).

```
$ python pmtud.py -d 8.8.4.4 -l 1402 -u 1549 -r 2 -t 2 -e 1500
Script inputs:
  - lower: 1402
  - upper: 1549
  - retry: 2
  - timeout: 2
  - expected_mtu: 1500
  - dest_ip: 8.8.4.4

MTU 1475 (lower 1402 / upper 1549) ... OK!
MTU 1512 (lower 1476 / upper 1549) .... FAIL!
MTU 1493 (lower 1476 / upper 1511) ... OK!
MTU 1502 (lower 1494 / upper 1511) .... FAIL!
MTU 1497 (lower 1494 / upper 1501) ... OK!
MTU 1499 (lower 1498 / upper 1501) ... OK!
MTU 1500 (lower 1500 / upper 1501) ... OK!
MTU 1501 (lower 1501 / upper 1501) .... FAIL!
FINAL MTU: 1500 bytes

$ echo $?
0
```

If the expected MTU does not match the discovered MTU, the script returns 1,
which signals a failure to your CI system. The script also prints an
additional line of output to indicate this mismatch for human confirmation.

```
$ python pmtud.py -d 8.8.4.4 -l 1402 -u 1549 -r 2 -t 2 -e 1499
Script inputs:
  - lower: 1402
  - upper: 1549
  - retry: 2
  - timeout: 2
  - expected_mtu: 1499
  - dest_ip: 8.8.4.4

MTU 1475 (lower 1402 / upper 1549) ... OK!
MTU 1512 (lower 1476 / upper 1549) .... FAIL!
MTU 1493 (lower 1476 / upper 1511) ... OK!
MTU 1502 (lower 1494 / upper 1511) .... FAIL!
MTU 1497 (lower 1494 / upper 1501) ... OK!
MTU 1499 (lower 1498 / upper 1501) ... OK!
MTU 1500 (lower 1500 / upper 1501) ... OK!
MTU 1501 (lower 1501 / upper 1501) .... FAIL!
FINAL MTU: 1500 bytes
** 1500 does not match expected MTU of 1499

$ echo $?
1
```

## Caveats
Some operating systems will not allow `scapy` to forge packets unless
they have administrator/super-user permissions. Also, `scapy` will
internally `raise` and `except` its own exceptions, so a script may
continue to run even as errors are occurring. This is rare and is
usually related to an IPv6 RA containing an MTU value and the script
trying to exceed that value. You can overcome this by setting a lower
`upper` value.

## Testing
A GNU `Makefile` is used to automate testing with the following targets:
  * `lint`: Runs `yamllint` and `pylint` linters, and the `black` formatter
  * `run4`: Performs test runs on IPv4 destinations
  * `run6`: Performs test runs on IPv6 destinations
  * `run`: Performs test runs on IPv4 and IPv6 destinations
  * `clean`: Deletes all `.pyc` files from this project
  * `all`: Default target that runs the sequence `clean lint run`
