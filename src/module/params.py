from os import getenv

PARAMS = {
    "BASE_URL": getenv("BASE_URL", ""),
    "USERNAME": getenv("USERNAME", ""),
    "PASSWORD": getenv("PASSWORD", ""),
    "DEVICE_ID": getenv("DEVICE_ID", ""),
    "RESOURCE": getenv("RESOURCE", ""),
    "INTERVAL": int(getenv("INTERVAL", 5)),
}
