#!/usr/bin/python

import re
import os
import sys
import json
import subprocess # may not be needed
from subprocess import Popen, PIPE

container = {}
regexes = []

def usage():
	print("Usage: " + sys.argv[0] + " [file]")
	print("\t -h, --help\t print help")
	exit()

def valid_string(line): # TODO: line = testcase, might want to rename...
	# case sensitivity problems - ie date
	line = line.lower() # potential problems
	
	# shared objects - find /lib/ -name "*.so*"

	# imports
	# for file in $(find /lib/ -name "*.so*"); do nm -aDP $file |& egrep -v ".so|:" | cut -d" " -f1; done;
		# -a list all symbols -- memset@@GLIBC_2.0
		# -D list dynamic symbols - memset, wmemset, ...etc
		# -D will conflict with -a....
	# PROBLEM - current implementation only checks root of lib

	for entry in data:
		if data[entry]["type"] == "list":
			#print "is list"
			if entry not in container:
				container[entry] = []
			if line in data[entry]["data"]: # something wrong here
				container[entry].append(line)
				return False
	
		########################
		# garbage - ALPHA STAGE (unoptimized)
		########################

		# [^_]  ^_] - 5e 5f 5d
		# TODO - also seeing [^]
		if len(line) < 6:
			if "^_]" in line:
				return False
			
		if len(line) == 5:
			if(line[2] == "9"):
			#if line in ["NP9KP","NH9KH","NX9KX","qX9rX","qP9rP","qH9rH","PTRhP"]:
				return False

		if "$" in line:
			return False	

		if line is "UWVS":
			return False

		if "(|6)" in line or "\"|()" in line:
			return False


	########################
	## REGEX - must escape some regex entities in db.json
	########################

	# need to foreach regex	
	for regx in regexes:
		# (\\b|.* )*(net|netsh|calc|cmd|exit){1}(\\b| .*)*
		# "data":"[a-zA-Z]?:\\(.*)"
		# test = re.compile(data[entry]["data"]) # really inefficient - need to create a compiled array at start of program
		if regx["regex"].match(line): # match vs search, line should be fine..
			tmpName = regx["name"]
			if tmpName not in container:
				container[tmpName] = []
			container[tmpName].append(line)
			return False
				

	return True

# main - expected input = file of strings dump
if len(sys.argv) == 2:
	if sys.argv[1] == "-h" or sys.argv[1] == "--help":
		usage()

	'''
	# would like to clear results file..
	oFile = open("results.txt", "w")a
	'''
	process = Popen(["strings", sys.argv[1]], stdout=PIPE)
	exit_code = os.waitpid(process.pid, 0)
	output =process.communicate()[0]

	db = open("db.json")
	data = json.load(db)	

	##################
	## prepare regexes
	##################
	for item in data:
		if data[item]["type"] == "regex":
			tmpObj = {
				"name":item,
				"regex":re.compile(data[item]["data"])
			}

			regexes.append(tmpObj)

	# print allowed data
	# f = open("S2IP.txt") # used to be sys.argv[1], when I was importing string output
	f = output.split("\n")
	for line in f: # rstrip'ing each loop, might be better to do it in one run...
		line = line.rstrip()
		if valid_string(line): ## DEBUG -
			#oFile.write(line + "\n")
			print(line)
			#print(line)

	#print str(container)

	# print dropped data
	for entry in container:
		if len(container[entry]) != 0:
			print("\n")
			print(entry)
			print("==========================")
			for item in container[entry]:
				print item

	db.close() # what about return False..
	#oFile.close()

else:
	usage()


