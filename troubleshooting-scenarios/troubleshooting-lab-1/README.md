# **🔎 Phase 1 — Incorrect Default Gateway (L3 Misconfiguration Test)**

In this first phase, I intentionally misconfigured the **Layer 3 host settings** to break inter-VLAN communication. Even though my router-on-a-stick setup on R1 was correct, the host in VLAN 10 couldn’t reach VLAN 20.
My goal here was to confirm that an incorrect default gateway causes packets to fail **before they ever reach the router**, and that fixing it restores normal routing.

---

## **🎯 Objective**

* Show how my incorrect default gateway prevented VLAN 10 from reaching VLAN 20.
* Observe ARP behavior, packet flow, and ICMP failure patterns.
* Confirm that correcting the gateway allows routing via `Gig0/0/0.10`.

---

## **🧪 Test Setup**

### **VLAN 10 Host**

* IP: `192.168.10.x`
* Mask: `255.255.255.0`
* **Incorrect Default Gateway I configured:** `192.168.10.15` ❌
  *(It should have been `192.168.10.1`.)*

### **Router-on-a-Stick on R1 (Gig0/0/0 trunk)**

* `Gig0/0/0.10` → `192.168.10.1`
* `Gig0/0/0.20` → `192.168.20.1`
* `Gig0/0/0.30` → `192.168.30.1`

### **Test**

Ping from VLAN 10 → VLAN 20 (`192.168.20.x`).

---

## **🔍 Observed Behavior**

Once I configured the wrong gateway:

### ❌ **My ping from VLAN 10 to VLAN 20 failed.**

Here's why:

1. The host ARPed for `192.168.10.15`.
2. Nothing on the network owned that address.
3. ARP never resolved.
4. No ICMP packet ever reached the router.
5. Routing never occurred.

This confirmed the issue was purely a local L3 configuration problem.

---

## **🛠️ Fix**

I corrected the default gateway to:

```text
192.168.10.1
```

Once I did:

* ARP resolved immediately.
* ICMP Echo Requests reached `Gig0/0/0.10`.
* R1 routed the packets to VLAN 20.
* Replies came back through the correct interface.

### ✅ **Ping succeeded.**

---

## **📌 Key Takeaway (Phase 1)**

A wrong default gateway stops packets at the source. Before I troubleshoot VLANs, trunks, or ACLs, I always validate:

* IP address
* Subnet mask
* Default gateway

![Topology](./screenshots/topology.png) Topology

![Phase 1 PC Ping Fail](./screenshots/p1-pc-ping-fail.png) Phase 1 PC Ping Fail

![Phase 1 CPT Simulation Mode](./screenshots/p1-cpt-sim-mode.png) Phase 1 CPT Simulation Mode

![Phase 1 Wrong Gateway](./screenshots/p1-pc-wrong-gateway.png) Phase 1 Wrong Gateway

![Phase 1 Ping Success](./screenshots/p1-pc-ping-success.png) Phase 1 Ping Success


---

---

# **🔎 Phase 2 — Wrong VLAN Assignment on Access Port (L2 Misplacement Test)**

In this phase, I tested a **Layer 2 VLAN assignment error**. I gave the host correct L3 settings, but I intentionally placed its switchport into the wrong VLAN. This created a totally different failure pattern: packets looked like they were reaching their destination in simulation mode, but replies never made it back.

This is one of the most common real-world router-on-a-stick mistakes.

---

## **🎯 Objective**

I wanted to show how incorrect VLAN membership breaks inter-VLAN routing even when:

* The host IP is correct
* The mask is correct
* The gateway is correct
* The router subinterfaces are correct

---

## **🧪 Test Setup**

### Intended VLAN: VLAN 10

* IP: `192.168.10.x`
* Mask: `255.255.255.0`
* Gateway: `192.168.10.1`

### Intentional Misconfiguration on Switch

```text
interface Fa0/1
 switchport mode access
 switchport access vlan 30   <-- ❌ wrong VLAN
```

### R1 Subinterfaces

