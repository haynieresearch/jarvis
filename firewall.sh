#!/bin/bash

#Default Open Ports
publicip="192.169.218.133"
ports="8123"
localnet=$(dig +short local.haynienetworks.com)

IPT=/sbin/iptables
WGET=/usr/bin/wget
EGREP=/bin/egrep

#Delete Current Rules & Chains
$IPT --flush
$IPT --delete-chain

#Allow Loopback
$IPT -A INPUT -i lo -j ACCEPT
$IPT -A OUTPUT -o lo -j ACCEPT

#Allow Local
$IPT -A INPUT -s 10.0.0.0/8 -j ACCEPT
$IPT -A OUTPUT -s 10.0.0.0/8 -j ACCEPT
$IPT -A INPUT -s 192.168.0.0/16 -j ACCEPT
$IPT -A OUTPUT -s 192.168.0.0/16 -j ACCEPT

#Allow Local
$IPT -A INPUT -s $localnet -j ACCEPT
$IPT -A OUTPUT -s $localnet -j ACCEPT

#Allow Established Connections
$IPT -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#Standard Rules
$IPT -A INPUT -p tcp -s $publicip -m multiport --dports $ports -j ACCEPT
$IPT -A OUTPUT -p tcp -m multiport --sports $ports -j ACCEPT

#Default Policies
$IPT -P INPUT DROP
$IPT -P FORWARD ACCEPT
$IPT -P OUTPUT ACCEPT
exit 0
