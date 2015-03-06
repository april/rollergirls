#!/usr/bin/python

import cgi
from os import environ, stat
from time import gmtime, localtime, strftime

# User Configuration
roster_file = 'master_roster.txt'
title = 'International Rollergirls\' Master Roster (all flat/banked-track leagues and rollergirl names)'
author = 'April King'
description = 'All US, Canadian, and International Rollergirls'
keywords = 'rollergirl roster roller derby names'
not_available = '&nbsp;'
c = 0                  # Default column number (starts at zero)

# Global variables
c_to_u = {}                                           # Selected Column -> Unique Column mapping
u_to_l = {}                                           # Unique Column (column 1) -> Line mapping
script_name = environ['REQUEST_URI'].split("?")[0]    # CGI SCRIPT_NAME variable, for linking to self

# Get column variable (sort number), and reversal
form = cgi.FieldStorage()
if form.has_key('c'): c = int(form['c'].value)
else: c = 0
if form.has_key('r'): reverse = 1
else: reverse = 0

# Create the stylesheet, based on the CGI print variable
stylesheet = """
 a { color: #725185; }
 a:hover { color: #585185; }
 a:active { color: #585185; }
 body {background-color: #DCE8D3; color: black; text-decoration: none; }
 .tables { font-size: smaller; border-style: solid; border-width: 1px; border-color: #000000; background-color: #A4BE95; }
 .tables td { padding-left: .5em; }
 .totals { border-style: solid; border-width: 0px; border-top-width: 1px; border-color: #000000; background-color: #A4BE95; }
 .header { background-color: #DCE8D3; }
 .headerspan { font-weight: bold; }
 .trc1 { background-color: #F1F2DC; }
 .trc2 { background-color: #DCE8D3; }
""" 

if form.has_key('print'):
	stylesheet = """
 a { color: #000000; }
 a:hover { color: #000000; }
 a:active { color: #000000; }
 body {background-color: #CCCCCC; color: #000000; text-decoration: none; }
 .tables { font-size: smaller; border-style: solid; border-width: 1px; border-color: #000000; background-color: #DDDDDD; }
 .tables td { padding-left: .5em; border-bottom: 1px solid black; }
 .totals { border-style: solid; border-width: 0px; border-top-width: 1px; border-color: #000000; background-color: #DDDDDD; }
 .totals td { border: 0; }
 .header { background-color: #DDDDDD; }
 .header td {border: 0; }
 .headerspan { font-weight: bold; }
 .trc1 { background-color: #FFFFFF; }
 .trc2 { background-color: #EEEEEE; }
"""

# Get the last updated time for the roster file (in MM/DD/YYYY format), add to title
last_updated = strftime("%m/%d/%Y", localtime(stat(roster_file)[8]))
last_updated_http = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime(stat(roster_file)[8]))

def print_tr(attr, bgcolor=''):
	row = ("<tr %s>" % bgcolor)  + ('<td>%s</td>' * c_max) + '</tr>'
	print row % tuple(attr)

# Open file
fh = open(roster_file, "r")

# Fix header to make links
header = list(fh.readline().strip().split('\t'))
c_max = len(header)
for i in range(0,len(header)):
	if ((i != c) or (reverse == 1)):   # Don't make it reversable
		header[i] = "<a href=\"%s?c=%s\">%s</a>" % (script_name,i,header[i])
	else:
		header[i] = "<a href=\"%s?c=%s&amp;r=1\">%s</a>" % (script_name,i,header[i])
	if (i == c):
		header[i] = '<span class="headerspan">' + header[i] + '</span>'

# Suck all the data in
while 1:

	line = fh.readline()
	if not line:
		break

	line = line.strip().split('\t')

	line.extend([not_available] * (c_max - len(line)))   # Make sure we have full lines for each

	u_to_l[line[0]] = line                # Add entry for movie (complete)
	if ((line[c] != not_available) and (line[c] != '')):
		try:
			c_to_u[line[c]].append(line[0])   # Add entry for column to sort by in values
		except:
			c_to_u[line[c]] = [line[0]]

# Now to print all the data out
print 'Content-type: text/html; charset=UTF-8'
print 'Last-Modified: %s\n' % last_updated_http

print """
<?xml version="1.0" encoding="UTF-8"?>\n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title>%s</title>
<meta name="author" content="%s" />
<meta name="description" content="%s" />
<meta name="keywords" content="%s" />
<style type="text/css">
%s
</style>
</head>
<body class="body">
  <div style="float: right;">
    <script type="text/javascript"><!--
    google_ad_client = "pub-3725161092275272";
    /* For Name List */
    google_ad_slot = "5845552846";
    google_ad_width = 120;
    google_ad_height = 600;
    //-->
    </script>
    <script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>
</div>
<table class="tables" cellspacing="0">
  <tr>
    <td colspan="%s">
      <table width="100%%">
        <tr>
          <td style="text-align: center; padding-bottom: .25em;">
            Please read the <b><a href="rules.html">REGISTRATION INSTRUCTIONS</a></b>.&nbsp;&nbsp;--&nbsp;&nbsp; 
            <b><a href="teams.cgi">TEAMS</a></b>&nbsp;&nbsp;--&nbsp;&nbsp; 
            Check a new name for uniqueness: <form action="similarity.cgi" method="get" style="display: inline; margin: 0;"><input type="text" name="name" style="border: 1px solid black; font-size: x-small; height: 1.5em; padding: 0; vertical-align: middle;"></form>&nbsp;&nbsp;--&nbsp;&nbsp; 
            Check an <a href="roster.html">entire roster</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
""" % (title, author, description, keywords, stylesheet, c_max)

print_tr(header,'class="header"')

# Print the ones with an entry for column
counter = 0
c_keys = c_to_u.keys()
c_keys.sort()
if reverse:
	c_keys.reverse()
for i in c_keys:
	c_to_u[i].sort()
	for j in c_to_u[i]:
		try:
			if counter % 2 == 0:
				print_tr(u_to_l[j],'class="trc1"')
			else:
				print_tr(u_to_l[j],'class="trc2"')
			del(u_to_l[j])
			counter = counter + 1
		except KeyError:
			pass

# Now the ones without it
t_keys = u_to_l.keys()
t_keys.sort()
for i in t_keys:
	try:
		if counter % 2 == 0:
			print_tr(u_to_l[i],'class="trc1"')
		else:
			print_tr(u_to_l[i],'class="trc2"')
		counter = counter + 1
	except KeyError:
		pass

print """
<tr><td colspan="%s">
<table class="totals" width="100%%">
<tr><td style="padding-left: 0;">Official roster, maintained by <a href="mailto:masterroster@gmail.com">Elaina B. & Soylent Mean</a> (April King).</td>
<td align="right"><b>TOTAL ROLLERGIRLS: %s</b></td></tr>
<tr><td style="padding-left: 0;">Based off of Elaina B.'s <a href="http://groups.yahoo.com/group/roller_girls/">official master roster</a>.</td>
<td align="right"><b>LAST UPDATED: %s</b></td></tr>
<tr><td colspan="2" style="padding-left: 0;">Please read the <b><a href="rules.html">RULES</a></b> before asking us questions!</td>
</table>
</td></tr></table>
</body>
</html>
""" % (c_max, counter, last_updated)
