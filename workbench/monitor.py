#!/usr/bin/env python
# SYSTEM DEPENDENCIES
import sys
import argparse
import json
import time
import platform
import os
import re
import time
import uuid
import datetime
from collections import OrderedDict, namedtuple

# OPENPILOT RELATED
import zmq
from cereal import car, log
from common.params import Params
from selfdrive.config import Conversions as CV
from selfdrive.car.car_helpers import get_car
from selfdrive.version import version, dirty
from selfdrive.swaglog import cloudlog
import selfdrive.messaging as messaging
from selfdrive.services import service_list

# WORKBENCH
from server import WebsocketServer
from system_info import *
from tombstones import *

def poll_zmq(ws):
  
#TODO: Someone better at Python than me can help clean this file up if they get time...
def new_client(client, ws):
  print("New client connected and was given id %d" % client['id'])
  initial_tombstones = set(get_tombstones())
  context = zmq.Context()
  poller = zmq.Poller()
  parser = argparse.ArgumentParser(description='Sniff a communcation socket')
  parser.add_argument('--pipe', action='store_true')
  parser.add_argument('--raw', action='store_true')
  parser.add_argument('--json', action='store_true')
  parser.add_argument('--dump-json', action='store_true')
  parser.add_argument('--no-print', action='store_true')
  parser.add_argument('--proxy', action='store_true', help='republish on localhost')
  parser.add_argument('--map', action='store_true')
  parser.add_argument('--addr', default='127.0.0.1')
  parser.add_argument("socket", type=str, nargs='*', help="socket name")
  args = parser.parse_args()
  republish_socks = {}

  service_whitelist = ["live100", "logMessage", "clocks", "androidLogEntry", "thermal", "health", "gpsLocation", "carState", "carControl"]
  for m in args.socket if len(args.socket) > 0 else service_list:
    if m in service_list:
      port = service_list[m].port
    elif m.isdigit():
      port = int(m)
    else:
      print("service not found")
      exit(-1)
    sock = messaging.sub_sock(context, port, poller, addr=args.addr)
    if args.proxy:
      republish_socks[sock] = messaging.pub_sock(context, port)
  
  can_messages = {}
  while 1:
    now_tombstones = set(get_tombstones())
    polld = poller.poll(timeout=1000)
    data = {}
    for sock, mode in polld:
      if mode != zmq.POLLIN:
        continue
      msg = sock.recv()
      # print fingerprint
      evt = log.Event.from_bytes(msg)
      
      if evt.which() == 'can':
        for c in evt.can:
          # read also msgs sent by EON on CAN bus 0x80 and filter out the
          # addr with more than 11 bits
          if c.src%0x80 == 0 and c.address < 0x800:
            can_messages[c.address] = len(c.dat)
        fingerprint = ', '.join("\"%d\": %d" % v for v in sorted(can_messages.items()))
        fingerprint = json.loads('{' + fingerprint + '}')
        data['fingerprint'] = fingerprint
      if evt.which() == 'thermal':
        data['openpilotParams'] = get_params()
        data['system'] = get_system_info()
        data['tombstones'] = []
        for fn, ctime in (now_tombstones):
          # cloudlog.info("reporting new tombstone %s", fn)
          data['tombstones'].append(get_tombstone(fn))
        # report_tombstone(fn, client)
        
        initial_tombstones = now_tombstones
      if evt.which() in service_whitelist:
        data[evt.which()] = evt.to_dict()[evt.which()]
      
      if any(data):
        # state_file = open("/data/workbench/data/state.json", "w")
        # state = merge_state(state,data)
        # state_file.write(json.dumps(state))
        # state_file.close()
        ws.send_message_to_all(json.dumps(data))
        time.sleep(1)
# Called for every client disconnecting
def client_left(client, ws):
	print("Client(%d) disconnected" % client['id'])

# Called when a client sends a message
def message_received(client, ws, message):
	if len(message) > 200:
		message = message[:200]+'..'
	print("Client(%d) said: %s" % (client['id'], message))

def merge_state(x, y):
  z = x.copy()   # start with x's keys and values
  z.update(y)    # modifies z with y's keys and values & returns None
  return z

  
def get_params():
  params = Params()

  is_metric = params.get("IsMetric") == "1"
  passive = params.get("Passive") != "0"
  CP = car.CarParams.from_bytes(params.get("CarParams", block=True))

  data = {
    "passive": passive,
    "is_metric": is_metric,
    "car": CP.to_dict()
  }
  return data

def main():
  PORT=4000
  ws = WebsocketServer(PORT,host='0.0.0.0')
  ws.set_fn_new_client(new_client)
  ws.set_fn_client_left(client_left)
  ws.set_fn_message_received(message_received)
  ws.run_forever()

if __name__ == '__main__':
  main()