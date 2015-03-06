#!/usr/bin/python

roster = file("master_roster.txt", "r")
for line in roster:
	print repr(line)
