#before we start hadchi 3amr comment bach n39l 3la kola 7ja hh


from ping3 import ping #import the ping func
import yaml #to read the config.yaml and will convert YAML  to py dictionary
from datetime import datetime
import psutil #gives system information like CPU and RAM usage.
import pathlib
import csv
import time
from typing import Dict, Any, List

DEFAULT_CONFIG_PATH = "/conifg/config.yaml"
DEFAULT_LOG_FILE = "/data/logs/ping_log.csv"

def load_config(config_path=DEFAULT_CONFIG_PATH):
    path = pathlib.Path(config_path) #hadchi liya bach mansach hh : we used the pathlib to turn the sting to path object

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}") #hadi gha debug bach ila mal9inach l path 

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) #i'v used the yaml to turn the config to python dectionary

    if config is None:
        config = {} # again hadi gha debug
#had part kaml for setting default if i didn't exists
    config.setdefault("hosts", [])
    config.setdefault("interval", 60)
    config.setdefault("timeout", 2)
    config.setdefault("count", -1)
    config.setdefault("log_file", DEFAULT_LOG_FILE)

    if isinstance(config["hosts"], str):
        config["hosts"] = [config["hosts"]]

    if not isinstance(config["hosts"], list):
        raise ValueError("hosts must be a list or a string")

    return config


#next function : for this func we wanna turn the input into like output 
#kifach b7al haka  : 
"""
host = "8.8.8.8"
l hadi 
{
    "timestamp": "2025-01-01T12:00:00Z",
    "host": "8.8.8.8",
    "success": True,
    "rtt_ms": 23.4
}

"""

def ping_host(host, timeout=2):
    timestamp = datetime.utcnow().isoformat() + "Z" #hadi bach n3rfo lw9t 
#basic try/except consept ila l9a resonse kay storiha f seccess 
    try:
        response = ping(host, timeout=timeout)
    except Exception:
        response = None

    success = response is not None

    if success:
        rtt_ms = round(response * 1000, 3)
    else:
        rtt_ms = None

    return {
        "timestamp": timestamp,
        "host": host,
        "success": success,
        "rtt_ms": rtt_ms,
    }

def run_monitor(config):
    hosts = config["hosts"]
    interval = config["interval"]
    timeout = config["timeout"]
    count = config["count"]
    log_file = config["log_file"]

    round_number = 0

    try:
        while True:
            if count != -1 and round_number >= count:
                break

            round_number += 1
            print(f"--- Ping round {round_number} ---")

            for host in hosts:
                result = ping_host(host, timeout)
                log_result(result, log_file)

                if result["success"]:
                    print(f"{host} reachable ({result['rtt_ms']} ms)")
                else:
                    print(f"{host} unreachable")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("Ping monitoring stopped.")
