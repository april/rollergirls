#!/usr/bin/python

import cgi, difflib, metaphone, sys
from string import capitalize, lower

# Cutoff levels
CUTOFF_LEVELS = [.85, .80, .75, .70, .65]
CUTOFF_NAMES = ["very high", "high", "medium", "low", "very low"]

# Maximum amount of similar names to return
MAX_RESULTS = 10

# Content type header
print 'Content-type: text/html; charset=UTF-8\n'

# Print Normal HTML blah blah
print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!-- TemplateBeginEditable name="doctitle" -->
<title>April King :: Roller Derby Name Similarity Checker</title>
<!-- TemplateEndEditable -->
<link href="../css/default.css" rel="stylesheet" type="text/css" />
</head>
<body>
<div class="main">
  <div class="boxes_left">
    <div class="box1"></div>
    <div class="box2"></div>
    <div class="box3"></div>
  </div>
  <div class="boxes_right">
    <div class="box4"></div>
    <div class="box5"></div>
    <div class="box6"></div>
  </div>
  <div class="title"><!-- InstanceBeginEditable name="title" -->roller derby name checker<!-- InstanceEndEditable -->
  </div>
	
  <div class="content">
"""

# Retrieve the name that is being tested
form = cgi.FieldStorage()
if form.has_key('name'):
	name = form['name'].value
	name = cgi.escape(name)
else:
	print "Sorry, you must enter a name.<br />"
	#sys.exit(1)

# Create a blank list of names (which will hold the entire roster), and a blank list of results
try:
	rg_names = []

	# Open the master roster file, and load all of the names
	master_roster_fh = open("master_roster.txt", "r")
	for line in master_roster_fh:
		rg_name = line.split("\t")[0].split(" (")[0]
		rg_names.append(rg_name)

	# Create a blank list of all metaphone names
	metaphones = []

	# Open the metaphones database, and read in all of the names
	metaphones_fh = open("master_roster_metaphones.txt")
	for line in metaphones_fh:
		metaphones.append(line.strip().split("\t"))

	# Split the names apart, if they are on multiple lines (like a roster)
	names = name.split("\n")

	for name in names:

		# Cleanup the inputted names, strip them, skip if they're blank (like a roster)
		name = name.strip()
		submitted_name = name
		if name.isspace() or name == "": continue
		
		# Reset the results list
		results = []

		# Capitalize the inputted name ("Soylent mean is a Scary girl" -> "Soylent Mean Is A Scary Girl")
		name = " ".join( map(capitalize, name.split(" ")) )

		# Find all names that entirely contain the inputted name
		containing_names = []
		for i in rg_names:
			if name.lower() in i.lower():
				containing_names.append(i)

		# Find all names that are pronounced the same as the inputted name
		pronunciation = metaphone.transform(name)
		metaphone_names = []
		for i in metaphones:
			if pronunciation == i[1]: metaphone_names.append(i[0])
		
		# Get all matches that "look" similar
		similar_names = difflib.get_close_matches(name, rg_names, MAX_RESULTS, CUTOFF_LEVELS[-1])

		# Calculate the "ratio" of similarity
		for i in range(0, len(similar_names)):
			sm = difflib.SequenceMatcher(None, name, similar_names[i]).ratio()

			# Names in the containing names field automatically get a +.1 score, if they're similar
			# Otherwise, they get a flat medium score
			if similar_names[i] in containing_names:
				sm = sm + .1
				containing_names.remove( similar_names[i] )
			if similar_names[i] in metaphone_names:
				sm = sm + .1
				metaphone_names.remove( similar_names[i] )

			# Add these similar names to the results list, in tuples - (ratio, name)
			results.append( (sm, similar_names[i]) )

		# Remaining "contained" / "metaphone" names get a modified score
		for i in containing_names:
			if i in metaphone_names:
				results.append((CUTOFF_LEVELS[1], i) )
				metaphone_names.remove(i)
			else:
				results.append((CUTOFF_LEVELS[2], i) )

		for i in metaphone_names:
			results.append( (CUTOFF_LEVELS[2], i) )
		
		# Sort the results by score, highest score first
		results.sort()
		results.reverse()

		# Truncate very long results
		if len(results) > MAX_RESULTS:
			results = results[:MAX_RESULTS]

		# Create a printable output
		# Put all the results in an array, along with their level - like Page Burnah (high)
		output = []
		for i in results:
			for j in range(0, len(CUTOFF_LEVELS)):
				if (i[0] +.001) > CUTOFF_LEVELS[j]:   # Account for FP errors by adding +.001
					output.append("%s (%s)" % (i[1], CUTOFF_NAMES[j]))
					break

		# Find all names that contain the inputted name
		if results != []:
			print "The following names are similar to \"%s\":<br /><ul><li>%s</li></ul>" % (submitted_name, "</li><li>".join(output))
		else:
			print "Congratulations, there are no names similar to \"%s\".<br />" % submitted_name

	# Print out similarity results disclaimer
	if similar_names != []: print """
	<br />
	Names with a "very high" level of similarity are almost guaranteed to be rejected.<br />
	Names with a "high" level of similarity are very likely to be rejected.<br />
	Names with a "medium" level of similarity are somewhat likely to be rejected.<br />
	Names with a "low" level of similarity may occasionally be rejected.<br />
	Names with a "very low" level of similarity are unlikely to be rejected.<br />
	<br />
	<i>Names with multiple similarities are more likely to be rejected!</i>
	"""

	# Print out a regular disclaimer
	print """
	<br /><br />
	Please note that passing this test does *not* guarantee that your name will be accepted.<br />
	Similarly, failing this test is not a guarantee that it will be rejected, but it does raise the chance that it will be.
	"""
except:
	raise

# Print out end of HTML blah blah
print """
  </div>
  <div class="designbydiv"><span class="designbyspan">Design by <a class="email" href="mailto:april@twoevils.org">April King</a> (Soylent Mean)</span></div>
</div>
<br clear="all" /><br /><br />
<div>
<center>
<script type="text/javascript"><!--
google_ad_client = "pub-3725161092275272";
/* 728x90, for similarity page */
google_ad_slot = "2593138366";
google_ad_width = 728;
google_ad_height = 90;
//-->
</script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
</center>
</div>
</body>
</html>
"""
