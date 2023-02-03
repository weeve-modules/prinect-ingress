# Prinect Ingress

|           |                                                                                       |
| --------- | ------------------------------------------------------------------------------------- |
| Name      | Prinect Ingress                                                                       |
| Version   | v1.0.0                                                                                |
| DockerHub | [weevenetwork/prinect-ingress](https://hub.docker.com/r/weevenetwork/prinect-ingress) |
| authors   | Paul Gaiduk                                                                           |

## Table of Content

- [Prinect Ingress](#prinect-ingress)
  - [Table of Content](#table-of-content)
  - [Description](#description)
  - [Environment Variables](#environment-variables)
    - [Module Specific](#module-specific)
    - [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
  - [Dependencies](#dependencies)
  - [Input](#input)
  - [Output](#output)

## Description

This module makes periodic requests to Prinect API and forwards the response to the next module.

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Environment Variables | type   | Description                                |
| --------------------- | ------ | ------------------------------------------ |
| BASE_URL              | string | Base URL for the API. Ends with /rest      |
| USERNAME              | string | Username for the API.                      |
| PASSWORD              | string | Password for the API.                      |
| DEVICE_ID             | string | ID of the device you want the data for.    |
| RESOURCE              | string | Resource you want the data for.            |
| INTERVAL              | string | Interval in seconds between each API call. |


### Set by the weeve Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

| Environment Variables | type   | Description                                                                                          |
| --------------------- | ------ | ---------------------------------------------------------------------------------------------------- |
| MODULE_NAME           | string | Name of the module                                                                                   |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output)                                                       |
| EGRESS_URLS           | string | HTTP ReST endpoint for the next module                                                               |
| LOG_LEVEL             | string | Allowed log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Refer to `logging` package documentation. |

## Dependencies

```txt
bottle
requests
```

## Input

-

## Output

Output of this module is JSON body the same as the JSON body received from HTTP GET request to the API.
