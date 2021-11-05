#!/bin/bash
#Copyright 2020 Haynie IPHC, LLC
#Developed by Haynie Research & Development, LLC
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

#Default Open Ports
publicip=$(curl -s checkip.amazonaws.com)
ports="8123"
localnet=$(dig +short jarvis.local) #local FQDN

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
$IPT -A INPUT -s 192.168.0.0/8 -j ACCEPT
$IPT -A OUTPUT -s 192.168.0.0/8 -j ACCEPT

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
