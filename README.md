## A tool to display and interact with network devices
This tool shows all network devices, a specific one as well as forcing a resync with Cisco DNA Center.

Network devices can also be deleted.

## Installing and Running

I would recommend using a virtual environment.  All that is required is the requests module
```buildoutcfg
pip install requests
```
The script uses the dnac_config.py file to specify the DNA Center, username and password.
These can also be set using environment variables too.  Run the following commands in the shell (changing the appropriate values)

```buildoutcfg
export DNAC="1.1.1.1"
export DNAC_USER="admin"
export DNAC_PASSWORD="password"
export DNAC_PORT=443

```
## Examples

### List of network devices
just run networkDevice.py with no arguments.

```buildoutcfg
$ ./networkDevice.py 
https://10.10.10.10:443/dna/intent/api/v1/network-device
hostname                                  mgmt IP          serial      platformId        SW Version  role            Uptime         
perth-9k.adamlab.cisco.com                10.10.50.2       FOC2224Z0F1 C9300-24P         16.6.5      ACCESS          20:27:32.64    
None                                      10.10.50.3       None        None              None        UNKNOWN         N/A            

```

### See a specific network device
The --netdev <ip> will show a specific network device.

```buildoutcfg


```

### Force a resync.
Just use the --forcesync <ip> option

```buildoutcfg
$ ./networkDevice.py  --forcesync 10.10.50.2  
https://10.10.10.1:443/dna/intent/api/v1/network-device?managementIpAddress=10.10.50.2
Waiting for Task 89f9171a-7a85-4da6-a8cf-796b5c68e20d
{'progress': 'Synced devices:\n', 'startTime': 1559614908907, 'version': 1559614908970, 'endTime': 1559614908972, 
'lastUpdate': 1559614908970, 'serviceType': 'Inventory service', 'isError': False, 
'rootId': '89f9171a-7a85-4da6-a8cf-796b5c68e20d', 'instanceTenantId': '5ccbc72a3aea9800cf8e5e76', 
'id': '89f9171a-7a85-4da6-a8cf-796b5c68e20d'}
```

### Delete Network Devices
```buildoutcfg
./networkDevice.py --delete 10.10.50.2 10.10.50.3
https://10.10.10.10:443/dna/intent/api/v1/network-device?managementIpAddress=10.10.50.2
Waiting for Task 535f490c-f658-447f-ac6f-0b6c655d88fe
Task=535f490c-f658-447f-ac6f-0b6c655d88fe has not completed yet. Sleeping 5 seconds...
Task=535f490c-f658-447f-ac6f-0b6c655d88fe has not completed yet. Sleeping 5 seconds...
10.10.50.2:Network device deleted successfully
https://10.10.10.10:443/dna/intent/api/v1/network-device?managementIpAddress=10.10.50.3
Waiting for Task 8fca6b88-17ba-4809-bf06-24c30769e96a
Task=8fca6b88-17ba-4809-bf06-24c30769e96a has not completed yet. Sleeping 5 seconds...
10.10.50.3:Network device deleted successfully

```

### Add Network Devices to inventory
```buildoutcfg
./networkDevice.py --username cisco --password cisco --snmp public --add 10.10.50.2 10.10.50.3 
Waiting for Task 863cece3-e100-48df-b60a-9d01351d6223
https://10.10.10.10:443/dna/intent/api/v1/task/863cece3-e100-48df-b60a-9d01351d6223/tree
url:/task/863cece3-e100-48df-b60a-9d01351d6223/tree
deviceUuid:b8ade651-12a1-4abd-afd3-2e2e383b3627 ipAddress:10.10.50.2 message:Success
deviceUuid:4ed1974e-bf77-4d9a-b36a-17295e378054 ipAddress:10.10.50.3 message:Success
```
### Advanced
can also use these with xargs.  Will provide the first 50 devices as argument to delete
```
head -50 /tmp/failed | xargs ./networkDevice.py --delete
```

### Change management IP address.
The change_mgmt_ip.py changes the management IP address of a list of devices. You need a csv file with two columns, oldip and newip.

A sample is provided in workfiles/change.csv.  This is a trivial example that changes a management IP address, then changes it back.
```buildoutcfg
$ cat workfiles/change.csv 
oldip,newip
10.10.15.200,10.10.15.201
10.10.15.201,10.10.15.200

```

the script is run as follows:
```buildoutcfg
$ ./change_mgmt_ip.py --ipmgmtfile workfiles/change.csv 
Changing Management IP 10.10.15.200 to 10.10.15.201.
Waiting for Task ea75e45f-779c-4ed8-8898-6ebaa1f09ea1
Inventory service updating devices
Updated device 10.10.15.201, result = true
Changing Management IP 10.10.15.201 to 10.10.15.200.
Waiting for Task dc90f1a7-1644-44c3-92a9-280fd3c9a9d8
Inventory service updating devices
Updated device 10.10.15.200, result = true

```

### Change Device Role.
takes a CSV file of ip address and new role.   Updates device to new role.

This sample does the same device twice, but that is just for testing.
```buildoutcfg
$ cat workfiles/role.csv 
ip,role
10.10.15.100,ACCESS
10.10.15.100,DISTRIBUTION

```
Need to run the script with the input csv file.
```buildoutcfg
 ./change_role.py --rolefile workfiles/role.csv 
Changing role of device IP 10.10.15.100 to ACCESS: Task:a53f2936-9d03-49bc-a910-04d345d9da77 not complete, waiting 10 seconds, polling 2
Device role was succesfully updated to ACCESS for 10.10.15.100
Changing role of device IP 10.10.15.100 to DISTRIBUTION: Task:0a972775-4cf8-4418-817f-6027bbb5621c not complete, waiting 10 seconds, polling 2
Device role was succesfully updated to DISTRIBUTION for 10.10.15.100

```