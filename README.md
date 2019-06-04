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

```buildoutcfg

```

### Delete Network Devices
```buildoutcfg
./networkDevice.py --delete 10.10.50.2 10.10.50.3
https://10.66.104.121:443/dna/intent/api/v1/network-device?managementIpAddress=10.10.50.2
Waiting for Task 535f490c-f658-447f-ac6f-0b6c655d88fe
Task=535f490c-f658-447f-ac6f-0b6c655d88fe has not completed yet. Sleeping 5 seconds...
Task=535f490c-f658-447f-ac6f-0b6c655d88fe has not completed yet. Sleeping 5 seconds...
10.10.50.2:Network device deleted successfully
https://10.66.104.121:443/dna/intent/api/v1/network-device?managementIpAddress=10.10.50.3
Waiting for Task 8fca6b88-17ba-4809-bf06-24c30769e96a
Task=8fca6b88-17ba-4809-bf06-24c30769e96a has not completed yet. Sleeping 5 seconds...
10.10.50.3:Network device deleted successfully

```

### Add Network Devices to inventory
```buildoutcfg
./networkDevice.py --username cisco --password cisco --snmp public --add 10.10.50.2 10.10.50.3 
Waiting for Task 863cece3-e100-48df-b60a-9d01351d6223
https://10.66.104.121:443/dna/intent/api/v1/task/863cece3-e100-48df-b60a-9d01351d6223/tree
url:/task/863cece3-e100-48df-b60a-9d01351d6223/tree
deviceUuid:b8ade651-12a1-4abd-afd3-2e2e383b3627 ipAddress:10.10.50.2 message:Success
deviceUuid:4ed1974e-bf77-4d9a-b36a-17295e378054 ipAddress:10.10.50.3 message:Success
```
