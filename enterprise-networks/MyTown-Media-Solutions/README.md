# **MyTown Media Solutions – Enterprise Network Deployment (Cisco Packet Tracer)**

*A full multi-site enterprise network featuring GRE tunneling, OSPF routing, VLAN segmentation, centralized services, and secure access control.*

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Tool](https://img.shields.io/badge/Tool-Cisco%20Packet%20Tracer-blue)
![Category](https://img.shields.io/badge/Category-Enterprise%20Networking-orange)

---

## **📌 Overview**

This repository contains the full enterprise network deployment for the **MyTown Media Solutions** project.
The design models a realistic HQ + Branch environment connected through an ISP using a **GRE tunnel** and **OSPF Area 0**. All Layer 3 routing, NAT boundaries, DHCP services, VLANs, ACLs, and security features follow production-grade network engineering standards.

The project demonstrates multi-site connectivity, centralized services, segmentation, and secure device management using Cisco IOS technologies.

---

## **🏗️ Network Architecture Summary**

### **Headquarters**

* VLANs: Management, Sales, Engineering, Holding
* Router-on-a-Stick on HQ-RTR
* EtherChannel (PAgP) between HQ switches
* Centralized **DHCP, DNS, TFTP, HTTP** services
* NAT Overload for all internal networks
* OSPF over GRE to Branch Office

### **Branch Office**

* VLANs: Admin, Guest, Holding
* DHCP relay to HQ server
* Router-on-a-Stick
* All Internet access routed through HQ NAT
* OSPF adjacency formed through GRE

### **ISP Router**

* Simulated public WAN segment
* Tunnel carrier for both sites

---

## **🔑 Key Features**

### **✔ VLAN & Addressing**

* Fully VLSM-applied subnetting using **192.168.99.0/24**
* GRE uses **192.168.98.0/30**
* Gateways use the first usable address in each subnet

### **✔ Routing**

* **OSPF Area 0** configured on all routers
* GRE tunnel provides logical point-to-point adjacency
* Consistent and scalable single-area design

### **✔ NAT & Internet Edge**

* NAT Overload configured on HQ-RTR
* ISP-RTR provides simulated public network
* Branch uses HQ as its NAT boundary

### **✔ Services (HQ-SRV)**

* DHCP for all VLANs (HQ + Branch)
* Internal DNS
* TFTP for device backups
* Internal HTTP web server

### **✔ Access Control**

* Sales ↔ Engineering blocked bidirectionally
* Management VLAN has full access
* ACLs applied **inbound** on sub-interfaces
* Additional ACLs restrict DNS/Web services

### **✔ Switch & L2 Enhancements**

* HQ-SW1 forced as STP root
* EtherChannel between HQ switches
* All unused interfaces placed in VLAN 99 and administratively shut down

### **✔ Security Hardening**

* SSH-only access to all devices
* RSA keys generated on every router/switch
* Login and MOTD banners
* Port security (sticky MAC, max 2, restrict mode)
* CDP disabled on WAN-facing interfaces
* Encrypted passwords

---

## **📁 Repository Contents**

This repository will include the following uploaded files:

### **1. `MyTownMediaSolutions.pkt`**

* Full Cisco Packet Tracer project file
* All configs saved
* Device names, interfaces, labels included

### **2. `/screenshots/` folder**

* Topology overview
* Routing table snapshots (`show ip route`, `show ip ospf neighbor`)
* ACL verification screenshots
* NAT translations
* STP root output
* EtherChannel summary
* SSH login banners
* DHCP/DNS tests
* TFTP backup demonstration

### **3. `network-addressing-table.md`**

* Complete VLSM subnet table
* VLAN-to-subnet mapping
* Gateway assignments
* Usable host ranges

## **🛠️ Troubleshooting Notes**

Real-world debugging encountered during the build:

* DHCP OFFER packets were **dropped at HQ-RTR** due to:

  * Missing `ip helper-address`
  * Incorrect native VLAN assignment
* ACLs were initially applied **outbound**, allowing unintended traffic
* SSH attempts failed until RSA keys were generated on all devices
* Branch initially failed to learn VLAN 99’s network due to OSPF area configuration and subnet advertising
* GRE tunnel OSPF adjacency required correct tunnel source and reachability

Each issue was documented and resolved as part of the learning process.

---

## **🎯 Purpose of This Project**

This lab reflects what a mid-sized business might deploy for:

* Scalable multi-site routing
* Split-site VLAN design
* Centralized services
* Secure segmentation
* Controlled WAN topology
* Hardened device access

It reinforces skills applicable to:

* Network Support / Network Engineering
* Infrastructure Operations
* SOC / Blue-Team environments
* CCNA-level lab design
* Real-world production architectures

---

