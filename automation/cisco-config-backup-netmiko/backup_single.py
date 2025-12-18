from netmiko import ConnectHandler
from datetime import datetime
from pathlib import Path
import logging

# ---------- Settings ----------
DEVICE = {
    "device_type": "cisco_ios",
    "host": "192.168.0.133",
    "username": "admin",
    "password": "cisco123",
    "use_keys": False,
    "allow_agent": False,
}

DEVICE_NAME = "R1"  # used for folder naming
BACKUP_DIR = Path("backups") / DEVICE_NAME
LOG_DIR = Path("logs")
# -----------------------------

def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_DIR / "backup.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

def save_backup(text: str) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_file = BACKUP_DIR / f"running-config_{timestamp}.txt"
    out_file.write_text(text, encoding="utf-8")
    return out_file

def main() -> None:
    setup_logging()
    logging.info("Starting backup for %s (%s)", DEVICE_NAME, DEVICE["host"])

    conn = ConnectHandler(**DEVICE)

    # Pull running-config
    running = conn.send_command("show running-config", read_timeout=120)
    conn.disconnect()

    out_file = save_backup(running)
    logging.info("Backup complete. Saved to %s", out_file)

    print(f"Backup complete. Saved to: {out_file}")

if __name__ == "__main__":
    main()