* `.10` → `192.168.10.1`
* `.20` → `192.168.20.1`
* `.30` → `192.168.30.1`

---

## **🔍 Observed Behavior**

### ❌ VLAN 10 → VLAN 20 ping failed

### ✅ VLAN 30 → VLAN 20 ping succeeded

In simulation mode, I actually saw ICMP Echo Requests arriving in VLAN 20 — but the pings still timed out.

---

## **🧬 Root Cause: Asymmetric Path Failure**

Even though the host had correct L3 settings, I had placed it in **VLAN 30**.

### **Forward path worked**

The ARP and ICMP requests were tagged as VLAN 30. R1 received them on `.30` and forwarded them normally.

### **Return path failed**

When R1 sent replies back, it used the routing table:

* “To reach VLAN 10 hosts → send via `Gig0/0/0.10`”

But my host was stuck in VLAN 30, so the reply evaporated.

### Result:

* Echo Request succeeds
* Echo Reply is lost
* Ping fails

A textbook wrong-VLAN symptom.

---

## **🛠️ Fix**

I corrected the port:

```text
interface Fa0/1
 switchport access vlan 10
```

After that:

* ARP hit the correct subinterface
* Replies returned through the correct VLAN
* Ping succeeded normally

![Phase 2 Show Switch Interface](./screenshots/p2-show-sw-int.png) Phase 2 Show Switch Interface

![Phase 2 VLAN Brief](./screenshots/p2-vlan-brief.png) Phase 2 VLAN Brief

![Phase 2 VLAN 10 Ping Fail](./screenshots/p2-vlan10-pingfail.png) Phase 2 VLAN 10 Ping Fail

