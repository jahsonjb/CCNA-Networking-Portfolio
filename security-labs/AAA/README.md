### AAA (Authentication, Authorization, and Accounting) Labs

This folder contains a collection of labs, notes, and configurations focused on **AAA (Authentication, Authorization, and Accounting)** in Cisco networking environments. The goal is to demonstrate how centralized authentication works across different scenarios, using tools such as local AAA, TACACS+, RADIUS, and Cisco ISE.

AAA is a foundational security concept in enterprise networks, and these labs show how Cisco devices authenticate users, authorize access, and log activity using both local and external servers.

---

## 🔐 What This Folder Covers

The labs in this directory explore several AAA concepts, including:

### ✅ **Local AAA**
- Enabling `aaa new-model`
- Creating local users
- Applying authentication to VTY and console lines

### ✅ **TACACS+ Authentication**
- Using external TACACS+ servers for device administration
- Configuring method lists
- Testing login via Telnet/SSH
- Viewing TACACS+ logs and command accounting

### ✅ **RADIUS Authentication**
- Using RADIUS for network access control
- Integrating with AAA servers or Cisco ISE
- VLAN assignment and authorization policies

### ✅ **Cisco ISE Integration (Optional Labs)**
- Using ISE as a centralized AAA server
- 802.1X, MAB, and posture assessment
- TACACS+ device administration through ISE

---

## 🧪 Lab Environments Used

These labs may use one or more of the following environments:

- **Cisco Packet Tracer** (lightweight AAA demonstrations)
- **GNS3** (more advanced AAA and ISE labs)
- **Cisco ISE** (enterprise-grade identity services)
- **Cisco routers and switches** (virtual or physical)

Each lab folder includes:
- A description of the topology  
- Device configurations  
- Step-by-step instructions  
- Verification commands  
- Screenshots or Packet Tracer files (if applicable)

---

## 📁 Folder Structure

```
AAA/
│
├── local-aaa/          # Local authentication and authorization examples
├── tacacs-lab/         # TACACS+ labs using Packet Tracer or GNS3
├── radius-lab/         # RADIUS authentication labs
├── ise-labs/           # Cisco ISE integration (optional/advanced)
└── README.md           # This file
```

As you add more labs, this structure can grow to include multi-router topologies, downloadable ACLs, 802.1X, and more.

---

## 🎯 Purpose of These Labs

These labs are designed to help you:

- Understand how AAA works on Cisco devices  
- Practice configuring TACACS+ and RADIUS  
- Build confidence with authentication method lists  
- Prepare for CCNA/CCNP security topics  
- Strengthen your GitHub portfolio with real networking projects  
