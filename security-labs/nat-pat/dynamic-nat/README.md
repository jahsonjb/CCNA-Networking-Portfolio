# 📘 **Dynamic NAT with a Pool — Cisco Packet Tracer (Scenario 2)**

### *Inside LAN via MLS SVI → NAT Edge Router → ISP Simulation*

This lab demonstrates **Dynamic NAT using a public IP address pool**, allowing multiple internal hosts to access external networks through a range of available global addresses. Unlike static NAT, dynamic NAT allocates public IPs **only when traffic is initiated** and releases them when sessions expire. This scenario builds directly on the previous Static NAT setup, using the same multilayer switch and NAT edge router topology.

---

## 🏗 **1. Lab Topology Overview**

This scenario uses the same network design as Scenario 1:

* **Multilayer Switch (MLS)** as the default gateway using an SVI
* **R1** as the NAT edge router performing Dynamic NAT
* **ISP Router** representing the external network
* **Inside hosts** located in VLAN 20

Traffic flow:

```
[Inside Hosts] → [MLS SVI] → [R1 NAT] → [ISP Router] → "Internet"
```

Dynamic NAT assigns public IPs from a pool:

```
Pool Range: 209.165.200.227 – 209.165.200.229
```

This allows internal hosts to receive temporary public IPs as needed.

---

## 🔧 **2. IP Addressing Scheme**

```
IP ADDRESSING SCHEME – DYNAMIC NAT POOL (MLS SVI + R1 NAT + ISP)

Inside LAN (VLAN 20)
---------------------------------------------------------
Device / Interface        IP Address          Subnet Mask          Notes
MLS – SVI (VLAN20)        192.168.20.1        255.255.255.0        Default gateway for inside hosts
PC1                       192.168.20.10       255.255.255.0        Inside host for NAT verification
PC2                       192.168.20.20       255.255.255.0        Second host for NAT pool testing
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

Dynamic NAT Pool
---------------------------------------------------------
Pool Range                209.165.200.227 – 209.165.200.229
Netmask                   255.255.255.248
Notes                     Used for dynamic outbound translations

Routing (Default Routes and Return Route)
---------------------------------------------------------
Device                    Route                                Notes
MLS                       ip route 0.0.0.0 0.0.0.0 192.168.30.1   Default route toward R1
R1                        ip route 0.0.0.0 0.0.0.0 209.165.200.230 Default route toward ISP
ISP Router                ip route 192.168.20.0 255.255.255.0 209.165.200.225  Return route to inside LAN
```

---

## ⚙️ **3. Configuration Summary**

Dynamic NAT requires three components:

1. **NAT Pool** – defines the range of public IPs
2. **ACL** – matches internal traffic eligible for NAT
3. **NAT Rule** – binds the ACL to the pool

---

### **Multilayer Switch (MLS)**

No changes from Scenario 1. The MLS continues routing inside traffic and forwarding to R1.

```bash
ip routing

interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shut

interface g0/1
 no switchport
 ip address 192.168.30.2 255.255.255.252
 no shut

ip route 0.0.0.0 0.0.0.0 192.168.30.1
```

---

### **R1 – NAT Edge Router (Dynamic NAT Pool)**

Add the following to the existing NAT configuration from Scenario 1:

```bash
! Define the NAT pool
ip nat pool dynamicpool 209.165.200.227 209.165.200.229 netmask 255.255.255.248

! Match inside traffic leaving toward the ISP
access-list 10 permit 192.168.20.0 0.0.0.255

! Bind ACL 10 to the pool
ip nat inside source list 10 pool NAT-POOL
```

Interface configuration remains:

```bash
interface g0/1
 ip address 192.168.30.1 255.255.255.252
 ip nat inside

interface g0/0
 ip address 209.165.200.225 255.255.255.248
 ip nat outside
```

Routing configuration:

```bash
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

### **1. Test outbound traffic from inside PC1**

From PC1:

```bash
ping 209.165.200.230
```

On R1:

```bash
show ip nat translations
```

Expected entry:

```
192.168.20.10   →   209.165.200.227
```

---

### **2. Test outbound traffic from inside PC2**

From PC2:

```bash
ping 209.165.200.230
```

Back on R1:

```
192.168.20.20   →   209.165.200.228
192.168.20.10   →   209.165.200.227
```

This confirms that:

* Each host receives a unique public IP
* NAT addresses are allocated dynamically from the pool

---

### **3. Traceroute from the inside PC**

From PC1 or PC2:

```bash
tracert 209.165.200.230
```

Expected path:

```
PC → 192.168.20.1 (MLS) → 192.168.30.1 (R1 NAT) → 209.165.200.230 (ISP)
```

---

### **4. Optional: Test pool exhaustion**

If you add a 4th inside host:

Only **three** hosts receive pool translations.
The 4th will fail to translate because:

```
Pool size = 3 IPs
```

This is excellent for demonstration purposes.

---

## 📸 **5. Screenshots for this lab**

Include:

* Topology diagram
* NAT pool definition (`show run | include ip nat pool`)
* ACL used for NAT (`show access-lists 10`)
* NAT translation table after PC1 + PC2 tests
* Pings from both inside hosts


Optional:

* NAT table during pool exhaustion test

---

## 📂 **6. Files Included in This Folder**

* `dynamic-nat-pool.pkt` (uploaded separately)
* Screenshots folder
* `README.md` (this file)
* Addressing table (txt)


