# Multicast IP to Multicast MAC Converter
This directory contains scripts to convert multicast IP addresses
into their corresponding multicast MAC addresses. It supports
both IPv4 and IPv6. Note: This is my very first Python project from years ago!

## Operations
Use the `mip2mac.py` script to convert IPv4 multicast addresses to
multicast MAC addresses. You must specify at least one IP address.

```
$ python mip2mac.py
Usage:   mip2mac mip1 mip2 mipn
Example: mip2mac 239.1.1.1 239.2.2.2

$ python mip2mac.py 239.1.1.1 239.2.2.2
01:00:5e:01:01:01
01:00:5e:02:02:02
```

IPv6 works similarly using the `mip2mac6.py` script. For both scripts, you can
use `xargs` to read IP addresses from a file for bulk processing.

```
$ cat mip2mac6.inputfile
ff00:0000:0000:0000:0000:0000:0000:0001
ff00:0000:0000:0000:0000:000a:000b:000c
ef00:0000:0000:0000:0000:0000:0000:0001
ff00:0000:0000:0000:0001:0000:0000:0001
ff00:0000:0000:0000:0000:ffff:abcd:ef21

$ cat mip2mac6.inputfile | xargs python mip2mac6.py
33:33:00:00:00:01
33:33:00:0b:00:0c
33:33:00:00:00:01
33:33:ab:cd:ef:21
```
