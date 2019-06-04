## A tool to display and interact with network devices
This tool shows all network devices, a specific one as well as forcing a resync with Cisco DNA Center.

Network devices can also be deleted.

## Examples

### List of network devices
just run networkDevice.py with no arguments.

```buildoutcfg

```

### See a specific network device
The --netdev <ip> will show a specific network device.

```buildoutcfg


```

### Force a resync.
Just use the --forcesync <ip> option

Shows a list of the deviceId and the IP address of the device with the tag "switch"
```buildoutcfg
$ ./tag.py --tag switch 
https://sandboxdnac.cisco.com:8080/api/v1/tag/association?tag=switch&resourceType=network-device
https://sandboxdnac.cisco.com:8080/api/v1/network-device/74b69532-5dc3-45a1-a0dd-6d1d10051f27
https://sandboxdnac.cisco.com:8080/api/v1/network-device/6d3eaa5d-bb39-4cc4-8881-4a2b2668d2dc
[('74b69532-5dc3-45a1-a0dd-6d1d10051f27', '10.10.22.70'), ('6d3eaa5d-bb39-4cc4-8881-4a2b2668d2dc', '10.10.22.66')]
```
