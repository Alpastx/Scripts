#!/bin/bash

ICON="🌐"

get_ip() {
    ip -4 addr show "$1" 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1
}

tun_ip=$(get_ip tun0)
eth_ip=$(get_ip enp88s0)

if [[ "$1" == "--copy" ]]; then
    # Copy mode
    if [[ -n "$tun_ip" ]]; then
        ip="$tun_ip"
    elif [[ -n "$eth_ip" ]]; then
        ip="$eth_ip"
    else
        ip=""
    fi

    if [[ -n "$ip" ]]; then
        if command -v wl-copy &> /dev/null; then
            echo -n "$ip" | wl-copy
        elif command -v xclip &> /dev/null; then
            echo -n "$ip" | xclip -selection clipboard
        elif command -v xsel &> /dev/null; then
            echo -n "$ip" | xsel --clipboard --input
        fi
        notify-send "📋 IP copied" "$ip"
    else
        notify-send "⚠️ No IP to copy"
    fi
    exit 0
fi

# Output for Waybar
if [[ -n "$tun_ip" ]]; then
    echo "{\"text\": \"$ICON $tun_ip\", \"class\": \"tun\"}"
elif [[ -n "$eth_ip" ]]; then
    echo "{\"text\": \"$ICON $eth_ip\", \"class\": \"eth\"}"
else
    echo "{\"text\": \"$ICON -\", \"class\": \"down\"}"
fi
