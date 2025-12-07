# 📘 **Static NAT Lab — Cisco Packet Tracer (Scenario 1)**

### *Inside LAN via MLS SVI → NAT Edge Router → ISP Simulation*

This lab demonstrates **Static NAT (one-to-one mapping)** using a multilayer switch for internal routing and a dedicated edge router performing NAT. The objective is to expose an internal server to an external network using a public IP address while maintaining proper routing boundaries between the LAN, the NAT edge, and the simulated ISP.

---

## 🏗 **1. Lab Topology Overview**

This scenario uses:

* **Multilayer Switch (MLS)** as the default gateway using an SVI
* **R1** as the NAT edge router (inside ↔ outside)
* **ISP Router** representing the external network
* **Inside hosts** located in VLAN 20

Traffic flow:

```
[Inside PC/Server] → [MLS SVI] → [R1 NAT] → [ISP Router] → "Internet"
```

Static NAT mapping:

```
192.168.20.50  →  209.165.200.226
```

This allows external hosts to reach the internal server via a public IP.

---

## 🔧 **2. IP Addressing Scheme**

```
IP ADDRESSING SCHEME – STATIC NAT (MLS SVI + R1 NAT + ISP)

Inside LAN (VLAN 20)
---------------------------------------------------------
Device / Interface        IP Address          Subnet Mask          Notes
MLS – SVI (VLAN20)        192.168.20.1        255.255.255.0        Default gateway for inside hosts
Server                    192.168.20.50       255.255.255.0        Inside local (static NAT mapping)
PC (optional)             192.168.20.10       255.255.255.0        Inside host
Host Default Gateway      192.168.20.1        ----                 Points to MLS SVI

MLS ↔ R1 Routed Link
---------------------------------------------------------
Device / Interface        IP Address          Subnet Mask          Notes
R1 – G0/1 (inside)        192.168.30.1        255.255.255.252      NAT inside interface
MLS – Routed Port         192.168.30.2        255.255.255.252      L3 uplink toward R1

R1 ↔ ISP WAN Link
---------------------------------------------------------
Device / Interface        IP Address          Subnet Mask          Notes
R1 – G0/0 (outside)       209.165.200.225     255.255.255.248      NAT outside interface
ISP Router – G0/0         209.165.200.230     255.255.255.248      WAN interface

Public NAT IP
---------------------------------------------------------
Device / Interface        IP Address          Subnet Mask          Notes
Static NAT Global IP      209.165.200.226     255.255.255.248      Public IP mapped to 192.168.20.50

Routing (Default Routes and Return Route)
---------------------------------------------------------
Device                    Route                                Notes
MLS                       ip route 0.0.0.0 0.0.0.0 192.168.30.1   Default route toward R1
R1                        ip route 0.0.0.0 0.0.0.0 209.165.200.230 Default route toward ISP
ISP Router                ip route 192.168.20.0 255.255.255.0 209.165.200.225  Return route to inside LAN
```

---

## ⚙️ **3. Configuration Summary**

### **Multilayer Switch (MLS)**

Handles internal routing via SVI.

```bash
ip routing

vlan 20
 name INSIDE_LAN

interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shut

interface fa0/1
 switchport mode access
 switchport access vlan 20

interface fa0/2
 switchport mode access
 switchport access vlan 20

interface g0/1
 no switchport
 ip address 192.168.30.2 255.255.255.252
 no shut

ip route 0.0.0.0 0.0.0.0 192.168.30.1
```

---

### **R1 – NAT Edge Router**

```bash
interface g0/1
 ip address 192.168.30.1 255.255.255.252
 ip nat inside
 no shut

interface g0/0
 ip address 209.165.200.225 255.255.255.248
 ip nat outside
 no shut

ip nat inside source static 192.168.20.50 209.165.200.226

ip route 192.168.20.0 255.255.255.0 192.168.30.2
ip route 0.0.0.0 0.0.0.0 209.165.200.230
```

---

### **ISP Router**

```bash
interface g0/0
 ip address 209.165.200.230 255.255.255.248
 no shut

ip route 192.168.20.0 255.255.255.0 209.165.200.225
```

---

## 🧪 **4. Verification Steps**

### **Check NAT Table on R1**

```bash
show ip nat translations
```

You should see:

```
192.168.20.50  <->  209.165.200.226
```

---

### **Verify Inside-to-Outside Connectivity**

From the **inside user PC**:

```bash
ping 209.165.200.230
```

This confirms the MLS → R1 → ISP path is working.

---

### **Traceroute from Inside PC to the Public NAT IP**

From the **inside PC**:

```bash
tracert 209.165.200.226
```

Expected path:

```
PC → MLS SVI (192.168.20.1) → R1 Inside (192.168.30.1) → ISP Router (209.165.200.230) → Public NAT IP
```

This validates:

* The inside routing path
* NAT boundary behavior
* Proper return-path routing via the ISP router

---

### **External-to-Internal NAT Test**

From the ISP router:

```bash
ping 209.165.200.226
```

Successful replies confirm:

* Static NAT translation is correct
* Return routing is functioning
* The internal server is reachable from outside via its public IP

---

## 📸 **5. Screenshots for this lab**

Include:

* Topology diagram
* MLS SVI configuration (`show run | section interface Vlan20`)
* R1 NAT configuration (`show run | section nat`)
* NAT translation table (`show ip nat translations`)
* Inside PC traceroute to the public IP
* ISP router ping to the public IP

These validate the full path and NAT behavior.

---

## 📂 **6. Files Included in This Folder**

* `static-nat.pkt` (uploaded separately)
* Screenshots folder
* `README.md` (this file)
* Addressing table (txt)
