from __future__ import print_function
import time

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

import requests
import json

## User of InfluxDB
USER = 'sopoal'

## Password of the User for InfluxDB
PASSWORD = 'password'

## DBNAME should be exist!
DBNAME = 'monero_stats'

## Host and port for InfluxDB
HOST = 'IP_OF_INFLUXDB'
PORT = '8086'

start_height = input()
print("End height")
end_height = input()

url = "http://localhost:18081/json_rpc"
headers = {"content-type" : "application/json"}

rpc_fields = {
	"method" : "get_block_headers_range",
	"params" : {
		"start_height" : start_height,
		"end_height" : end_height	
	}
}
rpc_fields.update({"jsonrpc": "2.0", "id": "0"})

print("PING " + url)

response = requests.post(url,data=json.dumps(rpc_fields),headers=headers)
response = response.json()

series = []
response = response['result']
print("Got a response!")
for i in range(0, end_height - start_height + 1):
	hostName = "put_your_hostname here"
	pointValues = {
		"time"  : int(response['headers'][i]['timestamp']),
		"measurement" : "default_block",
		"fields" : {
			"num_txes" : int(response['headers'][i]['num_txes']),
			"block_size": int(response['headers'][i]['block_size']),
			"difficulty" : int(response['headers'][i]['difficulty']), 
		},
		"tags" : {
			"hostName" : hostName,
		}
	}

	series.append(pointValues)
  
print("Series appended")
client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)

print("Writing....")
# Writing data into InfluxDB. "s" is the timestamp format since InfluxDB can support nanoseconds too.

client.write_points(series,'s')

print("The end..")
