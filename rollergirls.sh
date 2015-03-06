#!/bin/bash

export LC_ALL='C'

if [ "$1" = "gone-teams.txt" ]
then
	roster="gone-teams.txt"
else
	roster="master_roster.txt"
	roster_metaphones="master_roster_metaphones.txt"
fi

# Fix the newlines
#dos2unix $roster > /dev/null
perl -pi -e 's/\r\n/\n/' $roster
perl -pi -e 's/\r/\n/g' $roster
echo

# Move the date column to the third column
if [ "$roster" = "master_roster.txt" ]
then
	mv $roster /tmp; cat /tmp/$roster | awk -F '	' '{print $2, "\t", $3, "\t", $1, "\t", $4}' > $roster
elif [ "$roster" = "gone-teams.txt" ]
then
	mv $roster /tmp; cat /tmp/$roster | awk -F '	' '{print $2, "\t", $3, "\t", $1, "\t", $4, "\t", $5, "\t", $6, "\t", $7, "\t", $8}' > $roster
fi
# Capitalize the first letter of each line
perl -pi -e 's/\w.+/\u$&/' $roster

# Remove blank lines
perl -pi -e 's/^\s*$//' $roster

# Fix the duplicate names
perl -pi -e 's/^Travel Team.*$//' $roster

# Fix the headers
#perl -pi -e 's/ Skater Number/Skater Number/' $roster
#perl -pi -e 's/ League Name/League Name/' $roster
perl -pi -e 's/Name\t Team/Name\tTeam/g' $roster
perl -pi -e 's/\t\s*DATE\s*\t/\tDate Added\t/gi' $roster

# Fix the broken Excel formatting
perl -pi -e 's/\t+\n/\n/g' $roster
perl -pi -e 's/^\t+//' $roster
perl -pi -e 's/\"$//' $roster
perl -pi -e 's/\"\"/\"/g' $roster
perl -pi -e 's/^\"//' $roster

# Fix special characters
perl -pi -e "s/\xa0//g" $roster
perl -pi -e "s/\xca//g" $roster
perl -pi -e "s/\x92/\'/g" $roster
perl -pi -e "s/\x95/&iuml;/g" $roster
perl -pi -e "s/\xa2/&cent;/g" $roster
perl -pi -e "s/\xb4/&times;/g" $roster
perl -pi -e "s/\xbc/&deg;/g" $roster
perl -pi -e "s/\xb9/&pi;/g" $roster
perl -pi -e "s/\xd8/&Oslash;/g" $roster
perl -pi -e "s/\xf1/&ntilde;/g" $roster
perl -pi -e "s/\xfc/&uuml;/g" $roster
perl -pi -e "s/\xa1/&iexcl;/g" $roster
perl -pi -e "s/\xd4/\'/g" $roster
perl -pi -e "s/\xd5/\'/g" $roster
perl -pi -e "s/\x9a/&ouml;/g" $roster
perl -pi -e "s/\x8e/&eacute;/g" $roster

