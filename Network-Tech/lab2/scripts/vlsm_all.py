#!/usr/bin/env python3
"""Calculate the five VLSM subnets for every lab2 assignment variant."""

from __future__ import annotations

import ipaddress

VARIANTS = {
    1: ("194.85.32.19/24", [10, 6, 1, 18, 100]),
    2: ("10.12.12.15/23", [25, 16, 240, 117, 1]),
    3: ("212.24.15.199/26", [7, 0, 0, 11, 10]),
    4: ("120.13.120.120/27", [5, 2, 2, 1, 1]),
}


def subnet_size(computers: int) -> int:
    # One address is needed for the router port and two are network/broadcast.
    required_addresses = max(computers + 1, 2) + 2
    size = 4
    while size < required_addresses:
        size *= 2
    return size


def calculate(network_text: str, computers: list[int]) -> list[tuple[int, ipaddress.IPv4Network]]:
    source = ipaddress.ip_network(network_text, strict=False)
    cursor = int(source.network_address)
    result = []
    for index, count in sorted(enumerate(computers, 1), key=lambda item: -item[1]):
        size = subnet_size(count)
        prefix = 32 - (size.bit_length() - 1)
        candidate = ipaddress.ip_network((cursor, prefix), strict=False)
        if not candidate.subnet_of(source):
            raise ValueError(f"Вариант не помещается в исходную сеть: {network_text}")
        result.append((index, candidate))
        cursor = int(candidate.broadcast_address) + 1
    return sorted(result)


for variant, (network, computers) in VARIANTS.items():
    print(f"Вариант {variant}: исходная сеть {network}")
    print("Сеть | Компьютеры | Подсеть | Маска | Пригодный диапазон")
    for index, subnet in calculate(network, computers):
        hosts = list(subnet.hosts())
        host_range = f"{hosts[0]} - {hosts[-1]}" if hosts else "нет"
        print(f"{index} | {computers[index - 1]} | {subnet.network_address}/{subnet.prefixlen} | {subnet.netmask} | {host_range}")
    print()