![Phase 2 Ping Success #1](./screenshots/p2-ping-success.png) Phase 2 Ping Success

![Phase 2 Switchport Correction](./screenshots/p2-correct-sw-config.png) Phase 2 Switchport Correction

---

## **📌 Key Takeaway (Phase 2)**

A wrong VLAN assignment produces:

* Successful outbound ICMP
* Failed inbound ICMP
* “Half-working” traffic that looks like routing failure

This reinforced why I always verify access VLANs early.

---

---

# **🔎 Phase 3 — Missing OSPF Network Statement (R1 Not Advertising VLAN 20)**

In this phase, I explored a **Layer 3 routing protocol failure** caused by an incomplete OSPF configuration. All VLANs, subinterfaces, and local routing worked fine on R1, but because I neglected to advertise VLAN 20 in OSPF, R2 and R3 never learned that network.

This produced a realistic **partial reachability** issue.

---

## **🎯 Objective**

I wanted to observe how failing to advertise VLAN 20 into OSPF affects:

* Route visibility on R2 and R3
* Selective ping failures
* LSDB health despite incomplete routing
* Troubleshooting complexity

---

## **🧪 Topology Setup**

All routers run OSPF Area 0.

### R1 VLAN Gateways

* 192.168.10.1
* 192.168.20.1
* 192.168.30.1

### R1–R2 Link

* `10.0.0.4/30`

### R2–R3 Link

* `10.0.0.0/30`

---

## **🚫 Intentional Omission**

On R1, I intentionally left out VLAN 20:

```text
router ospf 1
 network 192.168.10.0 0.0.0.255 area 0
 ! Missing:
 ! network 192.168.20.0 0.0.0.255 area 0
 network 192.168.30.0 0.0.0.255 area 0
 network 10.0.0.4 0.0.0.3 area 0
```

Adjacency stayed up.
VLAN 10 and 30 were reachable.
VLAN 20 was invisible.

---

## **🔍 Observed Behavior**

### From R2 and R3:

* I could ping `192.168.10.1` ✔️
* I could ping `192.168.30.1` ✔️
* I **could NOT** ping `192.168.20.1` ❌

Checking routes:

```text
R2# show ip route 192.168.20.0
% Network not in table
```

Exactly what I expected.

---

## **🧬 Why This Happens**

OSPF does **not** auto-advertise connected networks.
It only advertises networks I explicitly configure.

Since VLAN 20 wasn’t included:

* R1 never injected the 192.168.20.0/24 LSA
* R2 never learned it
* R3 never learned it
* Pings failed from both routers

Local routing still worked fine on R1.

---

## **🛠️ Fix**

I added:

```text
network 192.168.20.0 0.0.0.255 area 0
```

Immediately:

* R2 and R3 re-learned the route
* OSPF tables updated
* Pings to `192.168.20.1` succeeded again

![Phase 3 R2 Ping Fail](./screenshots/p3-r2-ping-fail.png) Phase 3 R2 Ping Fail

![Phase 3 Missing Network](./screenshots/p3-missing-network.png) Phase 3 Missing Network

![Phase 3 R2 Ping Success](./screenshots/p3-r2-ping-success.png) Phase 3 R2 Ping Success

---

## **📌 Key Takeaway (Phase 3)**

A missing OSPF network statement creates **partial routing failures** that look like ACL or inter-VLAN issues. I now always check:

* Running config
* OSPF interfaces
* LSDB
* OSPF routes

before digging deeper.

---

---

# **🔎 Phase 4 — Shutting Down Gig0/0/0 on R1 (VLAN Gateway Failure Test)**

For this phase, I tested what happens when I shut down the **router-on-a-stick parent interface** on R1. My OSPF adjacency with R2 remained up because it's on `Gig0/0/1`, not on `Gig0/0/0`.

This produced a realistic scenario where routing between routers was fine, but all VLAN gateways on R1 disappeared.

---

## **🎯 Objective**

I wanted to disable R1’s VLAN gateway interface and observe:

* All subinterfaces going down
* OSPF LSAs being withdrawn
* VLAN routes disappearing from R2 and R3
* Pings to VLAN gateways failing

All while the R1↔R2 OSPF adjacency stayed fully operational.

---

## **🧪 Test Setup**

### Router-on-a-Stick on R1

Subinterfaces:

* `Gig0/0/0.10` — 192.168.10.1
* `Gig0/0/0.20` — 192.168.20.1
* `Gig0/0/0.30` — 192.168.30.1

### OSPF Adjacency Link

* `Gig0/0/1` → R2
* `10.0.0.4/30`

---

## **🚫 Intentional Failure**

I shut down the parent interface:

```text
interface Gig0/0/0
 shutdown
```

This immediately caused every VLAN gateway to go down.

---

## **🔍 Observed Behavior**

### ❌ From R3:

```text
ping 192.168.30.1
```

Timed out, as expected.

### R2 and R3 Routing Tables:

All OSPF routes for VLAN 10/20/30 were withdrawn.

### OSPF Adjacency:

Still **FULL**, because adjacency didn't depend on Gig0/0/0.

---

## **🧬 Why the Ping Failed**

1. Shutting down Gig0/0/0 brought **all subinterfaces down**.
2. R1 could no longer own any 192.168.x.1 addresses.
3. R1 withdrew those networks from OSPF.
4. R2 and R3 purged them from their routing tables.
5. R3 had no route to 192.168.30.1 → ping failed instantly.

---

## **🛠️ Fix**

I restored the interface:

```text
interface Gig0/0/0
 no shutdown
```

Immediately:

* All subinterfaces came back online
* R1 re-advertised its VLAN networks
* R2 and R3 reinstalled routes
* My ping succeeded again

![Phase 4 R1 Shut Interface](./screenshots/p4-r1-shut-int.png) Phase 4 R1 Shut Interface

![Phase 4 R3 Ping Fail](./screenshots/p4-r3-ping-fail.png) Phase 4 R3 Ping Fail

![Phase 4 R3 Ping Success](./screenshots/p4-r3-ping-success.png) Phase 4 R3 Ping Success


---

## **📌 Key Takeaway (Phase 4)**

This phase reinforced an important lesson:
Even if routing protocol adjacencies stay up, **interface failures can silently remove entire network segments** from the routing domain.

Before assuming ACLs or OSPF issues, I always check:

* Interface state
* Subinterface state
* OSPF LSAs
* Routing table entries


---

