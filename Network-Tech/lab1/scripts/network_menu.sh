#!/usr/bin/env bash
set -euo pipefail

interface="${1:-}"

choose_interface() {
    if [[ -n "$interface" ]]; then
        return
    fi
    interface="$(ip -o link show | awk -F': ' '$2 != "lo" {print $2; exit}')"
    if [[ -z "$interface" ]]; then
        echo "Не удалось определить сетевой интерфейс" >&2
        exit 1
    fi
}

show_hardware() {
    choose_interface
    echo "Интерфейс: $interface"
    ip -d link show dev "$interface"
    printf '\nСкорость и duplex:\n'
    ethtool "$interface" 2>/dev/null | grep -E 'Speed:|Duplex:|Link detected:' || true
    printf '\nMAC:\n'
    cat "/sys/class/net/$interface/address"
}

show_ipv4() {
    choose_interface
    ip -4 addr show dev "$interface"
    printf '\nШлюз:\n'
    ip route show default
    printf '\nDNS:\n'
    grep -E '^nameserver' /etc/resolv.conf || true
}

configure_static() {
    choose_interface
    sudo ip addr flush dev "$interface"
    sudo ip addr add 10.100.0.2/24 dev "$interface"
    sudo ip link set dev "$interface" up
    sudo ip route replace default via 10.100.0.1 dev "$interface"
    echo "Настроен сценарий 1 для $interface. DNS задается отдельно через resolv.conf."
}

configure_dhcp() {
    choose_interface
    if command -v dhclient >/dev/null 2>&1; then
        sudo dhclient -r "$interface" || true
        sudo dhclient "$interface"
    else
        echo "Не найден dhclient" >&2
        exit 1
    fi
}

while true; do
    cat <<EOF

Интерфейс: ${interface:-авто}
1) Показать параметры карты
2) Показать IPv4-конфигурацию
3) Настроить сценарий 1: 10.100.0.2/24, gateway 10.100.0.1
4) Настроить сценарий 2: получить параметры по DHCP
0) Выход
EOF
    read -r -p 'Выберите действие: ' action
    case "$action" in
        1) show_hardware ;;
        2) show_ipv4 ;;
        3) configure_static ;;
        4) configure_dhcp ;;
        0) exit 0 ;;
        *) echo 'Неизвестный пункт' >&2 ;;
    esac
done