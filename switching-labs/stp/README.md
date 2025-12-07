# **Spanning Tree Protocol (STP) – Root Bridge, Loop Simulation, and BPDU Guard Lab**

This lab demonstrates Spanning Tree Protocol behavior in a redundant Layer 2 topology, including root bridge election, forcing a new root, observing STP recalculation after introducing a physical loop, and verifying BPDU Guard protection on access ports. The topology is implemented in Cisco Packet Tracer using three distribution switches and one additional access-layer switch.

---

## **1. Lab Objectives**

This lab focuses on four core STP concepts:

1. Observe the initial STP Root Bridge election process.
2. Manually force a different switch to become the Root Bridge by adjusting STP priority.
3. Create a Layer 2 loop and examine how STP responds by blocking redundant links.
4. Enable BPDU Guard on an access interface and verify automatic err-disable behavior when a switch is connected.

These tasks reinforce how STP maintains a loop-free topology, how root placement influences forwarding paths, and how BPDU Guard protects against misconfigurations and rogue switches.

---

## **2. Topology Overview**

Three multilayer switches (SW1, SW2, SW3) form a triangle topology with redundant GigabitEthernet trunk links. SW4 acts as an access-layer switch for BPDU Guard testing.

```
        SW1
     /        \
SW2 ---------- SW3
       (triangle loop)

SW4 connected to SW2 Fa0/1 (BPDU Guard test)
```

Link characteristics:

* Trunk ports: GigabitEthernet0/1 and GigabitEthernet0/2 on all core switches
* BPDU Guard test port: FastEthernet0/1 on SW2
* Redundant link added: SW1 Fa0/1 to SW3 Fa0/1

---

## **3. STP Configuration Summary**

All core switches run PVST+ by default in Packet Tracer.

Example core configuration (applied across switches):

```
spanning-tree mode pvst
interface g0/1
 switchport mode trunk
interface g0/2
 switchport mode trunk
```

---

## **4. Part 1 – Initial Root Bridge Election**

Before modifying priorities, the output from:

```
show spanning-tree vlan 1
```

showed that **SW3** was elected as the Root Bridge. This occurred because SW3 had the lowest Bridge ID (priority + MAC address).

Initial expected behavior:

* SW3: All designated ports
* SW1 and SW2: One root port each, one blocked/designated port depending on path cost

---

## **5. Part 2 – Forcing a New Root Bridge (SW2)**

To take control of the STP topology and make SW2 the Root Bridge, its STP priority was lowered:

```
spanning-tree vlan 1 priority 4096
```

After convergence:

* SW2 became the Root Bridge
* All SW2 ports transitioned to Designated state
* SW1 and SW3 recalculated their Root Ports based on lowest path cost to SW2
* Ports facing redundant paths transitioned appropriately (Alternate/Blocking)

Verification:

```
show spanning-tree vlan 1
show spanning-tree root
```

---

## **6. Part 3 – Loop Simulation via Redundant Link**

A redundant link was added between **SW1 Fa0/1** and **SW3 Fa0/1**, intentionally introducing a Layer 2 loop.

STP responded by recalculating the topology:

* Only one path remained active between each segment
* One or more interfaces on SW1 or SW3 transitioned into Alternate/Blocking state
* No broadcast storm occurred due to proper STP operation

This demonstrates how STP dynamically prevents loops by blocking the appropriate port based on port cost and bridge ID.

---

## **7. Part 4 – BPDU Guard Err-Disable Test**

BPDU Guard was enabled on an access port on SW2:

```
interface fa0/1
 switchport mode access
 spanning-tree bpduguard enable
```

When SW4 was connected to SW2 Fa0/1:

* The port immediately detected incoming BPDUs
* SW2 safeguarded the topology by placing the interface into **err-disabled** state

Verification:

```
show interfaces status err-disabled
show spanning-tree interface fa0/1 detail
```

This behavior confirms that BPDU Guard effectively prevents unauthorized or accidental switch connections on access ports.

---

## **8. Key STP Behaviors Observed**

* STP Root Bridge election is determined by lowest Bridge ID.
* Lowering priority forces deterministic control of the Root Bridge.
* Loops created by redundant paths are mitigated automatically by STP blocking.
* BPDU Guard prevents harmful topology changes at the edge by disabling ports receiving BPDUs.

---

## **9. Screenshots for lab**

1. Topology diagram
2. `show spanning-tree vlan 1` before forcing SW2 as root
3. `show spanning-tree vlan 1` after SW2 becomes root
4. STP output after adding redundant link (showing Alternate/Blocking ports)
5. Interface err-disable after BPDU Guard trigger
6. Port configuration samples (trunks, BPDU Guard)

---

## **10. Files Included in This Folder**

* Packet Tracer `.pkt` project file (uploaded separately)
* Screenshots folder
* README.md (this file)
