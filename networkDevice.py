#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser, REMAINDER
from util import get_url, post_and_wait, put_and_wait, delete, wait_on_tasks
import time

LIMIT=500
def device2id(device):
    response = get_url('dna/intent/api/v1/network-device?managementIpAddress={0}'.format(device))
    logging.debug(response)
    return response['response'][0]['id']

def id2device(deviceId):
    response = get_url('network-device/{0}'.format(deviceId))
    return response['response']['managementIpAddress']

def show_devices():
    # fix pagination

    devices = []
    response = get_url('dna/intent/api/v1/network-device/count')
    count = response['response']
    logging.debug("count={}".count)
    for start in range(1, count + 1, LIMIT):
        response = get_url('dna/intent/api/v1/network-device?offset={}&limit={}'.format(start, LIMIT))
        devices.extend(response['response'])

    # print header
    print("{0:50}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
          format("hostname", "mgmt IP", "serial",
                 "platformId", "SW Version", "role", "Uptime"))

    for device in devices:
        uptime = "N/A" if device['upTime'] is None else device['upTime']

        # this is for the case of switch stacks.. multiple serial and model numbers
        if device['serialNumber'] is not None and "," in device['serialNumber']:
            serialPlatformList = zip(device['serialNumber'].split(","), device['platformId'].split(","))
        else:
            serialPlatformList = [(device['serialNumber'], device['platformId'])]

        for (serialNumber, platformId) in serialPlatformList:
            print("{0:50.49}{1:17}{2:12}{3:18}{4:12}{5:16}{6:15}".
                  format(str(device['hostname']),
                         str(device['managementIpAddress']),
                         str(serialNumber),
                         str(platformId),
                         str(device['softwareVersion']),
                         str(device['role']), uptime))



def update_devices(deviceList, snmpauth, snmppriv,snmpuser,username,password, enable):
    #print (snmp,username, password)
    deviceList = [d.rstrip() for d in deviceList]
    payload = {
        "ipAddress": deviceList,
        "type": "NETWORK_DEVICE",
        "computeDevice": "false",
        "snmpVersion": "v3",
        "snmpMode": "AUTHPRIV",
        "snmpAuthProtocol": "SHA",
        "snmpAuthPassphrase":snmpauth,
        "snmpPrivProtocol": "AES128",
        "snmpPrivPassphrase": snmppriv,
        "snmpUserName": snmpuser,
        "snmpRetry": "3",
        "snmpTimeout": "5",
        "cliTransport": "ssh",
        "userName": username,
        "password": password,
        "enablePassword": enable
    }
    #print(json.dumps(payload,indent=2))
    #return

    response = put_and_wait("dna/intent/api/v1/network-device", data=payload)
    task = response['id']
    time.sleep(5)
    tree = get_url("dna/intent/api/v1/task/{}/tree".format(task))
    logging.debug(json.dumps(tree,indent=2))

    for t in tree['response']:
        if 'failureReason' in t:
            print(t['failureReason'])
        else:
            #progress = json.loads(t['progress'])

            #print (" ".join(['{}:{}'.format(k, progress[k]) for k in progress.keys()]))
            print(t['progress'])

def forcesync(devicelist):
    deviceList = [ d.rstrip() for d in devicelist]
    logging.debug("SYNC:{}".format(str(deviceList)))
    payload = list(map(device2id, deviceList))
    logging.debug(payload)
    response = put_and_wait('dna/intent/api/v1/network-device/sync', payload)
    print(response)

def delete_devices(deviceList):
    taskdict = {}
    for device in deviceList:
        device=device.rstrip()
        try:
            dev_id = device2id(device)
        except IndexError:
            print("{}: ERROR NOT FOUND".format(device))
            continue
        taskid = delete('dna/intent/api/v1/network-device/{}'.format(dev_id))
        print('deleting {}:{}'.format(device, taskid))
        taskdict[taskid] = device
    #print(json.dumps(taskdict))
    print("polling deletion tasks")
    responses = wait_on_tasks(taskdict.keys())

    print("\nTask results:")
    for response in responses:
        message = ''
        if 'progress' in response:
            message = response['progress']
        print('{}:{}:{}'.format(taskdict[response['id']], response['id'],message))

def add_devices(deviceList, snmp,username,password):
    #print (snmp,username, password)
    deviceList = [d.rstrip() for d in deviceList]
    payload = {
        "ipAddress": deviceList,
        "type": "NETWORK_DEVICE",
        "computeDevice": "false",
        "snmpVersion": "v2",
        "snmpROCommunity": snmp,
        "snmpRWCommunity": "",
        "snmpRetry": "3",
        "snmpTimeout": "5",
        "cliTransport": "ssh",
        "userName": username,
        "password": password,
        "enablePassword": ""
    }
    response = post_and_wait("dna/intent/api/v1/network-device", data=payload)
    task = response['id']
    time.sleep(5)
    tree = get_url("dna/intent/api/v1/task/{}/tree".format(task))
    #print(json.dumps(tree,indent=2))

    for t in tree['response']:
        if 'failureReason' in t:
            print(t['failureReason'])
        else:
            progress = json.loads(t['progress'])
            print (" ".join(['{}:{}'.format(k, progress[k]) for k in progress.keys()]))


if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--netdev', type=str, required=False,
                        help="network devices")

    parser.add_argument('--forcesync', action='store_true', required=False,
                        help="force sync of devices")
    parser.add_argument('--delete', action='store_true', required=False,
                        help="delete  devices from inventory")
    parser.add_argument('--add', action='store_true', required=False,
                        help="add  devices to inventory")
    parser.add_argument('--update', action='store_true', required=False,
                        help="update  devices in inventory")
    parser.add_argument('--username', type=str, default='cisco', required=False,
                        help="username")
    parser.add_argument('--password', type=str, default='cisco', required=False,
                        help="password")
    parser.add_argument('--enable', type=str, default='cisco', required=False,
                        help="password")
    parser.add_argument('--snmp', type=str, default='public',required=False,
                       help="snmp")
    parser.add_argument('--snmpauth', type=str, default='public', required=False,
                        help="snmp")
    parser.add_argument('--snmppriv', type=str, default='public', required=False,
                        help="snmp")
    parser.add_argument('--snmpuser', type=str, default='public', required=False,
                        help="snmp")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    parser.add_argument('rest', nargs=REMAINDER)
    args = parser.parse_args()
    if args.v:

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("DEBUG ENABLED")

    if args.netdev:
        response = get_url("dna/intent/api/v1/network-device?managementIpAddress={}".format(args.netdev))
        print(json.dumps(response['response'],indent=2))

    elif args.forcesync:
        forcesync(args.rest)
    elif args.delete:
        delete_devices(args.rest)
    elif args.add:
        add_devices(args.rest, username=args.username,password=args.password,snmp=args.snmp)
    elif args.update:
        update_devices(args.rest, username=args.username,password=args.password,
                       snmpauth=args.snmpauth,snmppriv=args.snmppriv, snmpuser=args.snmpuser,enable=args.enable)
    else:
        show_devices()
