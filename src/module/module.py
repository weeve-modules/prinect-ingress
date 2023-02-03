"""
This file implements module's main logic.
Data inputting should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from api.send_data import send_data
from .params import PARAMS
import requests
import time

log = getLogger("module")


def module_main():
    """
    Implements module's main logic for inputting data.
    Function description should not be modified.
    """

    log.debug("Inputting data...")

    try:
        resource_map = {
            "device data": "",
            "activity data": "activity",
            "consumption data": "consumption",
        }

        resource_url = resource_map.get(PARAMS["RESOURCE"], None)
        if resource_url is None:
            raise ValueError(
                f"Invalid method: {PARAMS['RESOURCE']}. Allowed resource values are: {', '.join(resource_map.keys())}"
            )

        full_url = f"{PARAMS['BASE_URL']}/{PARAMS['DEVICE_ID']}"
        if resource_url:
            full_url += f"/{resource_url}"

        while True:
            if (
                resource_url == "activity"
            ):  # so far it's the only resource that supports pagination
                data = fetch_all_pages(full_url, "activities")
            else:
                data = fetch_data(full_url)

            if not data:
                log.error("Failed to fetch data from URL: %s" % full_url)
            else:
                log.debug("Received data: %s", data)

                # send data to the next module
                send_error = send_data(data)

                if send_error:
                    log.error(send_error)
                else:
                    log.debug("Data sent successfully.")

            time.sleep(PARAMS["INTERVAL"])

    except Exception as e:
        log.error(f"Exception in the module business logic: {e}")


def fetch_data(url):
    response = requests.get(url, auth=(PARAMS["USERNAME"], PARAMS["PASSWORD"]))
    return validate_response(response)


def fetch_page(url, page_number=0, page_size=100):
    response = requests.get(
        url,
        auth=(PARAMS["USERNAME"], PARAMS["PASSWORD"]),
        params={"page": page_number, "pagesize": page_size},
    )
    return validate_response(response)


def fetch_all_pages(url, data_key, page_size=100):
    page_number = 0
    all_data = {}
    while True:
        data = fetch_page(url, page_number, page_size)
        if not data:
            return None
        merge_jsons(all_data, data)
        if len(data[data_key]) < page_size:
            break
        page_number += 1
    return all_data


def validate_response(response: requests.Response):
    if response.status_code == 200:
        data = response.json()
        if data.get("error"):
            log.error(
                "Failed to fetch data. Error code: %s. Message: %s"
                % (data["error"]["code"], data["error"]["message"])
            )
            return None
        else:
            return data
    elif response.status_code == 401:
        log.error("Failed to fetch data. Invalid credentials.")
        return None
    elif response.status_code == 403:
        log.error(
            "Failed to fetch data. Forbidden. User doesn't have access rights for the resource."
        )
        return None
    else:
        log.error("Failed to fetch data. Response code: %s" % response.status_code)
        return None


def merge_jsons(json1, json2):
    for key in json2:
        if key in json1:
            if isinstance(json1[key], dict) and isinstance(json2[key], dict):
                json1[key] = merge_jsons(json1[key], json2[key])
            elif isinstance(json1[key], list) and isinstance(json2[key], list):
                json1[key].extend(json2[key])
            elif json1[key] == json2[key]:
                pass
            else:
                json1[key] = [json1[key], json2[key]]
        else:
            json1[key] = json2[key]
    return json1
