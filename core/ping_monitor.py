from ping3 import ping
import yaml
from datetime import datetime
import psutil
import os
import pathlib
import csv
import time
from typing import Dict, Any, List

# Default paths (can be overridden by config)
DEFAULT_CONFIG_PATH = "/conifg/config.yml"
DEFAULT_LOG_DIR = "/data/logs"
DEFAULT_LOG_FILE = "data/logs/ping_log.csv"


def load_config(config_path: str = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """
    Load YAML config and return a dict with defaults applied.

    Expected YAML keys (example):
      hosts:
        - 8.8.8.8
        - 192.168.1.1
      interval: 60          # seconds between polling rounds
      timeout: 2            # seconds timeout for ping
      count: -1             # number of rounds (-1 for infinite)
      log_file: data/logs/ping_log.csv

    Returns:
        config dict
    """
    path = pathlib.Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh) or {}

    # Apply defaults
    cfg.setdefault("hosts", [])
    cfg.setdefault("interval", 60)
    cfg.setdefault("timeout", 2)
    cfg.setdefault("count", -1)  # -1 means run forever
    cfg.setdefault("log_file", DEFAULT_LOG_FILE)

    # Normalize hosts to list of strings
    if isinstance(cfg["hosts"], str):
        cfg["hosts"] = [cfg["hosts"]]
    if not isinstance(cfg["hosts"], list):
        raise ValueError("`hosts` must be a list or string in config")

    return cfg


def ping_host(host: str, timeout: float = 2.0) -> Dict[str, Any]:
    """
    Ping a host using ping3.ping and gather lightweight system metrics.

    Returns a result dict:
      {
        "timestamp": "2025-01-01T12:00:00Z",
        "host": "8.8.8.8",
        "success": True/False,
        "rtt_ms": 12.3 or None,
        "cpu_percent": 1.2,
        "mem_percent": 42.5
      }
    """
    ts = datetime.utcnow().isoformat() + "Z"
    try:
        # ping returns round-trip time in seconds or None on failure
        rtt = ping(host, timeout=timeout)
    except Exception as e:
        # ping3 can raise on wrong input; treat as failure
        rtt = None

    success = rtt is not None
    rtt_ms = round(rtt * 1000, 3) if success else None

    # system metrics (useful context)
    try:
        cpu = psutil.cpu_percent(interval=0.0)
    except Exception:
        cpu = None
    try:
        mem = psutil.virtual_memory().percent
    except Exception:
        mem = None

    return {
        "timestamp": ts,
        "host": host,
        "success": success,
        "rtt_ms": rtt_ms,
        "cpu_percent": cpu,
        "mem_percent": mem,
    }


def log_result(result: Dict[str, Any], log_file: str = DEFAULT_LOG_FILE) -> None:
    """
    Append a result row to the CSV log file. Create directories/file headers if needed.
    CSV columns: timestamp,host,success,rtt_ms,cpu_percent,mem_percent
    """
    log_path = pathlib.Path(log_file)
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = log_path.exists()
    with open(log_path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if not file_exists:
            # write header
            writer.writerow(["timestamp", "host", "success", "rtt_ms", "cpu_percent", "mem_percent"])
        writer.writerow([
            result.get("timestamp"),
            result.get("host"),
            result.get("success"),
            result.get("rtt_ms"),
            result.get("cpu_percent"),
            result.get("mem_percent"),
        ])


def run_monitor(config: Dict[str, Any]) -> None:
    """
    Run the monitor loop using the provided config dict.

    Behavior:
      - Pings all hosts in config["hosts"] every config["interval"] seconds.
      - If config["count"] == -1, runs forever until KeyboardInterrupt.
      - Logs each ping result into config["log_file"].
    """
    hosts: List[str] = config.get("hosts", [])
    interval: int = int(config.get("interval", 60))
    timeout: float = float(config.get("timeout", 2))
    count: int = int(config.get("count", -1))
    log_file: str = str(config.get("log_file", DEFAULT_LOG_FILE))

    round_num = 0
    try:
        while True:
            if count != -1 and round_num >= count:
                break

            round_num += 1
            start_round = datetime.utcnow().isoformat() + "Z"
            print(f"[{start_round}] Round {round_num}: pinging {len(hosts)} hosts...")

            for host in hosts:
                res = ping_host(host, timeout=timeout)
                log_result(res, log_file=log_file)
                # Small console print for feedback
                if res["success"]:
                    print(f"  {host} -> {res['rtt_ms']} ms")
                else:
                    print(f"  {host} -> unreachable")

            # Sleep until next round (allow exit with Ctrl+C)
            if count == -1 or round_num < count:
                time.sleep(interval)
    except KeyboardInterrupt:
        print("Monitor stopped by user.")


if __name__ == "__main__":
    # Example quick-run: python core/ping_monitoring.py
    try:
        cfg = load_config()
    except Exception as e:
        print(f"Failed to load config: {e}")
        raise SystemExit(1)

    run_monitor(cfg)
