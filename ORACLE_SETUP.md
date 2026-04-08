# Oracle Cloud Instance Polling Setup

## Goal
Automatically poll Oracle Cloud's API every 5 minutes to snag a free-tier ARM instance (VM.Standard.A1.Flex — 4 OCPUs, 24GB RAM, Ubuntu 22.04 aarch64) in us-ashburn-1. The 8440p runs this script in the background until capacity opens up, at which point the trading system will be migrated there permanently.

---

## Machine
- **HP EliteBook 8440p** running Ubuntu Server 22.04
- Accessed remotely via SSH: `ssh hp8440p@100.127.245.21`
- Sleep/hibernate permanently disabled (set up separately for trading bot)

---

## What Was Set Up

### 1. OCI CLI Installed
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
exec -l $SHELL
oci --version  # confirmed 3.78.0
```

### 2. OCI API Key
- Generated key pair in Oracle Console → My Profile → API Keys → Add API Key
- Private key downloaded and SCP'd to the 8440p:
```bash
scp ~/NEW\ OracleCloudSSHKey/shriyans.singh2006@gmail.com-2026-04-08T18_01_48.456Z.pem hp8440p@100.127.245.21:~/.oci/oci_api_key.pem
```

### 3. OCI CLI Configured
```bash
mkdir -p ~/.oci
oci setup config
# Region: us-ashburn-1 (option 71)
# Key: ~/.oci/oci_api_key.pem
# Did NOT generate new key (used existing)
```

### 4. Permissions Fixed
```bash
oci setup repair-file-permissions --file /home/hp8440p/.oci/oci_api_key.pem
```

### 5. SSH Key Generated on 8440p
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
```

### 6. Correct ARM Image OCID Found
```bash
oci compute image list \
  --compartment-id ocid1.tenancy.oc1..aaaaaaaajlwctfegltugquuonz6a7reltepwfohzcm3nzmgynbwcfynvgnka \
  --operating-system "Canonical Ubuntu" \
  --operating-system-version "22.04" \
  --shape VM.Standard.A1.Flex \
  --output table \
  --query "data[*].{Name:\"display-name\", OCID:id}"
```
## Link to image ocid list based on region
### https://docs.oracle.com/en-us/iaas/images/ubuntu-2204/
**Correct image**: `Canonical-Ubuntu-22.04-aarch64-2026.02.28-0`  
**Image OCID**: `ocid1.image.oc1.iad.aaaaaaaahk7zm5s5gv4imyzgui5c77uzfpn72blj3od2icmohxzv3zpuiikq`

> Note: The x86 image OCID (from Oracle's docs page) was tried first and failed with `InvalidParameter`. Always use the aarch64 image for A1 Flex.

---

## Key OCIDs

| Resource | OCID |
|---|---|
| Tenancy | `ocid1.tenancy.oc1..aaaaaaaajlwctfegltugquuonz6a7reltepwfohzcm3nzmgynbwcfynvgnka` |
| Public Subnet | `ocid1.subnet.oc1.iad.aaaaaaaa2r7kb4gztjaiilkwftw4vuya5ktjzlrpvnmwagsbooc4hicjouta` |
| Image (aarch64) | `ocid1.image.oc1.iad.aaaaaaaahk7zm5s5gv4imyzgui5c77uzfpn72blj3od2icmohxzv3zpuiikq` |
| Region | `us-ashburn-1` |
| Availability Domains | AD-1, AD-2, AD-3 (all tried each cycle) |

---

## Polling Script
Located at: `/home/hp8440p/oracle_poller.py`  
Log file at: `/home/hp8440p/oracle_poller.log`

- Tries all 3 availability domains each cycle
- Catches "Out of host capacity" errors and retries
- Catches connection errors (e.g. WiFi blip at ~3 AM) and retries
- Sleeps 300 seconds (5 minutes) between full cycles
- Logs every attempt with timestamp
- Logs SUCCESS with instance ID when capacity is found

---

## Running the Script

### Start (in tmux)
```bash
tmux new -s oracle-setup
python3 ~/oracle_poller.py
```

### Check log (any time)
```bash
tail -f ~/oracle_poller.log
```

### Reattach after disconnect
```bash
tmux attach -t oracle-setup
```

### Switch tmux windows
- `Ctrl+B` then `0` — script
- `Ctrl+B` then `1` — log
- `Ctrl+B` then `2` — regular terminal
- `Ctrl+B` then `C` — new window
- `Ctrl+B` then `D` — detach (leaves everything running)

---

## Auto-Restart on Reboot
Added to crontab (`crontab -e`):
```
@reboot tmux new-session -d -s oracle-setup 'python3 /home/hp8440p/oracle_poller.py'
```

---

## What Happens When It Succeeds
The log will show:
```
SUCCESS - Instance launched in YoIh:US-ASHBURN-AD-X
Instance ID: ocid1.instance.oc1...
```

Next steps after success:
1. SSH into the new Oracle instance using the 8440p's key (`~/.ssh/id_rsa`)
2. Install trading system dependencies
3. Transfer trading system code from GitHub
4. Set up APScheduler, Streamlit, and all bots
5. Retire the 8440p as the trading system host

---

## Known Issues / Notes
- `alpaca-trade-api` has a urllib3 version conflict after OCI install — does not affect the poller, fix before running trading bot on 8440p
- WiFi on the 8440p cuts out ~3 AM for ~3 minutes — handled automatically by the retry loop
- Oracle ARM capacity in Ashburn is highly contested — script may run for days before succeeding
- OCI rate limits: keep retry interval at 3-5+ minutes minimum