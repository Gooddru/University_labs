#!/usr/bin/env bash
set -euo pipefail

bond_interface="${1:-bond007}"

if [[ ! -r /proc/net/dev ]]; then
    echo 'Не найден /proc/net/dev' >&2
    exit 1
fi

awk -v interface="$bond_interface" '
    $1 == interface ":" {
        printf "%s interface=%s receive_packets=%s transmit_packets=%s\n", strftime("%Y-%m-%dT%H:%M:%S%z"), interface, $3, $11
        found = 1
    }
    END { if (!found) exit 1 }
' /proc/net/dev