# Fix those on multiple teams, or those with long lines
perl -pi -e 's/\tUndetermined/\t /g' $roster
perl -pi -e 's/ \/ /<br> &nbsp\;&nbsp\;+ /g' $roster
perl -pi -e 's/1 part grenadine, 2 parts whoopass/(too long)/g' $roster
perl -pi -e 's/anarchy symbol/anarchy/g' $roster
perl -pi -e 's/form of immodestly dressed women/form of immodestly<br>&nbsp\;&nbsp\;&nbsp\;dressed women/' $roster
perl -pi -e 's/sporty derby darlins extra/sporty derby<br>&nbsp\;&nbsp\;&nbsp\;darlins extra/' $roster
perl -pi -e 's/Roses w\/ affection/Roses<br>&nbsp\;&nbsp\;&nbsp\;w\/ affection/' $roster
perl -pi -e 's/i\(imaginary number\)/<i>i<\/i>/' $roster
perl -pi -e 's/Commander of the Bob/Commander<br>of the Bob/g' $roster
perl -pi -e 's/\(waiting for the/<br> \(waiting for the/g' $roster
perl -pi -e 's/\(okay given by/<br> \(okay given by/g' $roster
perl -pi -e 's/Girl Mechanics w\/assorted vices Red Garage shirts \& black bottoms \(could be black \& white check bottoms\) Team colors: Red \& black w\/white accents/Red and black Girl Mechanics w\/ assorted vices/' $roster
perl -pi -e 's/Green and yellow, black sleeveless shirts, with black skirts or shorts \(one tutu\), all with yellow piping or flare and dobo  karate jackets/Green, yellow, and black karate theme/g' $roster
perl -pi -e 's/A fun-loving, but lethal, band of carnival freaks.*/Fun-loving carnival freaks/g' $roster
perl -pi -e 's/Three Mile Island workers.*/Three Mile Island workers/g' $roster
perl -pi -e 's/Girl Gang with Royal Blue Accents.*/Girl Gang/g' $roster
perl -pi -e 's/Old Mob theme White tops.*/Old Mob theme/g' $roster
perl -pi -e 's/Post-Apocalyptic champions of the Thunderdome.*/Post-Apocalyptic champions of the Thunderdome/g' $roster
perl -pi -e 's/Women in power wearing gray pin-striped skirts.*/Women in power wearing grey pin-stripes/g' $roster
perl -pi -e 's/Rowdy, sultry skaters in the form of immodestly.*/Rowdy, sultry skaters/g' $roster
perl -pi -e "s/Tough and sexy tribute to Guns.*/Tough and sexy tribute to Guns 'N' Roses/g" $roster

# Fix the duplicate names for those who don't have names (ugh!)
mv $roster /tmp; grep -v "^Undetermined" /tmp/$roster > $roster; rm /tmp/$roster
mv $roster /tmp; grep -v "^Various skaters" /tmp/$roster > $roster; rm /tmp/$roster

# Make all blank entries &nbsp;
perl -pi -e 's/\t *\t/\t&nbsp;\t/g' $roster
perl -pi -e 's/\t *\t/\t&nbsp;\t/g' $roster
perl -pi -e 's/\t *\t/\t&nbsp;\t/g' $roster

# Clear out any superfluous spaces before or after entries
perl -pi -e 's/\t +/\t/g' $roster
perl -pi -e 's/ +\t/\t/g' $roster

# Remove extra quotation marks
perl -pi -e 's/\t\"/\t/' $roster
perl -pi -e 's/\"\t/\t/' $roster


if [ "$roster" = "master_roster.txt" ]
then
	# Print out duplicate entries
	echo "Duplicates:"
	cat $roster | awk -F '	' '{print $1}' | sort | uniq -d
	echo

	# Generate the metaphone index
	echo "Generating metaphone index..."
	./roster_metaphones.py $roster > $roster_metaphones
	echo

	echo -n "Number of new names: "
	diff --side-by-side --suppress-common-lines master_roster.txt master_roster.txt.bak | grep -e "<$" | wc -l
	echo

	echo -n "Number of updated names: "
	diff --side-by-side --suppress-common-lines master_roster.txt master_roster.txt.bak | grep " |      " | wc -l
	echo

	echo -n "Number of deleted names: "
	diff --side-by-side --suppress-common-lines master_roster.txt master_roster.txt.bak | grep -e "  >" | wc -l
	echo

	# Backup the files for the next run, to get stats
	cp $roster $roster.bak

	# see how many members are on a league
	cat $roster  | awk -F '\t' '{print $4}' | sort | uniq -c | sort -n | grep -v Team | grep -v TBD | grep -e "^ 1[456789]" -e "^ [23456789]"
fi

# Upload new roster file
scp $roster $roster_metaphones april@stan.nerp.net:www/rollergirls/

# Re-run this same script for the teams file
if [ "$roster" = "master_roster.txt" ]
then
	./$0 gone-teams.txt
fi
