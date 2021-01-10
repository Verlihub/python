# coding: latin-1

# Blacklist 1.2.4.4
# © 2010-2021 RoLex
# Thanks to Frog

# Changelog:
# -------
# 0.0.1.0 - Initial release
# -------
# 1.0.0.0 - Added "find_maxres" configuration to limit number of results on find action
# 1.0.0.0 - Added country codes of addresses in waiting feed list
# -------
# 1.1.0.0 - Added "time_down" configuration to specify timeout of download operation in seconds
# -------
# 1.1.1.0 - Added "listoff" command to disable or enable lists
# -------
# 1.1.2.0 - Added another read failure check
# -------
# 1.1.3.0 - Fixed display of item configuration old value when changing from zero
# 1.1.3.0 - Fixed default exception file creation in wrong directory
# 1.1.3.0 - Added translation ability with list command "lang" and update command "tran"
# -------
# 1.1.4.0 - Added compression file format "zip"
# 1.1.4.0 - Added data file format "emule"
# -------
# 1.1.5.0 - Added "listget" command to force list load
# -------
# 1.1.6.0 - Added exception notifications to waiting feed list aswell
# -------
# 1.1.7.0 - Fixed OnTimer callback
# -------
# 1.1.8.0 - Fixed missing global variable declarations
# 1.1.8.0 - Added referer and user agent headers for URL requests
# 1.1.8.0 - Added different method of validating numbers
# 1.1.8.0 - Added different method of getting hub bot nicks
# 1.1.8.0 - Added public proxy lookup based on number of Google search results
# 1.1.8.0 - Added "listre" command to reload all blacklist lists
# 1.1.8.0 - Added "del" command to delete single blacklisted item in real time
# 1.1.8.0 - Added "code_block" configuration for space separated list of blocked country codes
# 1.1.8.0 - Added "code_except" configuration for space separated list of excepted country codes
# 1.1.8.0 - Added short configuration explanations
# 1.1.8.0 - Added custom blacklist to manage with "my*" commands
# 1.1.8.0 - Added exception list to database instead of text file
# -------
# 1.2.0.0 - Added bypass of public proxy lookup for local and private IP addresses
# 1.2.0.0 - Added four digit version numbering
# 1.2.0.1 - Added "listact" command to set list block action
# 1.2.0.1 - Added "action_proxy" configuration to set public proxy detection block action
# 1.2.0.1 - Added "action_mylist" configuration to set my list item detection block action
# 1.2.0.2 - Fixed wrong UTC time use instead of local time
# 1.2.0.3 - Fixed login notification for slow connections
# 1.2.0.4 - Added "nick_bot" configuration to register bot for sending notifications
# 1.2.0.5 - Added "extry" command to search for IP address in exception list
# -------
# 1.2.1.0 - Fixed incorrect action status when adding new list
# 1.2.1.0 - Fixed missing translation parameter in loading disabled list message
# 1.2.1.0 - Added "listex" command to disable or enable list exception usage
# 1.2.1.0 - Added "except_proxy" configuration to set public proxy detection exception usage
# 1.2.1.0 - Added "except_mylist" configuration to set my list item detection exception usage
# 1.2.1.1 - Added "action_extry" configuration to run exception lookup on notification actions
# 1.2.1.1 - Added "feeddel" command to delete items from waiting feed list
# -------
# 1.2.2.0 - Added IP Intelligence proxy lookup instead of Google based public proxy lookup
# 1.2.2.1 - Added chat mode to public proxy lookup
# 1.2.2.2 - Added operator chat message script command to Ledokol
# 1.2.2.3 - Added more debug messages to public proxy lookup
# 1.2.2.4 - Fixed public proxy exception on login and chat when user is still in cache list
# 1.2.2.5 - Added country code to all lower and higher IP addresses
# 1.2.2.5 - Added support for delayed main chat messages
# 1.2.2.6 - Fixed bypass of public proxy lookup for local and private IP addresses in chat mode
# 1.2.2.7 - Added country code translation to some messages
# 1.2.2.8 - Added "prox_quote" configuration to limit amount of public proxy lookups per day
# 1.2.2.9 - Added prioritization of public proxy and my lists
# 1.2.2.9 - Removed break on first match
# 1.2.2.9 - Added "prox_getasn" configuration to show GeoIP ASN information on proxy detection
# 1.2.2.9 - Added "extry_getasn" configuration to show GeoIP ASN information on exception lookup
# -------
# 1.2.3.0 - Added "myoff" and "exoff" commands to disable or enable items in my and exception lists
# 1.2.3.0 - Added results from my list to find action
# 1.2.3.0 - Added ASN check on connection
# 1.2.3.1 - Added "asn_block" configuration for space separated list of blocked AS numbers
# 1.2.3.1 - Added "asn_except" configuration for space separated list of excepted AS numbers
# 1.2.3.2 - Added "nick_skip" configuration for space separated list of users to skip proxy lookup
# 1.2.3.3 - Added translation file support instead of "lang" and "tran" commands
# 1.2.3.3 - Added "lang_pref" configuration as translation file language prefix
# 1.2.3.4 - Added "ver" command to automatically update script and loaded translation file
# 1.2.3.5 - Added "asn_nofeed" configuration for space separated AS numbers to skip notifying
# -------
# 1.2.4.0 - Added block chat mode with delayed chat messages to public proxy detection
# 1.2.4.1 - Added Mozilla compatible user agent for HTTP requests
# 1.2.4.1 - Fixed public proxy lookup message queue but it is recommended to use Ledokol instead for best compatibility
# 1.2.4.2 - Added redirection of blocked connections, requires Verlihub 1.2.0.1
# 1.2.4.3 - Removed predefined MySQL character set, collation and engine to use system defaults
# 1.2.4.4 - Fixed ASN list notifications resulting in unknown data
# -------

import vh, re, urllib2, gzip, zipfile, StringIO, time, os, subprocess, socket, struct, json

bl_defs = {
	"version": "1.2.4.4", # todo: dont forget to update
	"verfile": "687474703a2f2f6c65646f2e6665617264632e6e65742f707974686f6e2f626c61636b6c6973742f626c61636b6c6973742e766572",
	"pyfile": "687474703a2f2f6c65646f2e6665617264632e6e65742f707974686f6e2f626c61636b6c6973742f626c61636b6c6973742e7079",
	"langfile": "687474703a2f2f6c65646f2e6665617264632e6e65742f707974686f6e2f626c61636b6c6973742f626c61636b5f25732e6c616e67",
	"curlver": ["curl", "-V"],
	"curlreq": "6375726c202d47202d4c202d2d6d61782d726564697273202573202d2d7265747279202573202d2d636f6e6e6563742d74696d656f7574202573202d6d202573202d412022257322202d652022257322202d73202d6f202225732220222573222026",
	"ipintel": "687474703a2f2f636865636b2e6765746970696e74656c2e6e65742f636865636b2e7068703f666f726d61743d6a736f6e26636f6e746163743d25732669703d2573",
	"referer": "68747470733a2f2f6769746875622e636f6d2f7665726c696875622f707974686f6e2f",
	"useragent": ["4d6f7a696c6c612f352e302028636f6d70617469626c653b20426c61636b6c6973742f25733b202b68747470733a2f2f6769746875622e636f6d2f7665726c696875622f707974686f6e2f747265652f6d61737465722f626c61636b6c6973742f29", None],
	"botdesc": "3c426c61636b6c69737420563a25732c4d3a412c483a302f302f312c533a303e",
	"protmove": "24466f7263654d6f7665202573",
	"datadir": os.path.join (vh.basedir, "blackdata"),
	"timersec": 60,
	"quotesec": 60 * 60 * 24,
	"delwait": 60,
	"prevfeed": 30
}

bl_conf = {
	"nick_bot": ["", "str", 0, 250, "Bot nick to register and send notifications"],
	"nick_feed": ["", "str", 0, 250, "User nick to receive all feed messages"],
	"code_block": ["", "str", 0, 1000, "Space separated country codes to block"],
	"code_except": ["", "str", 0, 1000, "Space separated country codes to except"],
	"asn_block": ["", "str", 0, 1000, "Space separated AS numbers to block"],
	"asn_except": ["", "str", 0, 1000, "Space separated AS numbers to except"],
	"asn_nofeed": ["", "str", 0, 500, "Space separated AS numbers to skip notifying"],
	"class_feed": [5, "int", 0, 11, "Minimal class to receive feed messages"],
	"class_conf": [10, "int", 3, 11, "Minimal class to access script commands"],
	"class_skip": [3, "int", 0, 11, "Minimal class to skip public proxy lookup"],
	"nick_skip": ["", "str", 0, 10000, "Space separated nicks to skip proxy lookup"],
	"time_feed": [60, "int", 0, 1440, "Minutes to delay same IP notifications"],
	"time_down": [5, "int", 1, 300, "Download operation timeout in seconds"],
	"notify_update": [1, "int", 0, 1, "Enable blacklist list update notification"],
	"find_maxres": [1000, "int", 1, 10000, "Maximum number of blacklist search results"],
	"prox_lookup": [0, "int", 0, 2, "Enable proxy lookup on user login or chat"],
	"prox_email": ["", "str", 0, 250, "Email address required for proxy lookup"],
	"prox_match": [99, "int", 1, 100, "Minimal number of public proxy matches"],
	"prox_start": [5, "int", 0, 30, "Minutes to wait after hub is started"],
	"prox_timer": [3, "int", 1, 300, "Seconds to process proxy lookup queue"],
	"prox_queue": [100, "int", 1, 10000, "Maximum number of proxy lookups to enqueue"],
	"prox_maxreq": [1, "int", 1, 100, "Maximum number of proxy lookups to send"],
	"prox_quote": [500, "int", 0, 500000, "Maximum number of proxy lookups per day"],
	"prox_nofail": [0, "int", 0, 1, "Disable proxy lookup failure notifications"],
	"prox_getasn": [0, "int", 0, 1, "Enable GeoIP ASN information on proxy detection"],
	"prox_debug": [0, "int", 0, 3, "Level of proxy lookup debug information"],
	"action_proxy": [1, "int", 0, 2, "Block action on public proxy detections"], # 0 - notify only, 1 - drop user, 2 - block chat
	"action_mylist": [1, "int", 0, 1, "Block action on my list item detections"],
	"action_asnlist": [1, "int", 0, 1, "Block action on ASN list item detections"],
	"except_proxy": [1, "int", 0, 1, "Exception usage on public proxy detections"],
	"except_mylist": [1, "int", 0, 1, "Exception usage on my list item detections"],
	"except_asnlist": [1, "int", 0, 1, "Exception usage on ASN list item detections"],
	"action_extry": [0, "int", 0, 1, "Run exception lookup on notification actions"],
	"extry_getasn": [0, "int", 0, 1, "Enable GeoIP ASN information on exception lookup"],
	"lang_pref": ["", "str", 0, 2, "Translation file language prefix to use"],
	"redir_code": ["", "str", 0, 100, "Redirect address on country code block"],
	"redir_asn": ["", "str", 0, 100, "Redirect address on AS number block"],
	"redir_prox": ["", "str", 0, 100, "Redirect address on public proxy block"],
	"redir_my": ["", "str", 0, 100, "Redirect address on my list block"],
	"redir_list": ["", "str", 0, 100, "Redirect address on list block"]
}

bl_stat = {
	"connect": 0l,
	"block": 0l,
	"notify": 0l,
	"except": 0l,
	"lookup": 0l,
	"quote": time.time (),
	"update": time.time (),
	"proxy": time.time (),
	"ledokol": False
}

bl_lang = {}

bl_list = [
	#["http://list.iblocklist.com/?list=ijfqtofzixtwayqovmxn&fileformat=p2p&archiveformat=gz", "gzip-p2p", "TBG - Primary", 0, 0, 1, 1, 0, 0],
	#["http://list.iblocklist.com/?list=xoebmbyexwuiogmbyprb&fileformat=p2p&archiveformat=gz", "gzip-p2p", "Bluetack - Proxy", 0, 0, 1, 1, 1, 0],
	#["http://te-home.net/blacklist.php?do=load&list=AP2P", "p2p", "TE - AP2P", 0, 0, 1, 1, 0, 0],
	#["http://te-home.net/blacklist.php?do=load&list=Proxy", "p2p", "TE - Proxy", 0, 0, 1, 1, 1, 0],
	#["http://te-home.net/blacklist.php?do=load&list=SOCKS", "p2p", "TE - SOCKS", 0, 0, 1, 1, 1, 0],
	#["http://ledo.feardc.net/mirror/torexit.list", "single", "Tor exit", 60, 0, 1, 1, 1, 0],
	#["http://ledo.feardc.net/mirror/torserver.list", "single", "Tor server", 60, 0, 1, 1, 1, 0],
	#["http://stopforumspam.com/downloads/listed_ip_7.gz", "gzip-single", "Stop forum spam", 1440, 0, 1, 1, 1, 0]
]

