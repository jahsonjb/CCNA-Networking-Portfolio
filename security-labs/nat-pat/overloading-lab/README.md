# NAT Overload (PAT) — GNS3 Lab Documentation

## Overview

This lab demonstrates **NAT Overload (PAT)** using a Cisco IOS router connected to an outside host and a Layer 2 switch carrying three VLANs (10, 20, 30).
Each VLAN contains one host, and all inside networks successfully reach the outside host using a single public IP address configured on the router’s outside interface.

Screenshots included in this lab show:

- Topology  
- Router and switch interface states  
- VLAN configuration  
- NAT section of the running config  
- PAT translation table  
- Ping tests from all internal VLANs  
- Ping tests from the outside host  

This validates that **PAT is working correctly across multiple subnets** and that **Router-on-a-Stick + NAT** is functioning as intended.

---

## Topology Summary

```

Outside Host (203.0.113.1/24)
|
Router Gi0/0 (203.0.113.2/24)  <-- NAT Outside
Router Gi0/1 (802.1Q Trunk)    <-- NAT Inside Subinterfaces
|
L2 Switch
-----------------
|      |       |
VLAN10  VLAN20  VLAN30
PC1     PC2     PC3

```

![Topology Layout](./nat-pat/screenshots/NAT-ROUTER-TOPOLOGY.png)

---

## Key Router Configuration

### Inside Interfaces (Subinterfaces)

```

interface GigabitEthernet0/1
no ip address

interface GigabitEthernet0/1.10
encapsulation dot1Q 10
ip address 192.168.10.1 255.255.255.0
ip nat inside

interface GigabitEthernet0/1.20
encapsulation dot1Q 20
ip address 192.168.20.1 255.255.255.0
ip nat inside

interface GigabitEthernet0/1.30
encapsulation dot1Q 30
ip address 192.168.30.1 255.255.255.0
ip nat inside

```

### Outside Interface

```

interface GigabitEthernet0/0
ip address 203.0.113.2 255.255.255.0
ip nat outside
no shutdown

```

### Default Route

```

ip route 0.0.0.0 0.0.0.0 203.0.113.1

```

### PAT Configuration

```

access-list 10 permit 192.168.10.0 0.0.0.255
access-list 10 permit 192.168.20.0 0.0.0.255
access-list 10 permit 192.168.30.0 0.0.0.255

ip nat inside source list 10 interface GigabitEthernet0/0 overload

```

---

## Screenshot Summary (Markdown Image Format)

### 1. GNS3 Workspace Topology
![GNS3 Topology](./nat-pat/screenshots/NAT-ROUTER-TOPOLOGY.png)

---

### 2. NAT Router — show ip interface brief
![IP Interface Brief](./nat-pat/screenshots/ip-int-brief.png)

---

### 3. Switch — show vlan brief
![VLAN Brief](./nat-pat/screenshots/vlan-brief.png)

---

### 4. Switch — show interfaces trunk
![Interfaces Trunk](./nat-pat/screenshots/int-trunk.png)

---

### 5. NAT Section — show run | section nat
![NAT Config Section](./nat-pat/screenshots/Nat-config-section.png)

---

### 6. NAT Translation Table — show ip nat translations
![NAT Translation Table](./nat-pat/screenshots/ip-nat-trans.png)

---

### 7. Inside Hosts — Successful ping to outside
![PC Success Ping](./nat-pat/screenshots/pc-success-ping.png)

---

### 8. Outside Host — Ping to Router Public IP
![Outside Ping](./nat-pat/screenshots/outside-ping.png)

---

### Additional NAT Statistics
![NAT Stats](./nat-pat/screenshots/nat-stats.png)

---

## Validation Summary

All verification steps succeeded:

- Router-on-a-Stick trunking functional  
- All VLANs reachable  
- PAT overload translation confirmed  
- NAT translation table populated for all inside hosts  
- Outside host reachable  
- End-to-end connectivity validated  

---

## Conclusion

This lab successfully demonstrates:

- Multi-VLAN segmentation  
- Inter-VLAN routing via subinterfaces  
- NAT Overload (PAT) translating multiple internal hosts  
- Functional inside-to-outside communication using a single public IP  

This provides the foundation for advanced NAT labs, including:

- Static NAT  
- NAT Pools  
- Port Forwarding  
- ACL-based NAT policies  
- Multi-router NAT design  
```


