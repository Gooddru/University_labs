#!/usr/bin/env bash
set -euo pipefail

wan_interface="${WAN_INTERFACE:-eth0}"
lan_interface="${LAN_INTERFACE:-eth1}"
wan_network="${WAN_NETWORK:-192.168.0.0/24}"
real_host_network="${REAL_HOST_NETWORK:-192.168.0.0/24}"

if [[ "${1:-}" == "--help" ]]; then
    cat <<EOF
Генерирует restore-файл iptables для lab4 в stdout.

WAN_INTERFACE=$wan_interface
LAN_INTERFACE=$lan_interface
WAN_NETWORK=$wan_network
REAL_HOST_NETWORK=$real_host_network
EOF
    exit 0
fi

cat <<EOF
*nat
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 10.0.0.0/24 -o $wan_interface -j MASQUERADE
-A PREROUTING -i $wan_interface -p tcp --dport 55022 -j DNAT --to-destination 10.0.0.2:22
COMMIT
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -i $lan_interface -p tcp --dport 22 -j ACCEPT
-A INPUT -s 192.56.0.11 -j DROP
-A INPUT -s 14.12.44.0/18 -j DROP
-A INPUT -i $wan_interface -p tcp --dport 22 -j DROP
-A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A FORWARD -i $lan_interface -o $wan_interface -s 10.0.0.0/24 -p udp -d 8.8.8.8 --dport 53 -j ACCEPT
-A FORWARD -i $lan_interface -o $wan_interface -s 10.0.0.0/24 -p tcp -d 8.8.8.8 --dport 53 -j ACCEPT
-A FORWARD -i $lan_interface -o $wan_interface -s 10.0.0.0/24 -p tcp -m multiport --dports 22,25,80,110,443,8080 -j ACCEPT
-A FORWARD -i $wan_interface -o $lan_interface -s $real_host_network -p tcp --dport 55022 -d 10.0.0.2 -j ACCEPT
-A FORWARD -s 192.56.0.11 -j DROP
-A FORWARD -s 14.12.44.0/18 -j DROP
-A FORWARD -i $lan_interface -o $wan_interface -p icmp -s 10.0.0.0/24 -d 8.8.8.8 --icmp-type echo-request -j ACCEPT
COMMIT
EOF