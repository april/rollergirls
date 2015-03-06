#!/usr/bin/python

import metaphone, sys

# Create a blank list of names (which will hold the entire roster)
rg_names = []

# Open the master roster file, and load all of the names
master_roster_fh = open(sys.argv[1], "r")
for line in master_roster_fh:
	rg_name = line.split("\t")[0].split(" (")[0]
	rg_names.append(rg_name)

for name in rg_names:
	if metaphone.transform(name) != '': print "%s\t%s" % ( name, metaphone.transform(name) )
