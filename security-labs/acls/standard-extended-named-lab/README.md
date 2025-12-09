# **🔐 ACL Troubleshooting & Design Lab — README.md**

This lab explores **three phases** of ACL design and troubleshooting on a router-on-a-stick topology using:

* **VLAN 10 – Users**
* **VLAN 20 – Admin**
* **VLAN 30 – Servers**
* **SVIs on the router:**

  * VLAN 10 → `192.168.10.1`
  * VLAN 20 → `192.168.20.1` (management SVI)
  * VLAN 30 → `192.168.30.1`

The goal is to enforce **traffic restrictions** using:

1. **Phase 1 — Standard Numbered ACL**
2. **Phase 2 — Named Extended ACL (`access-restrict`)**
3. **Phase 3 — Numbered Extended ACL**

This README captures all lessons learned, mistakes discovered, and best practices demonstrated during the lab.

---

# **📘 Phase 1 — Standard ACL (Block VLAN 10 → VLAN 30)**

### **Goal**

Block all communication from **VLAN 10** to **VLAN 30**, while allowing all other traffic to continue functioning normally.

---

## **Key Lesson — Standard ACLs match *source only***

Because standard ACLs match only **source IPs**, they must be placed:

* **Close to the destination**
  **OR**
* **Inbound on the source** interface

The important point:
A standard ACL **cannot** match destination VLAN 30 directly.

---

## **❌ Mistake Encountered — ACL Applied Inbound (Wrong Direction)**

The ACL was originally placed **inbound** on VLAN 30:

```
interface g0/0.30
 ip access-group BLOCK-V10 in
```

**Result:**
VLAN 10 devices could STILL reach VLAN 30.

---

### **Why It Failed**

Traffic from VLAN 10 flows:

```
g0/0.10 (inbound) → routing → g0/0.30 (outbound)
```

Inbound on VLAN 30 sees **traffic FROM VLAN 30**, not traffic *to* VLAN 30.

---

## ✔ **Correct Fix — Apply ACL OUTBOUND on VLAN 30**

Outbound on g0/0.30 finally filtered packets *after routing*, successfully blocking VLAN 10 → VLAN 30.

**Standard ACL Configuration**
![p1-standard-acl-config](./screenshots/p1-standard-acl-config.png)

**Incorrect ACL Placement (Inbound on VLAN 30)**
![p1-standard-acl-applied](./screenshots/p1-standard-acl-applied.png)

**Corrected ACL Placement (Outbound on VLAN 30)**
![p1-corrected-placement-standard-acl](./screenshots/p1-corrected-placement-standard-acl.png)

**VLAN 10 Ping Test (After Corrected ACL Enforcement & Placement)**
![p1-vlan10-ping](./screenshots/p1-vlan10-ping.png)


---

### ✔ **Phase 1 Completed Successfully**

---

# **📘 Phase 2 — Named Extended ACL (`access-restrict`)**

This phase restricts access **to the Admin SVI (192.168.20.1)** using an extended named ACL.

---

## **Phase 2 Requirements**

1. Allow VLAN 20 to SSH into 192.168.20.1
2. Block VLAN 10 from SSH access
3. Allow VLAN 20 to ping the Admin SVI
4. Block VLAN 10 from pinging the Admin SVI
5. Block all other management protocols (HTTP/HTTPS/Telnet/SNMP/TFTP)
6. End with `permit ip any any`

---

# **🔎 Problems Encountered & Fixes**

## **❌ 1. SSH & ICMP from VLAN 10 still worked**

Even with deny statements in place, traffic from VLAN 10 reached the Admin SVI.

---

## **Cause A — SSH not configured yet**

SSH must be functional before ACL testing; otherwise, the router gives misleading results.

SSH was configured:

```
enable secret password

ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin secret password
line vty 0 4
 login local
 transport input ssh
```

---

## **❌ Cause B — ACL not applied on VLAN 10 inbound**

Traffic from VLAN 10 trying to reach 192.168.20.1 flows:

```
PC VLAN 10 → g0/0.10 (inbound) → router → local SVI 192.168.20.1
```

**It never reaches VLAN 20 outbound**, so placing the ACL there alone was insufficient.

### ✔ Fix

Apply the ACL **inbound on g0/0.10**:

```
interface g0/0.10
 ip access-group access-restrict in
```

This allowed the ACL to inspect the traffic where it actually enters the router.

---

## **❌ 2. ICMP rule only permitted VLAN 20 — but did not deny VLAN 10**

Original rule:

```
30 permit icmp 192.168.20.0 0.0.0.255 host 192.168.20.1 echo
```

This permits VLAN 20 → Admin SVI, but does not *deny* VLAN 10 → Admin SVI.

### ✔ Fix — Add explicit deny

```
35 deny icmp 192.168.10.0 0.0.0.255 host 192.168.20.1 echo
```

This correctly blocked VLAN 10 pings.

---

# **Final Named ACL (`access-restrict`)**