bl_item = [[] for pos in xrange (256)]
bl_prox = [[] for pos in xrange (256)]
bl_myli = []
bl_asn = []
bl_exli = []
bl_feed = []

def bl_main ():
	global bl_defs, bl_conf, bl_list, bl_myli, bl_exli

	vh.SQL (
		"create table if not exists `py_bl_conf` ("\
			"`name` varchar(255) not null primary key,"\
			"`value` text not null"\
		")"
	)

	vh.SQL (
		"create table if not exists `py_bl_list` ("\
			"`list` varchar(255) not null primary key,"\
			"`type` varchar(25) not null,"\
			"`title` varchar(255) not null,"\
			"`update` smallint(4) unsigned not null default 0,"\
			"`off` tinyint(1) unsigned not null default 0,"\
			"`action` tinyint(1) unsigned not null default 1,"\
			"`except` tinyint(1) unsigned not null default 1,"\
			"`redirect` tinyint(1) unsigned not null default 0"\
		")"
	)

	vh.SQL (
		"create table if not exists `py_bl_myli` ("\
			"`loaddr` int(10) unsigned not null,"\
			"`hiaddr` int(10) unsigned not null,"\
			"`title` varchar(255) null default null,"\
			"`off` tinyint(1) unsigned not null default 0,"\
			"unique `addr_index` (`loaddr`, `hiaddr`)"\
		")"
	)

	vh.SQL (
		"create table if not exists `py_bl_asn` ("\
			"`asn` varchar(255) not null primary key,"\
			"`off` tinyint(1) unsigned not null default 0"\
		")"
	)

	vh.SQL (
		"create table if not exists `py_bl_exli` ("\
			"`loaddr` int(10) unsigned not null,"\
			"`hiaddr` int(10) unsigned not null,"\
			"`title` varchar(255) null default null,"\
			"`off` tinyint(1) unsigned not null default 0,"\
			"unique `addr_index` (`loaddr`, `hiaddr`)"\
		")"
	)

	vh.SQL ("alter table `py_bl_conf` change column `value` `value` text not null")
	vh.SQL ("alter table `py_bl_list` add column `off` tinyint(1) unsigned not null default 0 after `update`")
	vh.SQL ("alter table `py_bl_list` add column `action` tinyint(1) unsigned not null default 1 after `off`")
	vh.SQL ("alter table `py_bl_list` add column `except` tinyint(1) unsigned not null default 1 after `action`")
	vh.SQL ("alter table `py_bl_list` add column `redirect` tinyint(1) unsigned not null default 0 after `except`")
	vh.SQL ("alter table `py_bl_myli` add column `off` tinyint(1) unsigned not null default 0 after `title`")
	vh.SQL ("alter table `py_bl_exli` add column `off` tinyint(1) unsigned not null default 0 after `title`")

	for name, value in bl_conf.iteritems ():
		vh.SQL ("insert ignore into `py_bl_conf` (`name`, `value`) values ('%s', '%s')" % (bl_repsql (name), bl_repsql (str (value [0]))))

	sql, rows = vh.SQL ("select * from `py_bl_conf`", 100) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_setconf (item [0], item [1], False)

	bl_langfile (bl_conf ["lang_pref"][0])
	sql, rows = vh.SQL ("select * from `py_bl_list` order by `off` asc, `action` desc, `title` asc", 100) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_list.append ([item [0], item [1], item [2], int (item [3]), int (item [4]), int (item [5]), int (item [6]), int (item [7]), 0])

	if bl_conf ["nick_bot"][0]:
		bl_addbot (bl_conf ["nick_bot"][0])

	out = (bl_getlang ("Blacklist %s startup") + ":\r\n\r\n") % bl_defs ["version"]
	out += bl_reload ()
	sql, rows = vh.SQL ("select * from `py_bl_myli`", 10000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_myli.append ([int (item [0]), int (item [1]), bl_getlang ("My item") if item [2] == "NULL" else item [2], int (item [3])])

	out += " [*] %s: %s\r\n" % (bl_getlang ("My list"), str (len (rows)))
	sql, rows = vh.SQL ("select * from `py_bl_asn`", 10000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_asn.append ([item [0], int (item [1])])

	out += " [*] %s: %s\r\n" % (bl_getlang ("ASN list"), str (len (rows)))
	sql, rows = vh.SQL ("select * from `py_bl_exli`", 10000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_exli.append ([int (item [0]), int (item [1]), bl_getlang ("Exception") if item [2] == "NULL" else item [2], int (item [3])])

	out += " [*] %s: %s\r\n" % (bl_getlang ("Exception"), str (len (rows)))

	if bl_conf ["prox_lookup"][0]:
		fail, res = True, bl_curlver ()
		out += (" [*] " + bl_getlang ("%s version: %s") + "\r\n") % ("cURL", res [1])

		if res [0]:
			res = bl_makedir (bl_defs ["datadir"])
			out += (" [*] " + bl_getlang ("Data directory: %s") + "\r\n") % res [1]

			if res [0]:
				try:
					import fake_useragent
					bl_defs ["useragent"][1] = fake_useragent.UserAgent ()
				except:
					pass

				out += (" [*] " + bl_getlang ("User agent: %s") + "\r\n") % bl_useragent (True)
				fail = False

		if fail:
			bl_setconf ("prox_lookup", "0")

	bl_notify (out)

def bl_import (list, type, title, action, exuse, redir, update = False): # gzip-p2p, gzip-emule, gzip-range, gzip-single, zip-p2p, zip-emule, zip-range, zip-single, p2p, emule, range, single
	global bl_defs, bl_conf, bl_item
	file = None

	if "://" in list:
		try:
			file = urllib2.urlopen (urllib2.Request (list, None, {"Referer": bl_defs ["referer"].decode ("hex"), "User-agent": bl_useragent ()}), None, bl_conf ["time_down"][0])
		except urllib2.HTTPError:
			return bl_getlang ("Failed with HTTP error")
		except urllib2.URLError:
			return bl_getlang ("Failed with URL error")
		except:
			return bl_getlang ("Failed with unknown error")
	else:
		try:
			file = open (list, "r")
		except:
			pass

	if not file:
		return bl_getlang ("Failed to open URL") if "://" in list else bl_getlang ("Failed to open file")

	find = None

	if "p2p" in type:
		find = "(.*)\\:(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\-(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})"
	elif "emule" in type:
		find = "(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3}) \\- (\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3}) \\, \\d{1,3} \\, (.*)"
	elif "range" in type:
		find = "(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\-(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})"
	elif "single" in type:
		find = "(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})"

	if not find:
		file.close ()
		return bl_getlang ("Unknown list type")

	try:
		find = re.compile ("^" + find + "$")
	except:
		file.close ()
		return bl_getlang ("Failed to compile pattern")

	if "gzip" in type or "zip" in type:
		data = None

		try:
			data = StringIO.StringIO (file.read ())
		except:
			pass

		file.close ()

		if not data:
			return bl_getlang ("Failed to read data")

		if "gzip" in type:
			try:
				file = gzip.GzipFile (fileobj = data)
				file.read (1)
			except:
				return bl_getlang ("File is not compressed with GZIP")
		elif "zip" in type:
			try:
				arch = zipfile.ZipFile (file = data)
				file = arch.open (arch.namelist () [0])
				arch.close ()
				file.read (1)
			except:
				return bl_getlang ("File is not compressed with ZIP")

	temp = []

	for line in file:
		part = find.findall (line.replace ("\r", "").replace ("\n", ""))

		if part:
			name, loaddr, hiaddr = None, None, None

			if "p2p" in type:
				name = part [0][0] or title
				loaddr = str (int (part [0][1])) + "." + str (int (part [0][2])) + "." + str (int (part [0][3])) + "." + str (int (part [0][4]))
				hiaddr = str (int (part [0][5])) + "." + str (int (part [0][6])) + "." + str (int (part [0][7])) + "." + str (int (part [0][8]))
			elif "emule" in type:
				name = part [0][8] or title
				loaddr = str (int (part [0][0])) + "." + str (int (part [0][1])) + "." + str (int (part [0][2])) + "." + str (int (part [0][3]))
				hiaddr = str (int (part [0][4])) + "." + str (int (part [0][5])) + "." + str (int (part [0][6])) + "." + str (int (part [0][7]))
			elif "range" in type:
				name = title
				loaddr = str (int (part [0][0])) + "." + str (int (part [0][1])) + "." + str (int (part [0][2])) + "." + str (int (part [0][3]))
				hiaddr = str (int (part [0][4])) + "." + str (int (part [0][5])) + "." + str (int (part [0][6])) + "." + str (int (part [0][7]))
			elif "single" in type:
				name = title
				loaddr = str (int (part [0][0])) + "." + str (int (part [0][1])) + "." + str (int (part [0][2])) + "." + str (int (part [0][3]))
				hiaddr = loaddr

			if name and loaddr and hiaddr and bl_validaddr (loaddr) and bl_validaddr (hiaddr):
				temp.append ([bl_addrtoint (loaddr), bl_addrtoint (hiaddr), name.replace ("\\'", "'").replace ("\\\"", "\"").replace ("\\&", "&").replace ("\\\\", "\\"), action, exuse, redir])

	file.close ()

	for item in temp:
		for pos in xrange (item [0] >> 24, (item [1] >> 24) + 1):
			if not update or not item in bl_item [pos]:
				bl_item [pos].append (item)

	return bl_getlang ("%s items loaded") % str (len (temp))

def bl_reload ():
	global bl_list, bl_item
	del bl_item [:]
	bl_item = [[] for pos in xrange (256)]
	out = ""

	for id, item in enumerate (bl_list):
		if not item [4]:
			out += " [*] %s: %s\r\n" % (item [2], bl_import (item [0], item [1], item [2], item [5], item [6], item [7]))

			if item [3]:
				bl_list [id][8] = time.time ()

	return out

def bl_lookup (data):
	global bl_conf
	list = None

	try:
		list = json.loads (data)
	except:
		return [False, bl_getlang ("Failed to load JSON")]

	if not list:
		return [False, bl_getlang ("Failed to parse JSON")]

	if not "status" in list:
		return [False, bl_getlang ("Failed to get status")]

	if list ["status"] == "error":
		return [False, bl_getlang ("Error status: %s") % str (list ["message"]) if "message" in list else bl_getlang ("Unknown")]

	if list ["status"] != "success":
		return [False, bl_getlang ("Unexpected status: %s") % str (list ["status"])]

	if not "result" in list:
		return [False, bl_getlang ("Failed to get result")]

	try:
		res = float (list ["result"])
	except:
		res = -1

	if res < 0:
		return [False, bl_getlang ("Failed to get result")]

	res = int (res * 100)

	if res >= bl_conf ["prox_match"][0]:
		return [True, res]

	return [False, res]

def bl_curlver ():
	global bl_defs
	out = None

	try:
		out = subprocess.check_output (bl_defs ["curlver"])
	except:
		pass

	if not out:
		return [False, bl_getlang ("Failed to execute command")]

	find = re.compile ("(\\d+[\\.\\d]+)").search (out)

	if not find:
		return [False, bl_getlang ("Failed to get version")]

	return [True, find.group (1)]

def bl_httpreq (url):
	global bl_defs, bl_conf
	file = None

	try:
		file = urllib2.urlopen (urllib2.Request (url, None, {"Referer": bl_defs ["referer"].decode ("hex"), "User-agent": bl_useragent ()}), None, bl_conf ["time_down"][0])
	except urllib2.HTTPError:
		return [False, bl_getlang ("Failed with HTTP error")]
	except urllib2.URLError:
		return [False, bl_getlang ("Failed with URL error")]
	except:
		return [False, bl_getlang ("Failed with unknown error")]

	if not file:
		return [False, bl_getlang ("Failed to open URL")]

	data = None

	try:
		data = file.read ()
	except:
		pass

	file.close ()

	if data:
		return [True, data]
	else:
		return [False, bl_getlang ("Failed to read data")]

def bl_remfile (file):
	res = True

	try:
		os.unlink (file)
	except:
		res = False

	return res

def bl_makedir (dir):
	if not os.path.exists (dir):
		try:
			os.makedirs (dir)
		except:
			return [False, bl_getlang ("Failed to create directory")]
	else:
		for file in os.listdir (dir):
			file = os.path.join (dir, file)

			if os.path.isfile (file):
				bl_remfile (file)

	return [True, dir]

def bl_extry (addr, code, intaddr, loaddr, hiaddr):
	global bl_conf, bl_exli

	for item in bl_exli:
		if not item [3] and intaddr >= item [0] and intaddr <= item [1]:
			return

	bl_notify (bl_getlang ("Exception list out of IP %s.%s: %s") % (addr, code, bl_inttoaddr (loaddr) + "-" + bl_inttoaddr (hiaddr)))

	if bl_conf ["extry_getasn"][0]:
		bl_notify (bl_getlang ("ASN: %s") % bl_getasn (addr))

def bl_excheck (addr, intaddr, code, asn, urlasn, name, exuse, nick = None, chat = False, skip = False):
	global bl_conf, bl_stat, bl_exli

	if exuse:
		if bl_conf ["code_except"][0] and code and str ().join ([" ", code, " "]) in str ().join ([" ", bl_conf ["code_except"][0], " "]): # country code exception
			if bl_waitfeed (addr):
				if nick:
					if chat:
						bl_notify ((bl_getlang ("Blacklisted chat exception from %s with IP %s.%s: %s") + " | %s") % (nick, addr, code, name, bl_getlang ("Excepted country: %s=%s") % (code, vh.GetIPCN (addr) or "??")))
					else:
						bl_notify ((bl_getlang ("Blacklisted login exception from %s with IP %s.%s: %s") + " | %s") % (nick, addr, code, name, bl_getlang ("Excepted country: %s=%s") % (code, vh.GetIPCN (addr) or "??")))
				else:
					bl_notify ((bl_getlang ("Blacklisted connection exception from %s.%s: %s") + " | %s") % (addr, code, name, bl_getlang ("Excepted country: %s=%s") % (code, vh.GetIPCN (addr) or "??")))

			if not nick:
				bl_stat ["except"] += 1

			return 1

		if bl_conf ["asn_except"][0] and asn and str ().join ([" ", asn, " "]) in str ().join ([" ", bl_conf ["asn_except"][0], " "]): # asn exception
			if bl_waitfeed (addr):
				if nick:
					if chat:
						bl_notify ((bl_getlang ("Blacklisted chat exception from %s with IP %s.%s: %s") + " | %s") % (nick, addr, code, name, bl_getlang ("Excepted ASN: %s") % urlasn))
					else:
						bl_notify ((bl_getlang ("Blacklisted login exception from %s with IP %s.%s: %s") + " | %s") % (nick, addr, code, name, bl_getlang ("Excepted ASN: %s") % urlasn))
				else:
					bl_notify ((bl_getlang ("Blacklisted connection exception from %s.%s: %s") + " | %s") % (addr, code, name, bl_getlang ("Excepted ASN: %s") % urlasn))

			if not nick:
				bl_stat ["except"] += 1

			return 1

		for item in bl_exli: # exception list
			if not item [3] and intaddr >= item [0] and intaddr <= item [1]:
				if bl_waitfeed (addr):
					if nick:
						if chat:
							bl_notify ((bl_getlang ("Blacklisted chat exception from %s with IP %s.%s: %s") + " | %s") % (nick, addr, code, name, item [2]))
						else:
							bl_notify ((bl_getlang ("Blacklisted login exception from %s with IP %s.%s: %s") + " | %s") % (nick, addr, code, name, item [2]))
					else:
						bl_notify ((bl_getlang ("Blacklisted connection exception from %s.%s: %s") + " | %s") % (addr, code, name, item [2]))

				if not nick:
					bl_stat ["except"] += 1

				return 1

	if bl_waitfeed (addr):
		if nick:
			if chat:
				if not skip:
					bl_notify (bl_getlang ("Blocking blacklisted chat from %s with IP %s.%s: %s") % (nick, addr, code, name))
			else:
				bl_notify (bl_getlang ("Blocking blacklisted login from %s with IP %s.%s: %s") % (nick, addr, code, name))
		else:
			bl_notify (bl_getlang ("Blocking blacklisted connection from %s.%s: %s") % (addr, code, name))

	if not nick:
		bl_stat ["block"] += 1

	return 0

def bl_waitfeed (addr, prev = False):
	global bl_defs, bl_conf, bl_feed
	mins, now = (bl_conf ["time_feed"][0] * 60), time.time ()

	for id, item in enumerate (bl_feed):
		if addr == item [0]:
			dif = now - item [1]

			if dif == 0 or dif >= mins or (prev and dif <= bl_defs ["prevfeed"]):
				bl_feed [id][1] = now
				return 1

			return 0

	bl_feed.append ([addr, now])
	return 1

def bl_langfile (pref):
	global bl_lang
	bl_lang = {}

	if not pref or pref == "en":
		return True

	name = os.path.join (vh.basedir, "scripts", ("black_%s.lang" % pref))

	if not os.path.isfile (name):
		return False

	file = None

	try:
		file = open (name, "r")
	except:
		pass

	if not file:
		return False

	find = re.compile ("^(.+)\|(.+)$")

	for line in file:
		if len (line) > 2 and line [0:1] != "#":
			part = find.findall (line.replace ("\r", "").replace ("\n", ""))

			if part and part [0][0].count ("%s") == part [0][1].count ("%s"):
				bl_lang [part [0][0]] = part [0][1]

	file.close ()
	return True

def bl_getlang (data):
	global bl_lang

	if data in bl_lang:
		return bl_lang [data]

	return data

def bl_hubconf (name, deva):
	res = vh.GetConfig (vh.config_name, name)

	if res == None:
		return deva

	res = str (res)

	if res.isdigit () or (res [:1] == "-" and res [1:].isdigit ()):
		res = int (res)

	return res

def bl_hubver (a, b, c, d):
	vers = bl_hubconf ("hub_version", "0.0.0.0")
	pars = re.findall ("^(\\d+)\\.(\\d+)\\.(\\d+)\\.(\\d+)$", vers)

	if not pars or not pars [0][0] or not pars [0][1] or not pars [0][2] or not pars [0][3]:
		return False

	va, vb, vc, vd = int (pars [0][0]), int (pars [0][1]), int (pars [0][2]), int (pars [0][3])

	if va > a:
		return True
	elif va < a:
		return False

	if vb > b:
		return True
	elif vb < b:
		return False

	if vc > c:
		return True
	elif vc < c:
		return False

	if vd > d:
		return True
	elif vd < d:
		return False

	return True # all numbers are equal

def bl_getconf (name):
	global bl_conf

	if not name in bl_conf:
		return None

	return bl_conf [name][0]

def bl_setconf (name, value, update = True):
	global bl_defs, bl_conf, bl_prox

	if not name in bl_conf:
		return bl_getlang ("Item not found")

	old, new = bl_conf [name][0], str (value)

	if bl_conf [name][1] == "int":
		if not new.isdigit ():
			return bl_getlang ("Value is not a number")

		new = int (new)

		if new < bl_conf [name][2]:
			return bl_getlang ("Value too low")
		elif new > bl_conf [name][3]:
			return bl_getlang ("Value too high")
	else:
		if len (new) < bl_conf [name][2]:
			return bl_getlang ("Value too short")
		elif len (new) > bl_conf [name][3]:
			return bl_getlang ("Value too long")

	if update:
		if name == "nick_bot":
			if new and not old:
				bl_addbot (new)
			elif not new and old:
				bl_delbot (old)
			elif new != old:
				bl_delbot (old)
				bl_addbot (new)

		elif name == "prox_lookup":
			if new and not old:
				res = bl_curlver ()

				if not res [0]:
					return res [1]

				bl_notify (bl_getlang ("%s version: %s") % ("cURL", res [1]))
				res = bl_makedir (bl_defs ["datadir"])

				if not res [0]:
					return res [1]

				bl_notify (bl_getlang ("Data directory: %s") % res [1])

				try:
					import fake_useragent
					bl_defs ["useragent"][1] = fake_useragent.UserAgent ()
				except:
					pass

				bl_notify (bl_getlang ("User agent: %s") % bl_useragent (True))
			elif not new and old:
				del bl_prox [:]
				bl_prox = [[] for pos in xrange (256)]
				bl_makedir (bl_defs ["datadir"])
				bl_defs ["useragent"][1] = None

		elif name == "lang_pref":
			if new != old:
				bl_langfile (new)

		vh.SQL ("update `py_bl_conf` set `value` = '%s' where `name` = '%s'" % (bl_repsql (str (new)), bl_repsql (name)))

	bl_conf [name][0] = new
	return "%s -> %s" % (str (old), str (new))

def bl_addrtoint (addr):
	res = 0

	try:
		res = struct.unpack ("!L", socket.inet_aton (addr)) [0]
	except:
		pass

	return res

def bl_inttoaddr (addr):
	res = "0.0.0.0"

	try:
		res = socket.inet_ntoa (struct.pack ("!L", int (addr)))
	except:
		pass

	return res

def bl_validaddr (addr):
	if len (addr) < 7 or len (addr) > 15:
		return 0

	num = 0

	for part in addr.split ("."):
		if len (part) < 1 or len (part) > 3 or not part.isdigit () or int (part) < 0 or int (part) > 255:
			return 0

		num += 1

	return (1 if num == 4 else 0)

def bl_getasn (addr):
	try:
		asn = vh.GetIPASN (addr)

		if asn:
			if re.match ("^AS\d+", asn):
				asn = "https://ipinfo.io/" + asn

			return asn
		else:
			return bl_getlang ("Information not found")
	except:
		return bl_getlang ("Function not supported")

def bl_useragent (rand = False):
	global bl_defs
	res = ""

	if rand and bl_defs ["useragent"][1]:
		res = str (bl_defs ["useragent"][1]["random"])
	else:
		res = bl_defs ["useragent"][0].decode ("hex") % bl_defs ["version"]

	return res

def bl_repsql (data):
	return data.replace (chr (92), chr (92) + chr (92)).replace (chr (34), chr (92) + chr (34)).replace (chr (39), chr (92) + chr (39))

def bl_repnmdc (data, out = False):
	if out:
		return data.replace ("&#124;", "|").replace ("&#36;", "$")
	else:
		return data.replace ("|", "&#124;").replace ("$", "&#36;")

def bl_reply (user, data):
	if bl_hubver (1, 0, 2, 16):
		vh.SendDataToUser ("<%s> %s|" % (vh.botname, bl_repnmdc (data)), user, bl_hubconf ("delayed_chat", 0)) # chat is not delayed by default
	else:
		vh.SendDataToUser ("<%s> %s|" % (vh.botname, bl_repnmdc (data)), user)

def bl_notify (data):
	global bl_conf

	if bl_conf ["nick_feed"][0]:
		vh.SendDataToUser ("$To: %s From: %s $<%s> %s|" % (bl_conf ["nick_feed"][0], vh.opchatname, vh.opchatname, bl_repnmdc (data)), bl_conf ["nick_feed"][0])
	elif bl_conf ["nick_bot"][0]:
		vh.SendPMToAll (bl_repnmdc (data), bl_conf ["nick_bot"][0], bl_conf ["class_feed"][0], 10)
	else:
		vh.SendPMToAll (bl_repnmdc (data), vh.opchatname, bl_conf ["class_feed"][0], 10)

		try:
			vh.ScriptCommand ("opchat_to_all", "[%s] <%s> %s" % (str (bl_conf ["class_feed"][0]), vh.opchatname, data)) # to catch in ledokol
		except:
			pass

def bl_delaychat (list, block = False):
	for data in list:
		if block: # send block message
			if data [:7] == "$MCTo: ": # mcto
				pars = re.findall ("^\$MCTo\: ([^ ]+) From\: ([^ ]+) \$<[^ ]+> (.*)$", data)

				if pars and pars [0][0] and pars [0][1] and pars [0][2]:
					bl_notify (bl_getlang ("Blocking private main chat message from %s with IP %s.%s detected as public proxy to %s with IP %s.%s: %s") % (pars [0][1], vh.GetUserIP (pars [0][1]), vh.GetUserCC (pars [0][1]), pars [0][0], vh.GetUserIP (pars [0][0]), vh.GetUserCC (pars [0][0]), pars [0][2]))
					bl_reply (pars [0][1], bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address."))

			elif data [:5] == "$To: ": # pm
				pars = re.findall ("^\$To\: ([^ ]+) From\: ([^ ]+) \$<[^ ]+> (.*)$", data)

				if pars and pars [0][0] and pars [0][1] and pars [0][2]:
					bl_notify (bl_getlang ("Blocking private message from %s with IP %s.%s detected as public proxy to %s with IP %s.%s: %s") % (pars [0][1], vh.GetUserIP (pars [0][1]), vh.GetUserCC (pars [0][1]), pars [0][0], vh.GetUserIP (pars [0][0]), vh.GetUserCC (pars [0][0]), pars [0][2]))
					vh.SendDataToUser ("$To: %s From: %s $<%s> %s|" % (pars [0][1], pars [0][0], vh.botname, bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address.")), pars [0][1])

			else: # mc
				pars = re.findall ("^<([^ ]+)> (.*)$", data)

				if pars and pars [0][0] and pars [0][1]:
					bl_notify (bl_getlang ("Blocking main chat message from %s with IP %s.%s detected as public proxy: %s") % (pars [0][0], vh.GetUserIP (pars [0][0]), vh.GetUserCC (pars [0][0]), pars [0][1]))
					bl_reply (pars [0][0], bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address."))

		else: # send chat messages via ledokol
			try:
				if data [:7] == "$MCTo: ": # mcto
					if bl_stat ["ledokol"]:
						vh.ScriptCommand ("delayed_mcto_to_user", data)

					else: # send by self
						pars = re.findall ("^\$MCTo\: ([^ ]+) From\: ([^ ]+) \$(<[^ ]+> .*)$", data)

						if pars and pars [0][0] and pars [0][1] and pars [0][2] and vh.GetUserClass (pars [0][0]) >= 0 and vh.GetUserClass (pars [0][1]) >= 0:
							vh.SendDataToUser ("%s|" % pars [0][2], pars [0][0]) # todo: check mcto support flag when supported by plugin, for now send regular chat message

				elif data [:5] == "$To: ": # pm
					if bl_stat ["ledokol"]:
						vh.ScriptCommand ("delayed_pm_to_user", data)

					else: # send by self
						pars = re.findall ("^\$To\: ([^ ]+) From\: ([^ ]+) \$<[^ ]+> .*$", data)

						if pars and pars [0][0] and pars [0][1] and vh.GetUserClass (pars [0][0]) >= 0 and vh.GetUserClass (pars [0][1]) >= 0:
							vh.SendDataToUser ("%s|" % data, pars [0][0])

				elif data [:1] == "<": # mc
					if bl_stat ["ledokol"]:
						vh.ScriptCommand ("delayed_chat_to_all", data)

					else: # send by self
						pars = re.findall ("^<([^ ]+)> .*$", data)

						if pars and pars [0] and vh.GetUserClass (pars [0]) >= 0:
							if bl_hubver (1, 0, 2, 16):
								vh.SendDataToAll ("%s|" % data, 0, 10, bl_hubconf ("delayed_chat", 0)) # chat is not delayed by default
							else:
								vh.SendDataToAll ("%s|" % data, 0, 10)

			except:
				pass

def bl_addbot (nick):
	global bl_defs, bl_conf
	vh.AddRobot (nick, bl_conf ["class_feed"][0], bl_defs ["botdesc"].decode ("hex") % bl_defs ["version"], chr (1), "", "0")

def bl_delbot (nick):
	vh.DelRobot (nick)

def bl_chatdata (nick, data, rem = False):
	global bl_defs, bl_conf, bl_prox, bl_stat

	if bl_conf ["prox_lookup"][0] < 2 or vh.GetUserClass (nick) >= bl_conf ["class_skip"][0] or (bl_conf ["nick_skip"][0] and str ().join ([" ", nick, " "]) in str ().join ([" ", bl_conf ["nick_skip"][0], " "])):
		return 1

	addr = vh.GetUserIP (nick)

	if not addr:
		return 1

	code = vh.GetUserCC (nick)

	if not code:
		code = "??"

	if code == "L1" or code == "P1":
		return 1

	bl_stat ["ledokol"] = False # check ledokol status

	try:
		vh.ScriptCommand ("are_you_there", "ledokol")
	except:
		pass

	intaddr = bl_addrtoint (addr)
	addrpos = intaddr >> 24
	size = 0

	for id, item in enumerate (bl_prox [addrpos]):
		if addr == item [0]:
			if item [3] < 2:
				if not nick in item [1]:
					bl_prox [addrpos][id][1].append (nick)

				if bl_conf ["action_proxy"][0] == 2: # add message to queue if enabled
					if not rem and data [:5] == "$To: ": # pm
						pars = re.findall ("^\$To\: ([^ ]+) From\: [^ ]+ \$<[^ ]+> .*$", data)

						if pars and pars [0]:
							vh.SendDataToUser ("$To: %s From: %s $<%s> %s|" % (nick, pars [0], vh.botname, bl_getlang ("Your message will be delayed for proxy lookup of your IP address.")), nick)

					else: # mc
						bl_reply (nick, bl_getlang ("Your message will be delayed for proxy lookup of your IP address."))

					if rem: # remove last main chat history message in ledokol, dont ask why
						try:
							vh.ScriptCommand ("remove_history_line", data)
						except:
							pass

					bl_prox [addrpos][id][2].append (data)
					return 0

			elif item [3] == 2: # drop user mode
				res = bl_excheck (addr, intaddr, code, None, None, bl_getlang ("Public proxy"), bl_conf ["except_proxy"][0], nick, True, True)

				if not res and rem: # remove last main chat history message in ledokol, dont ask why
					try:
						vh.ScriptCommand ("remove_history_line", data)
					except:
						pass

				return res

			elif item [3] == 3: # block chat mode
				if not rem and data [:7] == "$MCTo: ": # mcto
					pars = re.findall ("^\$MCTo\: ([^ ]+) From\: [^ ]+ \$<[^ ]+> (.*)$", data)

					if pars and pars [0][0] and pars [0][1]:
						bl_notify (bl_getlang ("Blocking private main chat message from %s with IP %s.%s detected as public proxy to %s with IP %s.%s: %s") % (nick, vh.GetUserIP (nick), vh.GetUserCC (nick), pars [0][0], vh.GetUserIP (pars [0][0]), vh.GetUserCC (pars [0][0]), pars [0][1]))
						bl_reply (nick, bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address."))

				elif not rem and data [:5] == "$To: ": # pm
					pars = re.findall ("^\$To\: ([^ ]+) From\: [^ ]+ \$<[^ ]+> (.*)$", data)

					if pars and pars [0][0] and pars [0][1]:
						bl_notify (bl_getlang ("Blocking private message from %s with IP %s.%s detected as public proxy to %s with IP %s.%s: %s") % (nick, vh.GetUserIP (nick), vh.GetUserCC (nick), pars [0][0], vh.GetUserIP (pars [0][0]), vh.GetUserCC (pars [0][0]), pars [0][1]))
						vh.SendDataToUser ("$To: %s From: %s $<%s> %s|" % (nick, pars [0][0], vh.botname, bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address.")), nick)

				else: # mc
					pars = re.findall ("^<[^ ]+> (.*)$", data)

					if pars and pars [0]:
						bl_notify (bl_getlang ("Blocking main chat message from %s with IP %s.%s detected as public proxy: %s") % (nick, vh.GetUserIP (nick), vh.GetUserCC (nick), pars [0]))
						bl_reply (nick, bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address."))

				if rem: # remove last main chat history message in ledokol, dont ask why
					try:
						vh.ScriptCommand ("remove_history_line", data)
					except:
						pass

				return 0

			#elif item [3] == 4: # exception
				#pass

			return 1 # nothing to do

		if not item [3]:
			size += 1

	if size < bl_conf ["prox_queue"][0]:
		now = time.time ()

		if bl_conf ["prox_quote"][0] > 0: # check daily quote
			if bl_stat ["lookup"] == 0: # first time
				bl_stat ["quote"] = now

			elif bl_stat ["lookup"] >= bl_conf ["prox_quote"][0]:
				if now - bl_stat ["quote"] >= bl_defs ["quotesec"]:
					if bl_conf ["prox_debug"][0] > 2:
						bl_notify (bl_getlang ("Resetting proxy lookup quote limit: %s") % str (bl_conf ["prox_quote"][0]))

					bl_stat ["lookup"], bl_stat ["quote"] = 0, now

				else:
					if bl_conf ["prox_debug"][0] > 1:
						bl_notify (bl_getlang ("Proxy lookup quote limit reached on chat user from IP %s.%s: %s") % (addr, code, nick))

					return 1

		bl_stat ["lookup"] = bl_stat ["lookup"] + 1
		bl_prox [addrpos].append ([addr, [nick], [data] if bl_conf ["action_proxy"][0] == 2 else [], 0, now, True]) # add message to queue if enabled

		if bl_conf ["prox_debug"][0] > 1:
			bl_notify (bl_getlang ("Checking chat user from IP %s.%s: %s") % (addr, code, nick))

		if bl_conf ["action_proxy"][0] == 2: # notify user
			if not rem and data [:5] == "$To: ": # pm
				pars = re.findall ("^\$To\: ([^ ]+) From\: [^ ]+ \$<[^ ]+> .*$", data)

				if pars and pars [0]:
					vh.SendDataToUser ("$To: %s From: %s $<%s> %s|" % (nick, pars [0], vh.botname, bl_getlang ("Your message will be delayed for proxy lookup of your IP address.")), nick)

			else: # mc
				bl_reply (nick, bl_getlang ("Your message will be delayed for proxy lookup of your IP address."))

			if rem: # remove last main chat history message in ledokol, dont ask why
				try:
					vh.ScriptCommand ("remove_history_line", data)
				except:
					pass

			return 0

	return 1

def UnLoad ():
	global bl_conf

	if bl_conf ["nick_bot"][0]:
		bl_delbot (bl_conf ["nick_bot"][0])

	return 1

def OnScriptCommand (name, data, plug, file):
	global bl_stat

	if name == "yes_im_here" and data == "ledokol" and plug == "lua" and file [-11:] == "ledokol.lua": # todo: this is valid only during last message, not sure what happens if we get another one inbetween
		bl_stat ["ledokol"] = True

	return 1

def OnNewConn (addr):
	global bl_conf, bl_stat, bl_defs, bl_item, bl_myli, bl_asn, bl_prox
	bl_stat ["connect"] += 1
	code = None

	if bl_conf ["code_block"][0]:
		code = vh.GetIPCC (addr) or "??" # if not code

		if str ().join ([" ", code, " "]) in str ().join ([" ", bl_conf ["code_block"][0], " "]):
			if bl_waitfeed (addr):
				bl_notify (bl_getlang ("Blocking blacklisted connection from %s.%s: %s") % (addr, code, bl_getlang ("Blocked country: %s=%s") % (code, vh.GetIPCN (addr) or "??")))

			bl_stat ["block"] += 1

			if bl_conf ["redir_code"][0] and bl_hubver (1, 2, 0, 1):
				return (bl_defs ["protmove"].decode ("hex") % bl_conf ["redir_code"][0], 0)

			return 0

	asn, asnum, urlasn = None, None, None

	if bl_conf ["asn_block"][0]: # get asn
		try:
			asn = vh.GetIPASN (addr) # if not asn

			if asn:
				urlasn = asn
				match = re.match ("^AS\d+", asn)

				if match:
					urlasn = "https://ipinfo.io/" + urlasn
					asnum = match.group (0)

					if str ().join ([" ", asnum, " "]) in str ().join ([" ", bl_conf ["asn_block"][0], " "]):
						if bl_waitfeed (addr):
							bl_notify (bl_getlang ("Blocking blacklisted connection from %s.%s: %s") % (addr, vh.GetIPCC (addr) or "??", bl_getlang ("Blocked ASN: %s") % urlasn))

						bl_stat ["block"] += 1

						if bl_conf ["redir_asn"][0] and bl_hubver (1, 2, 0, 1):
							return (bl_defs ["protmove"].decode ("hex") % bl_conf ["redir_asn"][0], 0)

						return 0

		except: # not supported
			pass

	intaddr = bl_addrtoint (addr)
	addrpos = intaddr >> 24

	if bl_conf ["prox_lookup"][0]: # check proxy
		if not code:
			code = vh.GetIPCC (addr) or "??"

		if code != "L1" and code != "P1" and time.time () - vh.starttime >= bl_conf ["prox_start"][0] * 60:
			for id, item in enumerate (bl_prox [addrpos]):
				if addr == item [0]:
					if item [3] == 2 and not bl_excheck (addr, intaddr, code, asnum, urlasn, bl_getlang ("Public proxy"), bl_conf ["except_proxy"][0]): # drop user mode, note: asn exception not supported
						if bl_conf ["redir_prox"][0] and bl_hubver (1, 2, 0, 1):
							return (bl_defs ["protmove"].decode ("hex") % bl_conf ["redir_prox"][0], 0)

						return 0

					break # dont return

	for item in bl_myli: # my list first
		if not item [3] and intaddr >= item [0] and intaddr <= item [1]:
			if not code: # will be set only once
				code = vh.GetIPCC (addr) or "??"

			if not bl_conf ["action_mylist"][0]: # notification only
				if bl_waitfeed (addr):
					bl_notify (bl_getlang ("Notifying blacklisted connection from %s.%s: %s") % (addr, code, item [2]))

				bl_stat ["notify"] += 1

			elif not bl_excheck (addr, intaddr, code, asnum, urlasn, item [2], bl_conf ["except_mylist"][0]): # note: asn exception not supported
				if bl_conf ["redir_my"][0] and bl_hubver (1, 2, 0, 1):
					return (bl_defs ["protmove"].decode ("hex") % bl_conf ["redir_my"][0], 0)

				return 0

			# dont break or return

	for item in bl_item [addrpos]:
		if intaddr >= item [0] and intaddr <= item [1]:
			if not code: # will be set only once
				code = vh.GetIPCC (addr) or "??"

			if not item [3]: # notification only
				if bl_waitfeed (addr):
					bl_notify (bl_getlang ("Notifying blacklisted connection from %s.%s: %s") % (addr, code, item [2]))

				bl_stat ["notify"] += 1

			elif not bl_excheck (addr, intaddr, code, asnum, urlasn, item [2], item [4]): # note: asn exception not supported
				if item [5] and bl_conf ["redir_list"][0] and bl_hubver (1, 2, 0, 1):
					return (bl_defs ["protmove"].decode ("hex") % bl_conf ["redir_list"][0], 0)

				return 0

			# dont break or return

	if bl_asn: # asn check
		if not asn:
			asn = vh.GetIPASN (addr)

		if asn:
			urlasn = asn
			match = re.match ("^AS\d+", asn)

			if match:
				urlasn = "https://ipinfo.io/" + urlasn
				asnum = match.group (0)
				lowasn = asn.lower ()

				for item in bl_asn:
					if not item [1] and item [0].lower () in lowasn:
						if not code: # will be set only once
							code = vh.GetIPCC (addr) or "??"

						if not bl_conf ["action_asnlist"][0]: # notification only
							if bl_conf ["asn_nofeed"][0] and asnum and str ().join ([" ", asnum, " "]) in str ().join ([" ", bl_conf ["asn_nofeed"][0], " "]): # skip notification
								pass
							elif bl_waitfeed (addr):
								bl_notify (bl_getlang ("Notifying blacklisted connection from %s.%s: %s") % (addr, code, urlasn))

							bl_stat ["notify"] += 1

						elif not bl_excheck (addr, intaddr, code, asnum, urlasn, urlasn, bl_conf ["except_asnlist"][0]):
							if bl_conf ["redir_asn"][0] and bl_hubver (1, 2, 0, 1):
								return (bl_defs ["protmove"].decode ("hex") % bl_conf ["redir_asn"][0], 0)

							return 0

						# dont break or return

	return 1

def OnUserLogin (nick):
	global bl_defs, bl_conf, bl_stat, bl_item, bl_prox, bl_myli
	addr = vh.GetUserIP (nick)

	if not addr:
		return 1

	code = vh.GetUserCC (nick)

	if not code:
		code = "??"

	intaddr = bl_addrtoint (addr)

	for item in bl_myli: # my list first
		if not item [3] and intaddr >= item [0] and intaddr <= item [1]:
			if not bl_conf ["action_mylist"][0]: # notification only
				if bl_waitfeed (addr, True):
					bl_notify (bl_getlang ("Notifying blacklisted login from %s with IP %s.%s: %s") % (nick, addr, code, item [2]))

					if bl_conf ["action_extry"][0]:
						bl_extry (addr, code, intaddr, item [0], item [1])

			# dont break or return

	addrpos = intaddr >> 24

	for item in bl_item [addrpos]:
		if intaddr >= item [0] and intaddr <= item [1]:
			if not item [3]: # notification only
				if bl_waitfeed (addr, True):
					bl_notify (bl_getlang ("Notifying blacklisted login from %s with IP %s.%s: %s") % (nick, addr, code, item [2]))

					if bl_conf ["action_extry"][0]:
						bl_extry (addr, code, intaddr, item [0], item [1])

			# dont break or return

	if code == "L1" or code == "P1" or vh.GetUserClass (nick) >= bl_conf ["class_skip"][0] or (bl_conf ["nick_skip"][0] and str ().join ([" ", nick, " "]) in str ().join ([" ", bl_conf ["nick_skip"][0], " "])):
		return 1

	now = time.time ()

	if not bl_conf ["prox_lookup"][0] or now - vh.starttime < bl_conf ["prox_start"][0] * 60:
		return 1

	size = 0

	for id, item in enumerate (bl_prox [addrpos]):
		if addr == item [0]:
			if item [3] < 2:
				if not nick in item [1]:
					bl_prox [addrpos][id][1].append (nick)

			#elif item [3] == 2: # drop user mode, checked on connect
				#return bl_excheck (addr, intaddr, code, None, None, bl_getlang ("Public proxy"), bl_conf ["except_proxy"][0], nick)

			elif item [3] == 3: # block chat mode
				if not bl_excheck (addr, intaddr, code, None, None, bl_getlang ("Public proxy"), bl_conf ["except_proxy"][0], nick, True):
					bl_reply (nick, bl_getlang ("You're not allowed to chat due to public proxy detection of your IP address."))

			#elif item [3] == 4: # exception
				#pass

			return 1 # nothing to do

		if not item [3]:
			size += 1

	if bl_conf ["prox_lookup"][0] == 1 and size < bl_conf ["prox_queue"][0]:
		if bl_conf ["prox_quote"][0] > 0: # check daily quote
			if bl_stat ["lookup"] == 0: # first time
				bl_stat ["quote"] = now

			elif bl_stat ["lookup"] >= bl_conf ["prox_quote"][0]:
				if now - bl_stat ["quote"] >= bl_defs ["quotesec"]:
					if bl_conf ["prox_debug"][0] > 2:
						bl_notify (bl_getlang ("Resetting proxy lookup quote limit: %s") % str (bl_conf ["prox_quote"][0]))

					bl_stat ["lookup"], bl_stat ["quote"] = 0, now

				else:
					if bl_conf ["prox_debug"][0] > 1:
						bl_notify (bl_getlang ("Proxy lookup quote limit reached on logged in user from IP %s.%s: %s") % (addr, code, nick))

					return 1

		bl_stat ["lookup"] = bl_stat ["lookup"] + 1
		bl_prox [addrpos].append ([addr, [nick], [], 0, now, False])

		if bl_conf ["prox_debug"][0] > 1:
			bl_notify (bl_getlang ("Checking logged in user from IP %s.%s: %s") % (addr, code, nick))

	return 1

def OnParsedMsgChat (nick, data):
	return bl_chatdata (nick, "<%s> %s" % (nick, data), True)

def OnParsedMsgPM (nick, data, user):
	return bl_chatdata (nick, "$To: %s From: %s $<%s> %s" % (user, nick, nick, data))

def OnParsedMsgMCTo (nick, data, user):
	return bl_chatdata (nick, "$MCTo: %s From: %s $<%s> %s" % (user, nick, nick, data))

def OnUserCommand (nick, data):
	if data [1:3] == "me" and (data [3:4] == "" or data [3:4] == " "):
		return OnParsedMsgChat (nick, data)

	return 1

def OnOperatorCommand (user, data):
	global bl_defs, bl_conf, bl_stat, bl_list, bl_item, bl_prox, bl_myli, bl_asn, bl_exli, bl_feed

	if data [1:3] == "bl":
		if vh.GetUserClass (user) < bl_conf ["class_conf"][0]:
			bl_reply (user, bl_getlang ("You don't have access to this command."))
			return 0

		if data [4:8] == "stat":
			size, lists, wcurl, acurl, myoff, asnoff, exoff = 0, 0, 0, 0, 0, 0, 0

			for pos in range (len (bl_item)):
				size += len (bl_item [pos])

			for item in bl_list:
				if not item [4]:
					lists += 1

			for item in bl_myli:
				if not item [3]:
					myoff += 1

			for item in bl_asn:
				if not item [1]:
					asnoff += 1

			for item in bl_exli:
				if not item [3]:
					exoff += 1

			for pos in range (len (bl_prox)):
				acurl += len (bl_prox [pos])

				for item in bl_prox [pos]:
					if item [3] < 3:
						wcurl += 1

			out = bl_getlang ("Blacklist statistics") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("Version: %s")) % bl_defs ["version"]
			out += ("\r\n [*] " + bl_getlang ("Translation: %s")) % (bl_conf ["lang_pref"][0] or "en").upper ()
			out += ("\r\n [*] " + bl_getlang ("Loaded lists: %s")) % (bl_getlang ("%s of %s") % (str (lists), str (len (bl_list))))
			out += ("\r\n [*] " + bl_getlang ("Blacklisted items: %s")) % str (size)
			out += ("\r\n [*] " + bl_getlang ("My items: %s")) % (bl_getlang ("%s of %s") % (str (myoff), str (len (bl_myli))))
			out += ("\r\n [*] " + bl_getlang ("ASN items: %s")) % (bl_getlang ("%s of %s") % (str (asnoff), str (len (bl_asn))))
			out += ("\r\n [*] " + bl_getlang ("Excepted items: %s")) % (bl_getlang ("%s of %s") % (str (exoff), str (len (bl_exli))))
			out += ("\r\n [*] " + bl_getlang ("Blocked connections: %s")) % str (bl_stat ["block"])
			out += ("\r\n [*] " + bl_getlang ("Notified connections: %s")) % str (bl_stat ["notify"])
			out += ("\r\n [*] " + bl_getlang ("Excepted connections: %s")) % str (bl_stat ["except"])
			out += ("\r\n [*] " + bl_getlang ("Total connections: %s")) % str (bl_stat ["connect"])
			out += ("\r\n [*] " + bl_getlang ("Waiting proxy lookups") + ": %s") % (bl_getlang ("%s of %s") % (str (wcurl), str (acurl)))
			out += ("\r\n [*] " + bl_getlang ("Proxy lookup quote") + ": %s") % (bl_getlang ("%s of %s") % (str (bl_stat ["lookup"]), str (bl_conf ["prox_quote"][0])))
			out += ("\r\n [*] " + bl_getlang ("Waiting feed list") + ": %s\r\n") % str (len (bl_feed))
			bl_reply (user, out)
			return 0

		if data [4:8] == "prox":
			if not bl_conf ["prox_lookup"][0]:
				bl_reply (user, bl_getlang ("Feature is disabled."))
				return 0

			size, out = 0, ""

			for pos in range (len (bl_prox)):
				for item in bl_prox [pos]:
					if item [3] < 3:
						size += 1
						out += (" [*] " + bl_getlang ("IP: %s.%s") + " | " + bl_getlang ("Status: %s") + " | " + bl_getlang ("Time: %s") + " | " + bl_getlang ("Chat: %s") + " | " + bl_getlang ("Users: %s") + "\r\n") % (item [0], vh.GetIPCC (item [0]) or "??", (bl_getlang ("Queued") if not item [3] else (bl_getlang ("Waiting") if item [3] == 1 else bl_getlang ("Done"))), time.strftime ("%H:%M:%S", time.localtime (item [4])), bl_getlang ("Yes") if item [5] else bl_getlang ("No"), (bl_getlang ("None") if item [3] == 2 else ", ".join (item [1])))

			if size:
				out = bl_getlang ("Waiting proxy lookups") + ":\r\n\r\n" + out
				out += ("\r\n " + bl_getlang ("Total: %s") + "\r\n") % str (size)
			else:
				out = bl_getlang ("Waiting proxy lookup list is empty.")

			bl_reply (user, out)
			return 0

		if data [4:11] == "feedall":
			if not bl_feed:
				out = bl_getlang ("Waiting feed list is empty.")
			else:
				out, mins = (bl_getlang ("Waiting feed list") + ":\r\n\r\n"), (bl_conf ["time_feed"][0] * 60)

				for item in bl_feed:
					out += (" [*] " + bl_getlang ("IP: %s.%s") + " | " + bl_getlang ("Expires: %s") + "\r\n") % (item [0], vh.GetIPCC (item [0]) or "??", time.strftime ("%d/%m %H:%M", time.localtime (item [1] + mins)))

				out += ("\r\n " + bl_getlang ("Total: %s") + "\r\n") % str (len (bl_feed))

			bl_reply (user, out)
			return 0

		if data [4:11] == "feeddel":
			if not bl_feed:
				bl_reply (user, bl_getlang ("Waiting feed list is empty."))
				return 0

			addr = data [12:]

			if not addr:
				del bl_feed [:]
				bl_reply (user, bl_getlang ("Waiting feed list has been cleared."))
				return 0

			if not bl_validaddr (addr):
				bl_reply (user, bl_getlang ("Bad command parameters: %s") % ("feeddel [" + bl_getlang ("addr") + "]"))
				return 0

			for id, item in enumerate (bl_feed):
				if item [0] == addr:
					bl_feed.pop (id)
					bl_reply (user, bl_getlang ("Waiting feed list item deleted: %s.%s") % (addr, vh.GetIPCC (addr) or "??"))
					return 0

			bl_reply (user, bl_getlang ("Waiting feed list out of item: %s.%s") % (addr, vh.GetIPCC (addr) or "??"))
			return 0

		if data [4:8] == "find":
			if not data [9:]:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("find <" + bl_getlang ("item") + ">"))
				return 0

			out, size = "", 0

			if bl_validaddr (data [9:]):
				intaddr = bl_addrtoint (data [9:])

				for item in bl_item [intaddr >> 24]:
					if intaddr >= item [0] and intaddr <= item [1]:
						out += " %s - %s : %s [%s]\r\n" % (bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2], bl_getlang ("Block") if item [3] else bl_getlang ("Notify"))
						size += 1

						if size >= bl_conf ["find_maxres"][0]:
							break

				if size < bl_conf ["find_maxres"][0] and bl_myli: # my list
					for item in bl_myli:
						if intaddr >= item [0] and intaddr <= item [1]:
							out += " %s - %s : %s [%s] [%s]\r\n" % (bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2], bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"), bl_getlang ("Enabled") if not item [3] else bl_getlang ("Disabled"))
							size += 1

							if size >= bl_conf ["find_maxres"][0]:
								break

				if size:
					bl_reply (user, (bl_getlang ("Results for IP: %s") + "\r\n\r\n%s") % (data [9:], out))
				else:
					bl_reply (user, bl_getlang ("No results for IP: %s") % data [9:])
			else:
				lowdata = data [9:].lower ()

				for pos in range (len (bl_item)):
					for item in bl_item [pos]:
						if lowdata in item [2].lower ():
							out += " %s - %s : %s [%s]\r\n" % (bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2], bl_getlang ("Block") if item [3] else bl_getlang ("Notify"))
							size += 1

							if size >= bl_conf ["find_maxres"][0]:
								break

					if size >= bl_conf ["find_maxres"][0]:
						break

				if size < bl_conf ["find_maxres"][0] and bl_myli: # my list
					for item in bl_myli:
						if lowdata in item [2].lower ():
							out += " %s - %s : %s [%s] [%s]\r\n" % (bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2], bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"), bl_getlang ("Enabled") if not item [3] else bl_getlang ("Disabled"))
							size += 1

							if size >= bl_conf ["find_maxres"][0]:
								break

				if size:
					bl_reply (user, (bl_getlang ("Results for title: %s") + "\r\n\r\n%s") % (data [9:], out))
				else:
					bl_reply (user, bl_getlang ("No results for title: %s") % data [9:])

			return 0

		if data [4:10] == "listre":
			out = bl_reload ()

			if out:
				out = bl_getlang ("Reload results") + ":\r\n\r\n" + out
			else:
				out = bl_getlang ("Blacklist list is empty.")

			bl_reply (user, out)
			return 0

		if data [4:7] == "del":
			pars = re.findall ("^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})[\\- ]*(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?$", data [8:])

			if not pars or not pars [0][0]:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("del <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "]"))
				return 0

			if not bl_validaddr (pars [0][0]):
				bl_reply (user, bl_getlang ("Lower IP not valid: %s") % pars [0][0])
				return 0

			if pars [0][1] and not bl_validaddr (pars [0][1]):
				bl_reply (user, bl_getlang ("Higher IP not valid: %s") % pars [0][1])
				return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])

			for pos in xrange (loaddr >> 24, (hiaddr >> 24) + 1):
				for id, item in enumerate (bl_item [pos]):
					if loaddr == item [0] and hiaddr == item [1]: # todo: exact match only for now
						bl_item [pos].pop (id)

						out = bl_getlang ("Item deleted from list") + ":\r\n"
						out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
						out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (pars [0][0], vh.GetIPCC (pars [0][0]) or "??")
						out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (pars [0][1] or pars [0][0], vh.GetIPCC (pars [0][1] or pars [0][0]) or "??")
						out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if item [3] else bl_getlang ("Notify"))

						bl_reply (user, out)
						return 0

			bl_reply (user, bl_getlang ("List out of item with range: %s - %s") % (pars [0][0], pars [0][1] or pars [0][0]))
			return 0

		if data [4:8] == "look":
			if not data [9:] or not bl_validaddr (data [9:]):
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("look <" + bl_getlang ("addr") + ">"))
				return 0

			code = vh.GetIPCC (data [9:])

			if not code:
				code = "??"

			if code == "L1" or code == "P1":
				bl_reply (user, bl_getlang ("Local or private IP specified: %s.%s") % (data [9:], code))
				return 0

			res = bl_httpreq (bl_defs ["ipintel"].decode ("hex") % (bl_conf ["prox_email"][0], data [9:]))

			if not res [0]:
				bl_reply (user, res [1])
				return 0

			res = bl_lookup (res [1])

			if res [0]:
				bl_reply (user, bl_getlang ("Public proxy detected: %s.%s") % (data [9:], vh.GetIPCC (data [9:]) or "??"))

				if bl_conf ["prox_getasn"][0]:
					bl_reply (user, bl_getlang ("ASN: %s") % bl_getasn (data [9:]))
			else:
				if str (res [1]).isdigit ():
					bl_reply (user, bl_getlang ("Not enough matches for %s.%s: %s of %s") % (data [9:], vh.GetIPCC (data [9:]) or "??", str (res [1]), str (bl_conf ["prox_match"][0])))
				else:
					bl_reply (user, res [1])

			return 0

		if data [4:11] == "listall":
			if not bl_list:
				out = bl_getlang ("Blacklist list is empty.")
			else:
				out = bl_getlang ("Blacklist list") + ":\r\n"

				for id, item in enumerate (bl_list):
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

			bl_reply (user, out)
			return 0

		if data [4:11] == "listadd":
			pars = re.findall ("^(\\S+)[ ]+(\\S+)[ ]+\"(.+)\"[ ]*(\\d+)?$", data [12:])

			if not pars or not pars [0][0] or not pars [0][1] or not pars [0][2]:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listadd <" + bl_getlang ("list") + "> <" + bl_getlang ("type") + "> <\"" + bl_getlang ("title") + "\"> [" + bl_getlang ("update") + "]"))
				return 0

			types = [
				"gzip-p2p",
				"gzip-emule",
				"gzip-range",
				"gzip-single",
				"zip-p2p",
				"zip-emule",
				"zip-range",
				"zip-single",
				"p2p",
				"emule",
				"range",
				"single"
			]

			if not pars [0][1] in types:
				bl_reply (user, bl_getlang ("Type must be one of: %s") % ", ".join (types))
				return 0

			update = 0

			if pars [0][3].isdigit ():
				update = int (pars [0][3])

			if update < 0 or update > 10800:
				bl_reply (user, bl_getlang ("Update must be in range: %s - %s") % (str (0), str (10800)))
				return 0

			for id, item in enumerate (bl_list):
				if item [0].lower () == pars [0][0].lower ():
					out = bl_getlang ("Item already in list") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

					bl_reply (user, out)
					return 0

			bl_list.append ([pars [0][0], pars [0][1], pars [0][2], update, 0, 1, 1, 0, time.time () if update else 0])
			vh.SQL ("insert into `py_bl_list` (`list`, `type`, `title`, `update`) values ('%s', '%s', '%s', %s)" % (bl_repsql (pars [0][0]), bl_repsql (pars [0][1]), bl_repsql (pars [0][2]), str (update)))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_list) - 1)
			out += ("\r\n [*] " + bl_getlang ("List: %s")) % pars [0][0]
			out += ("\r\n [*] " + bl_getlang ("Type: %s")) % pars [0][1]
			out += ("\r\n [*] " + bl_getlang ("Title: %s")) % pars [0][2]
			out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not update else (bl_getlang ("%s minute") + " | %s") % (str (update), time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (update * 60)))) if update == 1 else (bl_getlang ("%s minutes") + " | %s") % (str (update), time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (update * 60)))))
			out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
			out += ("\r\n [*] " + bl_getlang ("Action: %s")) % bl_getlang ("Block")
			out += ("\r\n [*] " + bl_getlang ("Except: %s")) % bl_getlang ("Yes")
			out += ("\r\n [*] " + bl_getlang ("Redirect: %s")) % bl_getlang ("No")
			out += ("\r\n [*] " + bl_getlang ("Status: %s") + "\r\n") % bl_import (pars [0][0], pars [0][1], pars [0][2], 1, 1, 0)

			bl_reply (user, out)
			return 0

		if data [4:11] == "listdel":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listdel <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list.pop (id)
				vh.SQL ("delete from `py_bl_list` where `list` = '%s'" % bl_repsql (item [0]))

				out = bl_getlang ("Item deleted from list") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
				out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
				out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
				out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
				out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else ((bl_getlang ("%s minute") % item [3]) if item [3] == 1 else (bl_getlang ("%s minutes") % item [3])))
				out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
				out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
				out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
				out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

				bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:11] == "listoff":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listoff <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if not item [4]:
					bl_list [id][4], bl_list [id][8] = 1, 0
					vh.SQL ("update `py_bl_list` set `off` = 1 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else ((bl_getlang ("%s minute") % item [3]) if item [3] == 1 else (bl_getlang ("%s minutes") % item [3])))
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("Yes")
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

					bl_reply (user, out)
				else:
					bl_list [id][4] = 0
					vh.SQL ("update `py_bl_list` set `off` = 0 where `list` = '%s'" % bl_repsql (item [0]))

					if item [3]:
						bl_list [id][8] = time.time ()

					out = bl_getlang ("Item now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))))
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s")) % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Status: %s") + "\r\n") % bl_import (item [0], item [1], item [2], item [5], item [6], item [7])

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:11] == "listact":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listact <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if item [5]:
					bl_list [id][5] = 0
					vh.SQL ("update `py_bl_list` set `action` = 0 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item now set to notify") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % bl_getlang ("Notify")
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

					bl_reply (user, out)
				else:
					bl_list [id][5] = 1
					vh.SQL ("update `py_bl_list` set `action` = 1 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item now set to block") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % bl_getlang ("Block")
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:10] == "listex":
			if data [11:].isdigit ():
				id = int (data [11:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listex <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if item [6]:
					bl_list [id][6] = 0
					vh.SQL ("update `py_bl_list` set `except` = 0 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item exception now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

					bl_reply (user, out)
				else:
					bl_list [id][6] = 1
					vh.SQL ("update `py_bl_list` set `except` = 1 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item exception now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % bl_getlang ("Yes")
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:11] == "listmov":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listmov <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if item [7]:
					bl_list [id][7] = 0
					vh.SQL ("update `py_bl_list` set `redirect` = 0 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item redirection now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % bl_getlang ("No")

					bl_reply (user, out)
				else:
					bl_list [id][7] = 1
					vh.SQL ("update `py_bl_list` set `redirect` = 1 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item redirection now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [8] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s") + "\r\n") % bl_getlang ("Yes")

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:11] == "listget":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("listget <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if not item [4]:
					if item [3]:
						bl_list [id][8] = time.time ()

					out = bl_getlang ("Item load result") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))))
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Except: %s")) % (bl_getlang ("No") if not item [6] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Redirect: %s")) % (bl_getlang ("No") if not item [7] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Status: %s") + "\r\n") % bl_import (item [0], item [1], item [2], item [5], item [6], item [7])

					bl_reply (user, out)
				else:
					bl_reply (user, bl_getlang ("Item is disabled: %s") % str (id))
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:9] == "myall":
			if not bl_myli:
				out = bl_getlang ("My list is empty.")
			else:
				out = bl_getlang ("My list") + ":\r\n"

				for id, item in enumerate (bl_myli):
					loaddr = bl_inttoaddr (item [0])
					hiaddr = bl_inttoaddr (item [1])

					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [3] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))

			bl_reply (user, out)
			return 0

		if data [4:9] == "myadd":
			pars = re.findall ("^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})[\\- ]*(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?[ ]*(.*)$", data [10:])

			if not pars or not pars [0][0]:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("myadd <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "] [" + bl_getlang ("title") + "]"))
				return 0

			if not bl_validaddr (pars [0][0]):
				bl_reply (user, bl_getlang ("Lower IP not valid: %s") % pars [0][0])
				return 0

			if pars [0][1] and not bl_validaddr (pars [0][1]):
				bl_reply (user, bl_getlang ("Higher IP not valid: %s") % pars [0][1])
				return 0

			for id, item in enumerate (bl_myli):
				if item [0] == bl_addrtoint (pars [0][0]) and item [1] == bl_addrtoint (pars [0][1] or pars [0][0]):
					out = bl_getlang ("Item already in list") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (pars [0][0], vh.GetIPCC (pars [0][0]) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (pars [0][1] or pars [0][0], vh.GetIPCC (pars [0][1] or pars [0][0]) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [3] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))

					bl_reply (user, out)
					return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])
			bl_myli.append ([loaddr, hiaddr, pars [0][2] or bl_getlang ("My item"), 0])
			vh.SQL ("insert ignore into `py_bl_myli` (`loaddr`, `hiaddr`, `title`) values (%s, %s, %s)" % (str (loaddr), str (hiaddr), ("'" + bl_repsql (pars [0][2]) + "'" if pars [0][2] else "null")))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_myli) - 1)
			out += ("\r\n [*] " + bl_getlang ("Title: %s")) % (pars [0][2] or bl_getlang ("My item"))
			out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (pars [0][0], vh.GetIPCC (pars [0][0]) or "??")
			out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (pars [0][1] or pars [0][0], vh.GetIPCC (pars [0][1] or pars [0][0]) or "??")
			out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
			out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))

			bl_reply (user, out)
			return 0

		if data [4:9] == "myoff":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("myoff <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_myli and len (bl_myli) - 1 >= id:
				item = bl_myli [id]
				loaddr, hiaddr = bl_inttoaddr (item [0]), bl_inttoaddr (item [1])

				if not item [3]:
					bl_myli [id][3] = 1
					vh.SQL ("update `py_bl_myli` set `off` = 1 where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

					out = bl_getlang ("Item now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("Yes")
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))

					bl_reply (user, out)
				else:
					bl_myli [id][3] = 0
					vh.SQL ("update `py_bl_myli` set `off` = 0 where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

					out = bl_getlang ("Item now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:9] == "mydel":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("mydel <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_myli and len (bl_myli) - 1 >= id:
				item = bl_myli.pop (id)
				vh.SQL ("delete from `py_bl_myli` where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))
				loaddr = bl_inttoaddr (item [0])
				hiaddr = bl_inttoaddr (item [1])

				out = bl_getlang ("Item deleted from list") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
				out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
				out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
				out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
				out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [3] else bl_getlang ("Yes"))
				out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))

				bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:10] == "asnall":
			if not bl_asn:
				out = bl_getlang ("ASN list is empty.")
			else:
				out = bl_getlang ("ASN list") + ":\r\n"

				for id, item in enumerate (bl_asn):
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("ASN: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [1] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_asnlist"][0] else bl_getlang ("Notify"))

			bl_reply (user, out)
			return 0

		if data [4:10] == "asnadd":
			asn = data [11:]

			if not asn:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("asnadd <" + bl_getlang ("asn") + ">"))
				return 0

			for id, item in enumerate (bl_asn):
				if item [0] == asn:
					out = bl_getlang ("Item already in list") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("ASN: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [1] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_asnlist"][0] else bl_getlang ("Notify"))

					bl_reply (user, out)
					return 0

			bl_asn.append ([asn, 0])
			vh.SQL ("insert ignore into `py_bl_asn` (`asn`) values ('%s')" % bl_repsql (asn))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_asn) - 1)
			out += ("\r\n [*] " + bl_getlang ("ASN: %s")) % asn
			out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
			out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_asnlist"][0] else bl_getlang ("Notify"))

			bl_reply (user, out)
			return 0

		if data [4:10] == "asnoff":
			if data [11:].isdigit ():
				id = int (data [11:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("asnoff <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_asn and len (bl_asn) - 1 >= id:
				item = bl_asn [id]

				if not item [1]:
					bl_asn [id][1] = 1
					vh.SQL ("update `py_bl_asn` set `off` = 1 where `asn` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("ASN: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("Yes")
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_asnlist"][0] else bl_getlang ("Notify"))

					bl_reply (user, out)
				else:
					bl_asn [id][1] = 0
					vh.SQL ("update `py_bl_asn` set `off` = 0 where `asn` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("ASN: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_asnlist"][0] else bl_getlang ("Notify"))

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:10] == "asndel":
			if data [11:].isdigit ():
				id = int (data [11:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("asndel <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_asn and len (bl_asn) - 1 >= id:
				item = bl_asn.pop (id)
				vh.SQL ("delete from `py_bl_asn` where `asn` = '%s'" % bl_repsql (item [0]))

				out = bl_getlang ("Item deleted from list") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
				out += ("\r\n [*] " + bl_getlang ("ASN: %s")) % item [0]
				out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [1] else bl_getlang ("Yes"))
				out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_asnlist"][0] else bl_getlang ("Notify"))

				bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:10] == "asntry":
			asn = data [11:]

			if not asn:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("asntry <" + bl_getlang ("asn") + ">"))
				return 0

			if not bl_asn:
				bl_reply (user, bl_getlang ("ASN list is empty."))
				return 0

			lowasn, out, size = asn.lower (), "", 0

			for id, item in enumerate (bl_asn):
				if item [0].lower () in lowasn:
					out += " %s. %s [%s]\r\n" % (str (id), item [0], bl_getlang ("Enabled") if not item [1] else bl_getlang ("Disabled"))
					size += 1

					if size >= bl_conf ["find_maxres"][0]:
						break

			if size:
				bl_reply (user, (bl_getlang ("Results for ASN: %s") + "\r\n\r\n%s") % (asn, out))
			else:
				bl_reply (user, bl_getlang ("No results for ASN: %s") % asn)

			return 0

		if data [4:9] == "exall":
			if not bl_exli:
				out = bl_getlang ("Exception list is empty.")
			else:
				out = bl_getlang ("Exception list") + ":\r\n"

				for id, item in enumerate (bl_exli):
					loaddr = bl_inttoaddr (item [0])
					hiaddr = bl_inttoaddr (item [1])

					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s") + "\r\n") % (bl_getlang ("No") if not item [3] else bl_getlang ("Yes"))

			bl_reply (user, out)
			return 0

		if data [4:9] == "exadd":
			pars = re.findall ("^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})[\\- ]*(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?[ ]*(.*)$", data [10:])

			if not pars or not pars [0][0]:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("exadd <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "] [" + bl_getlang ("title") + "]"))
				return 0

			if not bl_validaddr (pars [0][0]):
				bl_reply (user, bl_getlang ("Lower IP not valid: %s") % pars [0][0])
				return 0

			if pars [0][1] and not bl_validaddr (pars [0][1]):
				bl_reply (user, bl_getlang ("Higher IP not valid: %s") % pars [0][1])
				return 0

			for id, item in enumerate (bl_exli):
				if item [0] == bl_addrtoint (pars [0][0]) and item [1] == bl_addrtoint (pars [0][1] or pars [0][0]):
					out = bl_getlang ("Item already in list") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (pars [0][0], vh.GetIPCC (pars [0][0]) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (pars [0][1] or pars [0][0], vh.GetIPCC (pars [0][1] or pars [0][0]) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s") + "\r\n") % (bl_getlang ("No") if not item [3] else bl_getlang ("Yes"))

					bl_reply (user, out)
					return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])
			bl_exli.append ([loaddr, hiaddr, pars [0][2] or bl_getlang ("Exception"), 0])
			vh.SQL ("insert ignore into `py_bl_exli` (`loaddr`, `hiaddr`, `title`) values (%s, %s, %s)" % (str (loaddr), str (hiaddr), ("'" + bl_repsql (pars [0][2]) + "'" if pars [0][2] else "null")))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_exli) - 1)
			out += ("\r\n [*] " + bl_getlang ("Title: %s")) % (pars [0][2] or bl_getlang ("Exception"))
			out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (pars [0][0], vh.GetIPCC (pars [0][0]) or "??")
			out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (pars [0][1] or pars [0][0], vh.GetIPCC (pars [0][1] or pars [0][0]) or "??")
			out += ("\r\n [*] " + bl_getlang ("Disabled: %s") + "\r\n") % bl_getlang ("No")

			bl_reply (user, out)
			return 0

		if data [4:9] == "exoff":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("exoff <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_exli and len (bl_exli) - 1 >= id:
				item = bl_exli [id]
				loaddr, hiaddr = bl_inttoaddr (item [0]), bl_inttoaddr (item [1])

				if not item [3]:
					bl_exli [id][3] = 1
					vh.SQL ("update `py_bl_exli` set `off` = 1 where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

					out = bl_getlang ("Item now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s") + "\r\n") % bl_getlang ("Yes")

					bl_reply (user, out)
				else:
					bl_exli [id][3] = 0
					vh.SQL ("update `py_bl_exli` set `off` = 0 where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

					out = bl_getlang ("Item now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s") + "\r\n") % bl_getlang ("No")

					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:9] == "exdel":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("exdel <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_exli and len (bl_exli) - 1 >= id:
				item, stop = bl_exli.pop (id), False
				vh.SQL ("delete from `py_bl_exli` where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

				for pos in range (len (bl_prox)):
					for pid, prox in enumerate (bl_prox [pos]):
						intaddr = bl_addrtoint (prox [0])

						if intaddr >= item [0] and intaddr <= item [1]:
							if prox [3] == 4:
								bl_item [intaddr >> 24].append ([intaddr, intaddr, bl_getlang ("Public proxy"), bl_conf ["action_proxy"][0], bl_conf ["except_proxy"][0], len (bl_conf ["redir_prox"][0])]) # todo: also add to mysql table when we have one
								bl_prox [pos].pop (pid)

							stop = True
							break

					if stop:
						break

				loaddr = bl_inttoaddr (item [0])
				hiaddr = bl_inttoaddr (item [1])

				out = bl_getlang ("Item deleted from list") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
				out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
				out += ("\r\n [*] " + bl_getlang ("Lower IP: %s.%s")) % (loaddr, vh.GetIPCC (loaddr) or "??")
				out += ("\r\n [*] " + bl_getlang ("Higher IP: %s.%s")) % (hiaddr, vh.GetIPCC (hiaddr) or "??")
				out += ("\r\n [*] " + bl_getlang ("Disabled: %s") + "\r\n") % (bl_getlang ("No") if not item [3] else bl_getlang ("Yes"))

				bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:9] == "extry":
			if not data [10:] or not bl_validaddr (data [10:]):
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("extry <" + bl_getlang ("addr") + ">"))
				return 0

			out, size = "", 0
			intaddr = bl_addrtoint (data [10:])

			for id, item in enumerate (bl_exli):
				if intaddr >= item [0] and intaddr <= item [1]:
					out += " %s. %s - %s : %s [%s]\r\n" % (str (id), bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2], bl_getlang ("Enabled") if not item [3] else bl_getlang ("Disabled"))
					size += 1

					if size >= bl_conf ["find_maxres"][0]:
						break

			if size:
				bl_reply (user, (bl_getlang ("Results for IP: %s") + "\r\n\r\n%s") % (data [10:], out))
			else:
				bl_reply (user, bl_getlang ("No results for IP: %s") % data [10:])

			return 0

		if data [4:8] == "conf":
			out = bl_getlang ("Configuration list") + ":\r\n"

			for name, item in sorted (bl_conf.iteritems ()):
				out += ("\r\n [*] " + bl_getlang ("Name: %s")) % name
				out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
				out += ("\r\n [*] " + bl_getlang ("Range: %s - %s")) % (item [2], item [3])
				out += ("\r\n [*] " + bl_getlang ("Value: %s")) % item [0]
				out += ("\r\n [*] " + bl_getlang ("Explanation: %s") + "\r\n") % bl_getlang (item [4])

			bl_reply (user, out)
			return 0

		if data [4:7] == "set":
			pars = re.findall ("^(\\S+)[ ]*(.*)$", data [8:])

			if pars and pars [0][0]:
				out = bl_getlang ("Item configuration") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("Name: %s")) % pars [0][0]
				out += ("\r\n [*] " + bl_getlang ("Type: %s")) % (bl_conf [pars [0][0]][1] if pars [0][0] in bl_conf else bl_getlang ("None"))
				out += ("\r\n [*] " + bl_getlang ("Range: %s - %s")) % ((bl_conf [pars [0][0]][2] if pars [0][0] in bl_conf else 0), (bl_conf [pars [0][0]][3] if pars [0][0] in bl_conf else 0))
				out += ("\r\n [*] " + bl_getlang ("Old value: %s")) % (bl_getlang ("None") if bl_getconf (pars [0][0]) == None else bl_getconf (pars [0][0]))
				out += ("\r\n [*] " + bl_getlang ("New value: %s")) % pars [0][1]
				out += ("\r\n [*] " + bl_getlang ("Status: %s")) % bl_setconf (pars [0][0], pars [0][1])
				out += ("\r\n [*] " + bl_getlang ("Explanation: %s") + "\r\n") % (bl_getlang (bl_conf [pars [0][0]][4]) if pars [0][0] in bl_conf else bl_getlang ("Item not found"))
			else:
				out = bl_getlang ("Missing command parameters: %s") % ("set <" + bl_getlang ("item") + "> [" + bl_getlang ("value") + "]")

			bl_reply (user, out)
			return 0

		if data [4:7] == "ver":
			ver = bl_httpreq (bl_defs ["verfile"].decode ("hex"))

			if not ver [0]:
				bl_reply (user, bl_getlang ("Unable to download version file: %s") % ver [1])
				return 0

			new, old = ver [1].replace (".", ""), bl_defs ["version"].replace (".", "")

			if not new.isdigit () or not old.isdigit ():
				bl_reply (user, bl_getlang ("Unable to download version file: %s") % bl_getlang ("Invalid version number"))
				return 0

			if int (new) <= int (old):
				bl_reply (user, bl_getlang ("You are already running latest version: %s") % bl_defs ["version"])
				return 0

			bl_reply (user, bl_getlang ("New version is available for download: %s") % ver [1])
			res = bl_httpreq (bl_defs ["pyfile"].decode ("hex"))

			if not res [0]:
				bl_reply (user, bl_getlang ("Unable to download script file: %s") % res [1])
				return 0

			if not ("# Blacklist %s" % ver [1]) in res [1]:
				bl_reply (user, bl_getlang ("Unable to download script file: %s") % bl_getlang ("Invalid file content"))
				return 0

			temp, file = os.path.join (vh.basedir, "blacklist.temp"), None

			try:
				file = open (temp, "wb")
			except:
				pass

			if not file:
				bl_reply (user, bl_getlang ("Unable to update script file: %s") % bl_getlang ("Failed to write temporary file"))
				return 0

			file.write (res [1])
			file.close ()
			name = os.path.join (vh.basedir, "scripts", "blacklist.py")

			if os.path.isfile (name):
				bl_remfile (name)

			os.rename (temp, name)

			if not os.path.isfile (name):
				bl_reply (user, bl_getlang ("Unable to update script file: %s") % bl_getlang ("Failed to move file"))
				return 0

			if bl_conf ["lang_pref"][0] and bl_conf ["lang_pref"][0] != "en":
				res = bl_httpreq (bl_defs ["langfile"].decode ("hex") % bl_conf ["lang_pref"][0])

				if res [0]:
					if ("# Version: %s" % ver [1][:-2]) in res [1]:
						temp, file = os.path.join (vh.basedir, "black_%s.temp" % bl_conf ["lang_pref"][0]), None

						try:
							file = open (temp, "wb")
						except:
							pass

						if file:
							file.write (res [1])
							file.close ()
							name = os.path.join (vh.basedir, "scripts", "black_%s.lang" % bl_conf ["lang_pref"][0])

							if os.path.isfile (name):
								bl_remfile (name)

							os.rename (temp, name)

							if not os.path.isfile (name):
								bl_reply (user, bl_getlang ("Unable to update translation file: %s") % bl_getlang ("Failed to move file"))
						else:
							bl_reply (user, bl_getlang ("Unable to update translation file: %s") % bl_getlang ("Failed to write temporary file"))
					else:
						bl_reply (user, bl_getlang ("Unable to download translation file: %s") % bl_getlang ("Invalid file content"))
				else:
					bl_reply (user, bl_getlang ("Unable to download translation file: %s") % res [1])

			bl_reply (user, bl_getlang ("Finish update with following command: %s") % "!pyreload blacklist.py")
			return 0

		out = bl_getlang ("Blacklist usage") + ":\r\n\r\n"

		out += " stat\t\t\t\t\t- " + bl_getlang ("Script statistics") + "\r\n"
		out += " prox\t\t\t\t\t- " + bl_getlang ("Show waiting proxy lookups") + "\r\n\r\n"

		out += " feedall\t\t\t\t\t- " + bl_getlang ("Show waiting feed list") + "\r\n"
		out += " feeddel [" + bl_getlang ("addr") + "]\t\t\t\t- " + bl_getlang ("Delete from waiting feed list") + "\r\n\r\n"

		out += " find <" + bl_getlang ("item") + ">\t\t\t\t- " + bl_getlang ("Search in loaded lists") + "\r\n"
		out += " del <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "]\t\t\t- " + bl_getlang ("Delete blacklisted item") + "\r\n\r\n"

		out += " look <" + bl_getlang ("addr") + ">\t\t\t\t- " + bl_getlang ("Public proxy lookup") + "\r\n\r\n"

		out += " listall\t\t\t\t\t- " + bl_getlang ("Show all lists") + "\r\n"
		out += " listadd <" + bl_getlang ("list") + "> <" + bl_getlang ("type") + "> <\"" + bl_getlang ("title") + "\"> [" + bl_getlang ("update") + "]\t- " + bl_getlang ("Load new list") + "\r\n"
		out += " listoff <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Disable or enable list") + "\r\n"
		out += " listact <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Set list block action") + "\r\n"
		out += " listex <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Set list exception usage") + "\r\n"
		out += " listmov <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Set list redirection usage") + "\r\n"
		out += " listget <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Force load of existing list") + "\r\n"
		out += " listdel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete existing list") + "\r\n"
		out += " listre\t\t\t\t\t- " + bl_getlang ("Reload all lists") + "\r\n\r\n"

		out += " myall\t\t\t\t\t- " + bl_getlang ("Show my list") + "\r\n"
		out += " myadd <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "] [" + bl_getlang ("title") + "]\t\t- " + bl_getlang ("New my item") + "\r\n"
		out += " myoff <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Disable or enable item") + "\r\n"
		out += " mydel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete my item") + "\r\n\r\n"

		out += " asnall\t\t\t\t\t- " + bl_getlang ("Show ASN list") + "\r\n"
		out += " asnadd <" + bl_getlang ("asn") + ">\t\t\t\t- " + bl_getlang ("New ASN item") + "\r\n"
		out += " asnoff <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Disable or enable item") + "\r\n"
		out += " asndel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete ASN item") + "\r\n"
		out += " asntry <" + bl_getlang ("asn") + ">\t\t\t\t- " + bl_getlang ("Search in ASN list") + "\r\n\r\n"

		out += " exall\t\t\t\t\t- " + bl_getlang ("Show exception list") + "\r\n"
		out += " exadd <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "] [" + bl_getlang ("title") + "]\t\t\t- " + bl_getlang ("New exception item") + "\r\n"
		out += " exoff <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Disable or enable item") + "\r\n"
		out += " exdel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete an exception") + "\r\n"
		out += " extry <" + bl_getlang ("addr") + ">\t\t\t\t- " + bl_getlang ("Search in exceptions") + "\r\n\r\n"

		out += " conf\t\t\t\t\t- " + bl_getlang ("Show current configuration") + "\r\n"
		out += " set <" + bl_getlang ("item") + "> [" + bl_getlang ("value") + "]\t\t\t\t- " + bl_getlang ("Set configuration item") + "\r\n\r\n"

		out += " ver\t\t\t\t\t- " + bl_getlang ("Update script to latest version") + "\r\n"

		bl_reply (user, out)
		return 0

	return 1

