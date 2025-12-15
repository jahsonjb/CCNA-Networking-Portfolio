# 🔐 Switch Port Security Lab — Access Layer Enforcement & Recovery

## Overview

In this lab, I demonstrate **enterprise access-layer port security** using a single Layer 2 switch and multiple endpoints. The focus is on how switches enforce MAC-based access control, how different **violation modes** behave operationally, and how improper recovery can lead to repeated outages.

This lab emphasizes:
- Realistic access-layer behavior
- Security vs. availability trade-offs
- Troubleshooting err-disabled ports
- Clear cause → effect → validation

All behavior occurs strictly at **Layer 2**. No routing or higher-layer controls are involved.

---

## Topology Summary

**Devices**
- **L2-SW-Access** — Layer 2 access switch  
- **PC1** — VPCS  
- **Linux-PC2** — Alpine Linux  
- **PC3** — VPCS  

**Tooling Note**

VPCS does not allow manual MAC address modification. To accurately test MAC-based security controls and violation behavior, I used Linux hosts (Alpine Linux) for phases that required MAC address changes.

---

**VLAN Design**
- VLAN 10 — User access VLAN  
- Subnet: `192.168.10.0/24`

**IP Addressing**
- PC1: `192.168.10.10`
- Linux-PC2: `192.168.10.20`
- PC3: `192.168.10.30`

**Switch Ports**
- `Gi0/0` → PC1  
- `Gi0/1` → Linux-PC2  
- `Gi0/2` → PC3  

All switch ports were configured as access ports in **VLAN 10**.

---

## Phase 1 — Baseline Connectivity (No Security)

### Objective
Verify normal Layer 2 connectivity before applying any security controls.

### Actions
- Assigned `Gi0/0`, `Gi0/1`, and `Gi0/2` to VLAN 10
- Configured static IP addresses on all hosts
- Verified end-to-end connectivity between PC1, Linux-PC2, and PC3

### Validation
- ICMP traffic succeeded between all hosts
- MAC addresses were dynamically learned in the CAM table
- No port security features were enabled

This phase established a clean baseline for comparison.

---

## Phase 2 — Sticky MAC Learning

### Objective
Demonstrate **dynamic MAC authorization** using sticky port security.

### Actions
- Enabled port security on `Gi0/0`
- Enabled **sticky MAC learning**
- Generated traffic from PC1

### Observed Behavior
- The switch dynamically learned PC1’s MAC address
- The learned MAC was:
  - Written into the running configuration
  - Converted into a **STATIC** CAM table entry
- The interface remained in a secure-up state

### Verification
I validated behavior using:
- Port security status commands
- The running configuration
- The MAC address table

### Key Insight
With sticky MAC learning enabled, the switch dynamically learned the first host’s MAC address, converted it into a static CAM entry, and enforced single-host access on the port. Although the MAC appears as **STATIC** in the CAM table, it was learned dynamically and persisted by the switch for enforcement.

---

## Phase 3 — Port Security Violation Modes

In this phase, I tested how different **violation modes** affect enforcement, visibility, and availability when an unauthorized MAC address appears.

### Test Setup
- Port security and sticky learning were already enabled on `Gi0/1`
- Linux-PC2 was connected to `Gi0/1`
- Initial connectivity was verified

I manually changed the MAC address on Linux-PC2 from:

```

0c:42:e2:c7:00:00

```

to:

```

00:11:22:33:44:55

```

---

### 3.1 Protect Mode — Silent Enforcement

**Expected Behavior**
- Unauthorized traffic is dropped
- No logs or counters
- Interface remains up

**Observed Results**
- ICMP traffic failed after the MAC change
- The interface remained up
- No violations were logged

**Conclusion**
Protect mode enforces security silently but provides no operational visibility.

---

### 3.2 Restrict Mode — Enforcement with Visibility

**Expected Behavior**
- Unauthorized traffic is dropped
- Violation counters increment
- Interface remains up

**Observed Results**
- ICMP traffic failed
- Violation count increased
- The interface remained up and operational

**Conclusion**
Restrict mode provides enforcement with visibility and is commonly used in enterprise access networks.

---

### 3.3 Shutdown Mode — Maximum Enforcement (Default)

**Expected Behavior**
- Interface transitions to err-disabled
- All traffic is blocked
- Manual recovery is required

**Observed Results**
- ICMP traffic failed
- Violation count increased
- `Gi0/1` transitioned to an err-disabled state

**Conclusion**
Shutdown mode provides maximum security at the cost of immediate service disruption.

---

This phase demonstrated the behavioral and operational differences between **protect**, **restrict**, and **shutdown** violation modes, highlighting the trade-offs between security enforcement, visibility, and service availability.

---

## Phase 4 — Recovery & Troubleshooting

### Scenario
A user reports sudden loss of network connectivity.

### Actions Taken
- Identified the err-disabled interface
- Administratively shut down `Gi0/1`
- Issued `no shutdown` to restore the port

### Observed Behavior
- The interface came back up temporarily
- The interface transitioned back to err-disabled shortly afterward

### Root Cause
- The unauthorized MAC address was still present on Linux-PC2
- The violation mode remained set to shutdown

### Key Lesson
Recovering a port without addressing the **underlying policy violation** results in repeated outages.

---

## Key Takeaways

This lab reflects real enterprise access-layer incidents such as desk moves, device swaps, and unintended MAC changes. Through this lab, I learned how access-layer port security directly impacts both network security and user availability. Sticky MAC learning provides dynamic authorization with persistent enforcement, while violation modes introduce clear trade-offs between visibility and service disruption. Testing protect, restrict, and shutdown modes reinforced how small Layer 2 decisions can quickly lead to real outages if not designed and recovered intentionally.

---

## Skills Demonstrated

- Layer 2 access design
- Port security configuration and enforcement
- Sticky MAC learning
- Violation mode analysis
- Err-disabled troubleshooting
- Operational recovery logic
- Validation using diagnostic commands

---

## Status

Completed and validated.  
This lab is part of my ongoing **enterprise switching and network security portfolio**.
```

---
