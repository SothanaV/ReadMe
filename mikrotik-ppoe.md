ref https://www.sys2u.online/XPERT_TOPIC27_how-to-setup-mikrotik-2-WAN-(PPPoE)-to-LAN-MikroTik.html

```
/ip firewall mangle

add action=mark-routing chain=prerouting dst-address-type=!local new-routing-mark=wan-1-nt passthrough=no per-connection-classifier=both-addresses-and-ports:2/0

add action=mark-routing chain=prerouting dst-address-type=!local new-routing-mark=wan-2-true passthrough=no per-connection-classifier=both-addresses-and-ports:2/1
```

```
/ip firewall nat

add action=masquerade chain=srcnat dst-address-type=!local out-interface=ether1

add action=masquerade chain=srcnat dst-address-type=!local out-interface=ether2
```

# Chat
```
/ip address add address=171.100.254.223 interface=ether2
/ip route add gateway=171.100.254.222
```

```
/ip firewall mangle add chain=input in-interface=pppoe-nt action=mark-connection new-connection-mark=pppoe_conn passthrough=yes
/ip firewall mangle add chain=input in-interface=ether2 action=mark-connection new-connection-mark=ether2_conn passthrough=yes

/ip firewall mangle add chain=prerouting dst-address-type=!local in-interface=bridge-lan per-connection-classifier=both-addresses:2/0 action=mark-connection new-connection-mark=pppoe_conn passthrough=yes
/ip firewall mangle add chain=prerouting dst-address-type=!local in-interface=bridge-lan per-connection-classifier=both-addresses:2/1 action=mark-connection new-connection-mark=ether2_conn passthrough=yes
```

```
/ip firewall mangle add chain=prerouting connection-mark=pppoe_conn in-interface=bridge-lan action=mark-routing new-routing-mark=to_pppoe passthrough=yes
/ip firewall mangle add chain=prerouting connection-mark=ether2_conn in-interface=bridge-lan action=mark-routing new-routing-mark=to_ether2 passthrough=yes
```

```
/ip route add dst-address=0.0.0.0/0 gateway=pppoe-nt routing-mark=to_pppoe check-gateway=ping
/ip route add dst-address=0.0.0.0/0 gateway=171.100.254.222 routing-mark=to_ether2 check-gateway=ping

/ip route add dst-address=0.0.0.0/0 gateway=pppoe-nt distance=1 check-gateway=ping
/ip route add dst-address=0.0.0.0/0 gateway=171.100.254.222 distance=2 check-gateway=ping
```

```
/ip firewall nat add chain=srcnat out-interface=pppoe-nt action=masquerade
/ip firewall nat add chain=srcnat out-interface=ether2 action=masquerade
```