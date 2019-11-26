#!/usr/bin/env python
from __future__ import print_function
import sys
import json
import logging
from argparse import ArgumentParser, REMAINDER
from util import get_url, post_and_wait, put_and_wait, delete, wait_on_tasks
import time
import csv


def update_device(oldip, newip):

    payload = {
	"type": "NETWORK_DEVICE",
	"computeDevice": False,
	"snmpVersion": "NODATACHANGE",
	"snmpROCommunity": "NO!$DATA!$",
	"snmpRWCommunity": "NO!$DATA!$",
	"snmpRetry": "-1",
	"snmpTimeout": "-1",
	"cliTransport": "NO!$DATA!$",
	"userName": "NO!$DATA!$",
	"password": "NO!$DATA!$",
	"enablePassword": "NO!$DATA!$",
	"netconfPort": "-1",
	"ipAddress": [oldip],
	"updateMgmtIPaddressList": [{
		"newMgmtIpAddress": newip,
		"existMgmtIpAddress": oldip
	}]
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


def change_ip(file):
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            params = dict(row)
            print(json.dumps(params))
            update_device(params['oldip'], params['newip'])

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')
    parser.add_argument('--ipmgmtfile', type=str, required=False,
                        help="mgmt file.  csv of old, new ip address")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()

    if args.v:

        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.debug("DEBUG ENABLED")

    if args.ipmgmtfile:
        change_ip(args.ipmgmtfile)

