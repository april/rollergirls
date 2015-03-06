#!/usr/bin/python

import string, sys

# Configuration options
header = ["Skater Name", "Skater Number", "Position", "League Name"]
roster_fh = open("master_roster.txt")
positions = ["Coach", "Manager", "Mascot", "Captain", "Co-Captain", "Blocker", "Jammer", "Pivot"]
positions_abbr = {"Coach" : "Coach", "Manager" : "Manager", "Mascot" : "Mascot", "Captain" : "Cap", "Co-Captain" : "Co-Cap", "Blocker" : "Bl", "Jammer" : "Ja", "Pivot" : "Pi"}
separator = "/"

# Suck in roster file, save to players dict, ignoring first line
roster_fh.readline()  # Ignore header line
players = {}
for player in roster_fh:
	
	# Ignore blank lines
	if player.strip() == "": continue

	# Tab break each line
	player = player.strip().split("\t")

	# Print a warning if a name is duplicated...
	if player[0] in players: sys.stderr.write("Warning: Player %s is duplicated!\n" % player[0])

	# Assign to dict (name -> player info), adding position field after the skater number
	if len(player) > 1: players[player[0]] = [player[1]] + [''] + player[2:]
	else:
		sys.stderr.write("Player %s has no league!\n" % player[0])
		players[player[0]] = []

# Suck in all of the positions file, assigning them all to a position dict (position -> [names])
player_positions = {}
for i in positions:
	position_fh = open("positions/%s" % i, "r")
	position_fh = position_fh.readlines()
	position_fh = map(string.strip, position_fh)
	position_fh = map(string.lower, position_fh)
	player_positions[i] = position_fh

# Now loop through all of the players, adding their position their entry
players_keys = players.keys()
players_keys.sort()

for i in players:
	for j in positions:
		if i.lower() in player_positions[j]:
			if players[i][1] == '': players[i][1] = positions_abbr[j]             # If they don't have an assigned position
			else: players[i][1] = players[i][1] + separator + positions_abbr[j]   # If they already have a position

# Print out the roster
print "\t".join(header)
for i in players_keys:
	print i + "\t" + "\t".join(players[i])
