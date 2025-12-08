# 📘 **Linux Host Troubleshooting Lab — GNS3 (VPCS + Wireshark)**

This lab demonstrates essential host-level troubleshooting using the lightweight **VPCS** node in GNS3 for connectivity testing and **Wireshark** for packet inspection. The objective is to validate ARP resolution, ICMP reachability, and routing behavior without requiring a full Linux virtual machine.

This approach provides a fast and efficient way to examine Layer 2 and Layer 3 communication in a controlled environment.

---

## 🏗 **1. Lab Topology Overview**

The topology includes:

* **VPCS host** acting as a minimal Linux-like endpoint
* **Switch/Router infrastructure** (depending on your design)
* **Wireshark** packet capture running on the VPCS uplink

This enables verification of:

* ARP request and reply behavior
* ICMP echo request/reply communication
* Hop-by-hop routing
* Packet flow between host and gateway

> *Note: VPCS does not maintain a visible ARP cache. ARP traffic occurs normally and appears in Wireshark even when the VPCS `arp` command shows an empty table.*

---

## 🔧 **2. Host IP Configuration (VPCS)**

The VPCS node was configured with:

```bash
ip 192.168.20.20/24 192.168.20.1
```

This sets the host IP, mask, and default gateway.

Primary VPCS commands used:

* `ping <IP>`
* `trace <IP>`
* `show ip`
* `arp` *(may return empty — expected behavior)*

---

## 🧪 **3. Troubleshooting Steps**

### **Step 1 — Verify Host Configuration**

```bash
show ip
```

Confirms that VPCS is using the correct IP and gateway.

---

### **Step 2 — Test Connectivity with Ping**

```bash
ping 192.168.20.1
```

This validates basic Layer 3 reachability.

**Expected Result:**
ICMP echo requests and replies visible in Wireshark.

---

### **Step 3 — Analyze ARP Resolution in Wireshark**

A packet capture was taken on the host-facing link.

Wireshark filter:

```
arp
```

Expected behavior:

* ARP Request: “Who has 192.168.20.1?”
* ARP Reply: “192.168.20.1 is at <MAC address>”

---

### **Step 4 — Analyze ICMP Traffic**

Wireshark filter:

```
icmp
```

Expected frames include:

* ICMP Echo Request
* ICMP Echo Reply

This confirms end-to-end connectivity.

---

### **Step 5 — Run Traceroute from VPCS**

```bash
trace 192.168.20.1
```

Displays hop-by-hop path toward the destination.

---

## 📂 **4. Packet Capture Included**

All ARP and ICMP analysis is contained in a single file:

```
arp-icmp.pcapng
```

Reviewers may open this file in Wireshark to reproduce the analysis.

---

## 📸 **5. Screenshot Folder**

Pictures for this lab are stored in screenshots folder:

* `arp.png`
* `icmp.png`

There are many more that can be viewed inside the folder. 
---

## 📝 **6. Conclusion**

This lab demonstrates how to perform foundational host-level troubleshooting using VPCS and Wireshark. Key concepts validated include:

* ARP resolution and MAC-layer discovery
* ICMP reachability testing
* Hop-by-hop routing behavior
* Packet inspection for ARP and ICMP

This workflow effectively mirrors Linux troubleshooting fundamentals while using lightweight tools suited for rapid GNS3 lab development and portfolio documentation.