```
ip access-list extended access-restrict
 10 permit tcp 192.168.20.0 0.0.0.255 host 192.168.20.1 eq 22
 20 deny   tcp 192.168.10.0 0.0.0.255 host 192.168.20.1 eq 22
 30 permit icmp 192.168.20.0 0.0.0.255 host 192.168.20.1 echo
 35 deny   icmp 192.168.10.0 0.0.0.255 host 192.168.20.1 echo
 40 deny   tcp any host 192.168.20.1 eq www
 50 deny   tcp any host 192.168.20.1 eq 443
 60 deny   tcp any host 192.168.20.1 eq telnet
 70 deny   udp any host 192.168.20.1 range snmp 162
 80 deny   udp any host 192.168.20.1 eq tftp
 90 permit ip any any
```

✔ VLAN 20 can SSH + ping
✔ VLAN 10 cannot SSH or ping
✔ All other management protocols blocked
✔ Normal routing unaffected

### Phase 2 — Named Extended ACL Screenshots

**SSH Success from VLAN 20 (Expected Allow)**
![p2-admin-ssh](./screenshots/p2-admin-ssh.png)

**Named ACL Applied to Sub-Interface**
![p2-named-acl-on-sub](./screenshots/p2-named-acl-on-sub.png)

**ACL Verification (`show access-lists`)**
![p2-show-access](./screenshots/p2-show-access.png)

**SSH Failure from VLAN 10 (Expected Deny)**
![p2-ssh-fail-vlan-10](./screenshots/p2-ssh-fail-vlan-10.png)

**ICMP Failure from VLAN 10 (After Rule 35 Added)**
![p2-vlan10-ping](./screenshots/p2-vlan10-ping.png)

---

# **📘 Lessons Learned (Critical ACL Concepts)**

### **1. ACLs only filter traffic they actually SEE**

Direction matters.

### **2. Extended ACLs go close to the source**

Inbound on VLAN 10 was the correct design.

### **3. Standard ACLs fit best near the destination**

Phase 1 reinforced this.

### **4. You must configure SSH before testing SSH ACLs**

Otherwise tests produce false positives.

### **5. Explicit denies prevent implicit mismatches**

Especially important with ICMP.

### **6. Always test both allowed and denied flows**

Ping + SSH + cross-VLAN tests.

---

# **📘 Phase 3 — Numbered Extended ACL (Server Access Control)**

### **Phase 3 Goal**

Create a **numbered extended ACL (110)** that enforces:

1. **VLAN 20 (Admins) can reach all servers in VLAN 30**
2. **VLAN 10 (Users) can ONLY access the web server (192.168.30.30) via ports 80/443**
3. **All other VLAN 10 → VLAN 30 traffic must be denied**
4. Preserve all unrelated flows using a final `permit ip any any`

---

## **Your ACL 110 (Final Working Version)**

```
access-list 110 permit ip 192.168.20.0 0.0.0.255 192.168.30.0 0.0.0.255
access-list 110 permit tcp 192.168.10.0 0.0.0.255 host 192.168.30.30 eq www
access-list 110 permit tcp 192.168.10.0 0.0.0.255 host 192.168.30.30 eq 443
access-list 110 deny   ip 192.168.10.0 0.0.0.255 192.168.30.0 0.0.0.255
access-list 110 permit ip any any
```

---

## ✔ Why It Works Perfectly

### **1. VLAN 20 full server access**

Line 10 explicitly permits all Admin → Server traffic.

### **2. VLAN 10 restricted web access**

Lines 20 & 30 allow HTTP/HTTPS only
to **one specific host** (192.168.30.30).

### **3. All other VLAN 10 → VLAN 30 traffic blocked**

Line 40 denies the entire subnet.

### **4. ACL applied at the correct place**

You placed it **outbound on g0/0.30**, which is correct because:

* Both VLAN 10 and VLAN 20 traffic must exit through that interface to reach VLAN 30.
* Applying inbound on VLAN 10 alone would not catch VLAN 20 traffic.
* Applying inbound on VLAN 20 alone would not catch VLAN 10 traffic.

Outbound on VLAN 30 cleanly captures *both sources*.

---

### Phase 3 — Numbered Extended ACL Screenshots

**Ping Success from VLAN 20 → Servers**
![p3-admin-ping](./screenshots/p3-admin-ping.png)

**Ping Failure from VLAN 10 → Servers**
![p3-pc-ping](./screenshots/p3-pc-ping.png)

**ACL 110 Verification / Hit Counters**
![p3-show-access-list](./screenshots/p3-show-access-list.png)





## ✔ Phase 3 Testing Results

* VLAN 20 → Any server: **Allowed**
* VLAN 10 → 192.168.30.30 (HTTP/HTTPS): **Allowed**
* VLAN 10 → Any other server IP/protocol: **Blocked**
* All other routing: **Unaffected**

---

In this lab I demonstrated:

* Standard ACL logic and direction
* Extended named ACL for device protection
* Extended numbered ACL for server segmentation
* Correct interface placement
* Correct direction analysis
* Troubleshooting methodology
* Real-world reasoning identical to CCNA/CCNP exam expectations

---


