#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ARP Sweep with Scapy
- Sends an ARP Request to a broadcast address on a network (CIDR).
- Collects and parses the responses.
- Prints the IP and MAC addresses of active hosts.

Usage:
    sudo python3 arp_sweep.py -n 192.168.1.0/24 -i eth0 -t 2
"""

import sys
import os
import argparse

try:
    # Scapy provides network layers (Ether, ARP) and send/receive functions (srp)
    from scapy.all import Ether, ARP, srp, get_if_list
except ImportError:
    print("[ERROR] Scapy is not installed. Install it with: sudo pip3 install scapy")
    sys.exit(1)


def parse_args():
    """Handles command-line arguments."""
    parser = argparse.ArgumentParser(description="Simple ARP sweep using Scapy")
    parser.add_argument(
        "-n", "--network", default="192.168.58.0/24",
        help="Target network in CIDR notation (default: 192.168.58.0/24)"
    )
    parser.add_argument(
        "-i", "--interface", default="eth0",
        help="Network interface to use (default: eth0)"
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=2,
        help="Timeout in seconds to wait for responses (default: 2)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable Scapy's internal verbose mode"
    )
    return parser.parse_args()


def main():
    # Privilege check: Sending Layer 2 (L2) frames typically requires root/sudo
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        print("[ERROR] Please run this script with elevated privileges (e.g., sudo).")
        sys.exit(1)

    args = parse_args()

    # Quick check to ensure the specified interface exists on the system
    if args.interface not in get_if_list():
        print(f"[ERROR] Interface '{args.interface}' not found. Available interfaces:")
        for iface in get_if_list():
            print(f" - {iface}")
        sys.exit(1)

    # Broadcast MAC address: all bits set to 1 -> ff:ff:ff:ff:ff:ff
    # This tells the network switch to send the frame to every port in the VLAN.
    broadcast_mac = "ff:ff:ff:ff:ff:ff"

    # Layer 2 (Ethernet) Construction:
    # - dst=broadcast_mac: Sends the frame to all nodes in the L2 broadcast domain.
    ether_layer = Ether(dst=broadcast_mac)

    # ARP Layer Construction:
    # - op=1: Specifies an ARP "who-has" request.
    # - pdst: Destination network/host (Scapy handles CIDR ranges automatically).
    arp_layer = ARP(op=1, pdst=args.network)

    # Packet Stacking:
    # - In Scapy, the '/' operator stacks layers (Ethernet header / ARP payload).
    packet = ether_layer / arp_layer

    # Sending and Receiving at Layer 2 with srp():
    # - iface: Interface to transmit through.
    # - timeout: How long to wait for replies.
    # - verbose: Prints Scapy's internal progress if set.
    # Returns a tuple: (answered_packets, unanswered_packets).
    # 'answered' is a list of pairs: (sent_packet, received_packet).
    answered, unanswered = srp(
        packet,
        iface=args.interface,
        timeout=args.timeout,
        verbose=1 if args.verbose else 0
    )

    # Output Header
    print("\nActive hosts found (IP -> MAC):")
    print("-" * 45)

    # Scan the responses
    # Each 'rcv' is a response packet: an ARP reply encapsulated in an Ethernet frame.
    found_count = 0
    for _snd, rcv in answered:
        # rcv[ARP].psrc = Source IP in the ARP reply (the host that responded)
        ip = rcv[ARP].psrc

        # rcv[Ether].src = Source MAC address of the Ethernet frame (Hardware address of the host)
        mac = rcv[Ether].src

        # Formatted output
        print(f"{ip:15} -> {mac}")
        found_count += 1

    if found_count == 0:
        print("(No responses received)")

    print(f"\n[*] Scan complete. {found_count} host(s) discovered.")

    # Technical Note:
    # - ARP.op: 1 = request, 2 = reply
    # - Use rcv.show() during debugging to inspect all available fields in the packet.


if __name__ == "__main__":
    main()
