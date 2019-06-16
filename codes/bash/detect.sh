#!/bin/bash

influx -username influx -password influx_pass -host 192.168.188.128 -database telegraf -format csv -execute "select time, usage_system, usage_user, packets_recv, packets_sent from cpu, net where time >= now() - 5m" > ~/flask/test.csv