def OnTimer (msec):
	global bl_defs, bl_conf, bl_stat, bl_list, bl_item, bl_prox, bl_feed
	now = time.time ()

	if now - bl_stat ["update"] >= bl_defs ["timersec"]:
		bl_stat ["update"], mins = now, (bl_conf ["time_feed"][0] * 60)
		bl_feed = [item for item in bl_feed if now - item [1] < mins]

		for id, item in enumerate (bl_list):
			if not item [4] and item [3] and now - item [8] >= item [3] * 60:
				bl_list [id][8], out = now, bl_import (item [0], item [1], item [2], item [5], item [6], item [7], True)

				if bl_conf ["notify_update"][0]:
					bl_notify ("%s: %s" % (item [2], out))

	if bl_conf ["prox_lookup"][0] and now - bl_stat ["proxy"] >= bl_conf ["prox_timer"][0]:
		bl_stat ["proxy"], start, dels = now, 0, []

		for pos in range (len (bl_prox)):
			for id, item in enumerate (bl_prox [pos]):
				if not item [3]:
					if start < bl_conf ["prox_maxreq"][0]:
						start += 1

						try:
							os.system (bl_defs ["curlreq"].decode ("hex") % (str (1), str (1), str (bl_conf ["time_down"][0]), str (bl_conf ["time_down"][0] * 2), bl_useragent (True), "", os.path.join (bl_defs ["datadir"], item [0]), (bl_defs ["ipintel"].decode ("hex") % (bl_conf ["prox_email"][0], item [0])))) # bl_defs ["referer"].decode ("hex")
							bl_prox [pos][id][3], bl_prox [pos][id][4] = 1, now

						except:
							bl_delaychat (item [2]) # delayed messages
							bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], vh.GetIPCC (item [0]) or "??", bl_getlang ("Failed to execute command")))
							dels.insert (0, [pos, id])

				elif item [3] == 1:
					name = os.path.join (bl_defs ["datadir"], item [0])
					isfile = os.path.isfile (name)

					if isfile:
						size = 0

						try:
							size = os.path.getsize (name)
						except:
							pass

						if size:
							file = None

							try:
								file = open (name, "r")
							except:
								pass

							keep = False
							code = vh.GetIPCC (item [0])

							if not code:
								code = "??"

							if file:
								data = None

								try:
									data = file.read ()
								except:
									pass

								file.close ()

								if data:
									res = bl_lookup (data)

									if res [0]:
										bl_notify (bl_getlang ("Public proxy detected: %s.%s") % (item [0], code)) # todo: must be controlled by bl_waitfeed

										if bl_conf ["prox_getasn"][0]:
											bl_notify (bl_getlang ("ASN: %s") % bl_getasn (item [0]))

										intaddr = bl_addrtoint (item [0])
										keep = True

										if bl_conf ["action_proxy"][0] == 0: # notify only mode
											if bl_waitfeed (item [0]):
												if item [5]:
													bl_notify (bl_getlang ("Notifying blacklisted chat from %s with IP %s.%s: %s") % (item [1][0] if len (item [1]) == 1 else ", ".join (item [1]), item [0], code, bl_getlang ("Public proxy")))
												else:
													bl_notify (bl_getlang ("Notifying blacklisted login from %s with IP %s.%s: %s") % (item [1][0] if len (item [1]) == 1 else ", ".join (item [1]), item [0], code, bl_getlang ("Public proxy")))

											# todo: bl_extry if ever required
											bl_stat ["notify"] += 1
											bl_prox [pos][id][3] = 4

										elif bl_excheck (item [0], intaddr, code, None, None, bl_getlang ("Public proxy"), bl_conf ["except_proxy"][0], item [1][0] if len (item [1]) == 1 else ", ".join (item [1]), item [5]): # exception
											bl_delaychat (item [2]) # delayed messages
											bl_stat ["except"] += len (item [1])
											bl_prox [pos][id][3] = 4

										elif bl_conf ["action_proxy"][0] == 1: # drop user mode
											for nick in item [1]:
												vh.CloseConnection (nick)

											bl_stat ["block"] += len (item [1])
											bl_prox [pos][id][3] = 2
											bl_item [intaddr >> 24].append ([intaddr, intaddr, bl_getlang ("Public proxy"), bl_conf ["action_proxy"][0], bl_conf ["except_proxy"][0], len (bl_conf ["redir_prox"][0])]) # todo: also add to mysql table when we have one

										elif bl_conf ["action_proxy"][0] == 2: # block chat mode
											bl_delaychat (item [2], True) # delayed messages
											bl_stat ["block"] += len (item [2])
											bl_prox [pos][id][3] = 3

									else:
										if str (res [1]).isdigit ():
											keep = True
											bl_prox [pos][id][3] = 4

											if (bl_conf ["prox_debug"][0] and int (res [1])) or bl_conf ["prox_debug"][0] > 1:
												bl_notify (bl_getlang ("Not enough matches for %s.%s: %s of %s") % (item [0], code, str (res [1]), str (bl_conf ["prox_match"][0])))

										elif not bl_conf ["prox_nofail"][0]:
											bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], code, res [1]))

										bl_delaychat (item [2]) # delayed messages
								else:
									bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], code, bl_getlang ("Failed to read data")))
									bl_delaychat (item [2]) # delayed messages

							else:
								bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], code, bl_getlang ("Failed to open file")))
								bl_delaychat (item [2]) # delayed messages

							if keep:
								del bl_prox [pos][id][1][:]
								del bl_prox [pos][id][2][:]
								bl_prox [pos][id][4] = now
							else:
								dels.insert (0, [pos, id])

							bl_remfile (name)
							continue

					if now - item [4] >= (bl_conf ["time_down"][0] * 2) + (bl_conf ["prox_timer"][0] * 2):
						dels.insert (0, [pos, id])

						if isfile:
							bl_remfile (name)

				elif item [3] == 2:
					if now - item [4] >= bl_defs ["delwait"]:
						dels.insert (0, [pos, id])

				#elif item [3] == 3: # block chat mode
					#pass

				#elif item [3] == 4: # exception
					#pass

		for item in dels:
			bl_prox [item [0]].pop (item [1])

bl_main ()

# end of file