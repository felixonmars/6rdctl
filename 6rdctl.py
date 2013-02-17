#!/usr/bin/env python
from __future__ import unicode_literals
import socket
import fcntl
import struct
from sh import ip, ErrorReturnCode_1
from argparse import ArgumentParser


def get_ip_address(dev):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack(b'256s', dev.encode("utf8")[:15])
    )[20:24])


if __name__ == "__main__":
    parser = ArgumentParser(description="6rd Control Tool")
    parser.add_argument(
        '-d', '--delete',
        action="store_true",
        default=False,
        help="Remove the corresponding 6rd interface"
    )
    parser.add_argument(
        '-i', '--interface',
        nargs='?',
        default='eth0',
        help='WAN interface to use, default: eth0',
    )
    parser.add_argument(
        '-p', '--prefix',
        nargs='?',
        default='2001:e41',
        help='6rd prefix to use, default: 2001:e41'
    )
    parser.add_argument(
        '-r', '--router',
        nargs='?',
        default='61.211.224.125',
        help='6rd router to use, default: 61.211.224.125'
    )
    parser.add_argument(
        '--ip',
        nargs='?',
        default=None,
        help='Specify custom IP to use for calculating 6rd address, default: gather from WAN interface',
    )
    parser.add_argument(
        '--radvd',
        action="store_true",
        default=False,
        help="Change /etc/radvd.conf accordingly",
    )
    parser.add_argument(
        '--radvd-interface',
        nargs='?',
        default='eth1',
        help="LAN interface to use, default: eth1"
    )

    options = parser.parse_args()

    if not options.ip:
        options.ip = get_ip_address(options.interface)

    _6rd_interface = "6rd"

    address = options.prefix + ":{:02x}{:02x}:{:02x}{:02x}".format(*[int(x) for x in options.ip.split(".")]) + "::/"

    radvd_template = """
        interface %s {
        AdvSendAdvert on;
        MinRtrAdvInterval 1;
        MaxRtrAdvInterval 3;

        prefix %s64 {
            AdvOnLink on;
            AdvAutonomous on;
        };
    };
    """
    try:
        ip.tunnel("del", _6rd_interface)
    except ErrorReturnCode_1:
        pass

    if not options.delete:

        if options.radvd:
            with open("/etc/radvd.conf", "w") as f:
                f.write((radvd_template % (options.radvd_interface, address)).encode("utf8"))
                ip.addr.add(address + "64", "dev", options.radvd_interface)

        ip.tunnel.add(_6rd_interface, "mode", "sit", "local", get_ip_address(options.interface), "ttl", 64)
        ip.tunnel("6rd", "dev", _6rd_interface, "6rd-prefix", options.prefix + "::/32")
        ip.addr.add(address + "32", "dev", _6rd_interface)
        ip.link.set(_6rd_interface, "up")
        ip.route.add("::/0", "via", "::" + options.router, "dev", _6rd_interface)
