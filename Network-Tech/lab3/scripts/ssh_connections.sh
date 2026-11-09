#!/usr/bin/env bash
set -euo pipefail

port="${1:-22}"

if ! [[ "$port" =~ ^[0-9]+$ ]] || (( port < 1 || port > 65535 )); then
    echo "Использование: $0 [порт 1..65535]" >&2
    exit 2
fi

if command -v ss >/dev/null 2>&1; then
    connections="$(ss -Htn state established "( sport = :$port )" 2>/dev/null || true)"
else
    connections="$(netstat -nt 2>/dev/null | awk -v port=":$port" '$4 ~ port && $6 == "ESTABLISHED"' || true)"
fi

printf '%s\n' "$connections" \
    | awk '{peer=$5; sub(/:[^:]+$/, "", peer); sub(/^\[|\]$/, "", peer); if (peer != "") count[peer]++} END {for (peer in count) print peer, count[peer]}' \
    | sort -k2,2nr -k1,1