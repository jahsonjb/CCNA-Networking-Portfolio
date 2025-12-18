## Troubleshooting and Challenges Encountered

During the implementation of this automation lab, several real-world issues were encountered and resolved. These challenges reflect common problems faced when automating network devices, especially legacy infrastructure, and provided valuable hands-on troubleshooting experience.

### 1. SSH Key Exchange Algorithm Mismatch

**Issue:**
Initial SSH attempts to the Cisco IOS router failed with errors indicating no matching key exchange (KEX) algorithm.

**Cause:**
The Cisco IOSv image used in GNS3 supports only older SSH algorithms (`diffie-hellman-group14-sha1` and `ssh-rsa`). Modern Windows OpenSSH clients disable these algorithms by default.

**Resolution:**
A per-host SSH configuration was created to explicitly allow the required legacy algorithms **only for the lab router**, preserving secure defaults system-wide. This mirrors real-world handling of legacy network devices.

---

### 2. OpenSSH Client Availability on Windows

**Issue:**
SSH commands were initially unavailable or inconsistent.

**Cause:**
The OpenSSH Client was not fully installed or available in the system PATH.

**Resolution:**
The OpenSSH Client was verified and enabled via PowerShell, and the terminal session was restarted to ensure the SSH binary was accessible.

---

### 3. SSH Configuration File Path and Naming Issues

**Issue:**
SSH host aliases were not recognized, resulting in hostname resolution errors.

**Cause:**
The SSH configuration file either did not exist, was placed in the wrong directory, or was incorrectly named (for example, `config.txt` instead of `config`).

**Resolution:**
The correct `.ssh` directory under the user profile was confirmed, and a properly named `config` file was created and validated.

---

### 4. PowerShell Command Parsing Errors

**Issue:**
Attempts to execute SSH commands using quoted paths resulted in PowerShell parser errors.

**Cause:**
PowerShell handles quoted executables and arguments differently than Command Prompt.

**Resolution:**
The PowerShell call operator (`&`) and PowerShell environment variables (`$env:USERPROFILE`) were used to correctly execute SSH commands with custom options.

---

### 5. Python Script File Path Errors

**Issue:**
Python failed to locate the automation script when executed.

**Cause:**
The script was executed from a directory different than where it was saved.

**Resolution:**
A dedicated project directory was created, and all scripts were run from within that directory to maintain a consistent execution context.

---

### 6. Netmiko Module Not Installed

**Issue:**
Running the Python script resulted in a `ModuleNotFoundError` for Netmiko.

**Cause:**
Netmiko was not installed in the active Python environment.

**Resolution:**
Netmiko was installed using `python -m pip install netmiko`, ensuring it was installed for the correct Python interpreter.

---

### 7. Netmiko Authentication Failure Due to Incorrect Credentials

**Issue:**
Netmiko failed to authenticate to the router even though manual SSH access was working.

**Cause:**
The password defined in the Python script did not match the router’s local user credentials. This resulted in an authentication failure during automated login.

**Resolution:**
The credentials in the Netmiko device dictionary were corrected to match the router’s configured username and password. After updating the script, Netmiko authenticated successfully and executed commands as expected.

---

## Outcome

After resolving these issues, the automation environment functioned reliably and demonstrated:

* Secure, scoped SSH compatibility handling
* Successful programmatic authentication using Netmiko
* Automated retrieval and storage of router configurations
* A repeatable automation workflow suitable for expansion

These troubleshooting steps reflect realistic challenges encountered in enterprise network environments and demonstrate practical problem-solving skills beyond basic lab execution.
