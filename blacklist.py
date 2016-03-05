# coding: latin-1

# Blacklist 1.2.0.3
# © 2010-2016 RoLex
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
# 1.1.8.0 - Fixed missing global variable declarations
# -------
# 1.2.0.0 - Added bypass of public proxy lookup for local and private IP addresses
# 1.2.0.0 - Added four digit version numbering
# -------
# 1.2.0.2 - Fixed wrong UTC time use instead of local time
# 1.2.0.3 - Fixed login notification for slow connections
# 1.2.0.1 - Added "listact" command to set list block action
# 1.2.0.1 - Added "action_proxy" configuration to set public proxy detection block action
# 1.2.0.1 - Added "action_mylist" configuration to set my list item detection block action
# -------

import vh, re, urllib2, urlparse, gzip, zipfile, StringIO, time, os, subprocess, socket, struct, operator, random, json, ConfigParser

bl_defs = {
	"version": "1.2.0.3", # todo: dont forget to update
	"curlver": ["curl", "-V"],
	"curlreq": "curl -G -L --max-redirs %s --retry %s --connect-timeout %s -m %s --interface %s -A \"%s\" -e \"%s\" -s -o \"%s\" \"%s\" &",
	"google": "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&userip=%s&rsz=8&q=proxy%%20OR%%20socks%%20%%22%s%%3a1..65535%%22",
	"userip": "http://www.te-home.net/?do=tools&action=whatismyip",
	"referer": ["https://github.com/verlihub/python/", []],
	"useragent": ["Blacklist/%s", None],
	"datadir": os.path.join (vh.basedir, "blackdata"),
	"timersec": 60,
	"delwait": 60,
	"prevfeed": 60
}

bl_lang = {
	0: "Blacklist %s startup",
	1: "Exception",
	2: "Failed with HTTP error",
	3: "Failed with URL error",
	4: "Failed with unknown error",
	5: "Failed to compile pattern",
	6: "File is not compressed with GZIP",
	7: "Failed to read data",
	8: "%s items loaded",
	9: "Unknown list type",
	10: "Failed to open file",
	11: "My list",
	12: "Value too low",
	13: "Value too high",
	14: "Value is not a number",
	15: "Value too short",
	16: "Value too long",
	17: "Item not found",
	18: "Blacklisted connection exception from %s.%s: %s",
	19: "Blocking blacklisted connection from %s.%s: %s",
	20: "You don't have access to this command.",
	21: "Blacklist statistics",
	22: "Version: %s",
	23: "Loaded lists: %s",
	24: "Blacklisted items: %s",
	25: "Excepted items: %s",
	26: "Blocked connections: %s",
	27: "Excepted connections: %s",
	28: "Total connections: %s",
	29: "Missing command parameters: %s",
	30: "Results for IP: %s",
	31: "No results for IP: %s",
	32: "Results for title: %s",
	33: "No results for title: %s",
	34: "Blacklist list is empty.",
	35: "Blacklist list",
	36: "ID: %s",
	37: "List: %s",
	38: "Type: %s",
	39: "Title: %s",
	40: "Update: %s",
	41: "On load",
	42: "%s minute",
	43: "%s minutes",
	44: "Disabled: %s",
	45: "No",
	46: "Yes",
	47: "Type must be one of: %s",
	48: "Update must be in range: %s - %s",
	49: "Item already in list",
	50: "Item added to list",
	51: "Status: %s",
	52: "Item deleted from list",
	53: "List out of item with ID: %s",
	54: "Item now disabled",
	55: "Item now enabled",
	56: "Exception list is empty.",
	57: "Exception list",
	58: "Lower IP: %s",
	59: "Higher IP: %s",
	60: "Lower IP not valid: %s",
	61: "Higher IP not valid: %s",
	62: "Configuration list",
	63: "Name: %s",
	64: "Range: %s - %s",
	65: "Value: %s",
	66: "Item configuration",
	67: "Old value: %s",
	68: "New value: %s",
	69: "Waiting feed list is empty.",
	70: "Waiting feed list",
	71: "IP: %s.%s",
	72: "Expires: %s",
	73: "Blacklist usage",
	74: "Script statistics",
	75: "Search in loaded lists",
	76: "Show all lists",
	77: "Load new list",
	78: "Disable or enable list",
	79: "Delete existing list",
	80: "Show exception list",
	81: "New exception item",
	82: "Delete an exception",
	83: "Show current configuration",
	84: "Set configuration item",
	85: "Show waiting feed list",
	86: "value",
	87: "item",
	88: "id",
	89: "addr",
	90: "range",
	91: "title",
	92: "list",
	93: "type",
	94: "update",
	95: "None",
	96: "Set translation string",
	97: "Show current translation",
	98: "Translation list",
	99: "Updated translation with ID: %s",
	100: "Parameter count mismatch in translation with ID: %s",
	101: "File is not compressed with ZIP",
	102: "Force load of existing list",
	103: "Item is disabled",
	104: "Item load result",
	105: "Failed to load JSON",
	106: "Failed to parse JSON",
	107: "Failed to get status",
	108: "Unexpected status: %s",
	109: "Failed to get results",
	110: "Failed to open URL",
	111: "Failed to get search data",
	112: "Failed to read INI",
	113: "Failed to create file",
	114: "Failed to get IP",
	115: "User IP: %s",
	116: "Public proxy lookup",
	117: "Missing user IP.",
	118: "Not enough matches for %s.%s: %s of %s",
	119: "Public proxy detected: %s:%s.%s",
	120: "Failed proxy detection for %s.%s: %s",
	121: "Delete blacklisted item",
	122: "List out of item with range: %s - %s",
	123: "Data directory: %s",
	124: "Failed to create directory",
	125: "Failed to execute command",
	126: "Public proxy",
	127: "Show waiting proxy lookups",
	128: "Waiting proxy lookup list is empty.",
	129: "Waiting proxy lookups",
	130: "Time: %s",
	131: "Users: %s",
	132: "Feature is disabled.",
	133: "Total: %s",
	134: "Queued",
	135: "Waiting",
	136: "Failed to get version",
	137: "%s version: %s",
	138: "%s of %s",
	139: "Done",
	140: "My list is empty.",
	141: "Reload all lists",
	142: "My item",
	143: "Reload results",
	144: "Show my list",
	145: "New my item",
	146: "Delete my item",
	147: "My items: %s",
	148: "Excepted country",
	149: "Blocked country",
	150: "User nick to receive all feed messages",
	151: "Space separated country codes to block",
	152: "Space separated country codes to except",
	153: "Minimal class to receive feed messages",
	154: "Minimal class to access script commands",
	155: "Minimal class to skip public proxy lookup",
	156: "Minutes to delay same IP notifications",
	157: "Download operation timeout in seconds",
	158: "Enable blacklist list update notification",
	159: "Maximum number of blacklist search results",
	160: "Enable public proxy lookup on user login",
	161: "Own IP required for public proxy lookup",
	162: "Minimal number of public proxy matches",
	163: "Minutes to wait after hub is started",
	164: "Seconds to process proxy lookup queue",
	165: "Maximum number of proxy lookups to enqueue",
	166: "Maximum number of proxy lookups to send",
	167: "Explanation: %s",
	168: "Disable proxy lookup failure notifications",
	169: "Level of proxy lookup debug information",
	170: "User agent: %s",
	171: "New referer: %s",
	172: "Set list block action",
	173: "Item now set to block",
	174: "Item now set to notify",
	175: "Action: %s",
	176: "Block",
	177: "Notify",
	178: "Blocking blacklisted login from %s with IP %s.%s: %s",
	179: "Notifying blacklisted connection from %s.%s: %s",
	180: "Notifying blacklisted login from %s with IP %s.%s: %s",
	181: "Block action on public proxy detections",
	182: "Block action on my list item detections",
	183: "Notified connections: %s"
}

bl_conf = {
	"nick_feed": ["", "str", 0, 255, "User nick to receive all feed messages"],
	"code_block": ["", "str", 0, 255, "Space separated country codes to block"],
	"code_except": ["", "str", 0, 255, "Space separated country codes to except"],
	"class_feed": [5, "int", 0, 11, "Minimal class to receive feed messages"],
	"class_conf": [10, "int", 3, 11, "Minimal class to access script commands"],
	"class_skip": [3, "int", 0, 11, "Minimal class to skip public proxy lookup"],
	"time_feed": [60, "int", 0, 1440, "Minutes to delay same IP notifications"],
	"time_down": [5, "int", 1, 300, "Download operation timeout in seconds"],
	"notify_update": [1, "int", 0, 1, "Enable blacklist list update notification"],
	"find_maxres": [1000, "int", 1, 10000, "Maximum number of blacklist search results"],
	"prox_lookup": [0, "int", 0, 1, "Enable public proxy lookup on user login"],
	"prox_userip": ["", "str", 0, 15, "Own IP required for public proxy lookup"],
	"prox_match": [3, "int", 1, 8, "Minimal number of public proxy matches"],
	"prox_start": [5, "int", 0, 30, "Minutes to wait after hub is started"],
	"prox_timer": [3, "int", 1, 300, "Seconds to process proxy lookup queue"],
	"prox_queue": [100, "int", 1, 10000, "Maximum number of proxy lookups to enqueue"],
	"prox_maxreq": [1, "int", 1, 100, "Maximum number of proxy lookups to send"],
	"prox_nofail": [0, "int", 0, 1, "Disable proxy lookup failure notifications"],
	"prox_debug": [0, "int", 0, 2, "Level of proxy lookup debug information"],
	"action_proxy": [1, "int", 0, 1, "Block action on public proxy detections"],
	"action_mylist": [1, "int", 0, 1, "Block action on my list item detections"]
}

bl_stat = {
	"connect": 0l,
	"block": 0l,
	"notify": 0l,
	"except": 0l,
	"update": time.time (),
	"proxy": time.time ()
}

bl_list = [
	#["http://list.iblocklist.com/?list=ijfqtofzixtwayqovmxn&fileformat=p2p&archiveformat=gz", "gzip-p2p", "TBG - Primary", 0, 0, 1, 0],
	#["http://list.iblocklist.com/?list=xoebmbyexwuiogmbyprb&fileformat=p2p&archiveformat=gz", "gzip-p2p", "Bluetack - Proxy", 0, 0, 1, 0],
	#["http://te-home.net/blacklist.php?do=load&list=AP2P", "p2p", "TE - AP2P", 0, 0, 1, 0],
	#["http://te-home.net/blacklist.php?do=load&list=Proxy", "p2p", "TE - Proxy", 0, 0, 1, 0],
	#["http://ledo.feardc.net/mirror/torexit.list", "single", "Tor exit", 60, 0, 1, 0],
	#["http://ledo.feardc.net/mirror/torserver.list", "single", "Tor server", 60, 0, 1, 0]
]

bl_item = []
bl_prox = [[] for pos in xrange (256)]
bl_myli = []
bl_exli = []
bl_feed = []

def bl_main ():
	global bl_defs, bl_lang, bl_conf, bl_list, bl_myli, bl_exli
	random.seed ()

	vh.SQL (
		"create table if not exists `py_bl_lang` ("\
			"`id` bigint(20) unsigned not null primary key,"\
			"`value` text collate utf8_unicode_ci not null"\
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL (
		"create table if not exists `py_bl_conf` ("\
			"`name` varchar(255) collate utf8_unicode_ci not null primary key,"\
			"`value` varchar(255) collate utf8_unicode_ci not null"\
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL (
		"create table if not exists `py_bl_list` ("\
			"`list` varchar(255) collate utf8_unicode_ci not null primary key,"\
			"`type` varchar(25) collate utf8_unicode_ci not null,"\
			"`title` varchar(255) collate utf8_unicode_ci not null,"\
			"`update` smallint(4) unsigned not null default 0,"\
			"`off` tinyint(1) unsigned not null default 0,"\
			"`action` tinyint(1) unsigned not null default 1"\
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL (
		"create table if not exists `py_bl_myli` ("\
			"`loaddr` int(10) unsigned not null,"\
			"`hiaddr` int(10) unsigned not null,"\
			"`title` varchar(255) collate utf8_unicode_ci null default null,"\
			"unique `addr_index` (`loaddr`, `hiaddr`)"\
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL (
		"create table if not exists `py_bl_exli` ("\
			"`loaddr` int(10) unsigned not null,"\
			"`hiaddr` int(10) unsigned not null,"\
			"`title` varchar(255) collate utf8_unicode_ci null default null,"\
			"unique `addr_index` (`loaddr`, `hiaddr`)"\
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL ("alter ignore table `py_bl_list` add column `off` tinyint(1) unsigned not null default 0 after `update`")
	vh.SQL ("alter ignore table `py_bl_list` add column `action` tinyint(1) unsigned not null default 1 after `off`")

	for id, item in bl_lang.iteritems ():
		vh.SQL ("insert ignore into `py_bl_lang` (`id`, `value`) values (%s, '%s')" % (str (id), bl_repsql (item)))
		bl_lang [id] = [item, item]

	sql, rows = vh.SQL ("select * from `py_bl_lang`", 300) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			id = int (item [0])

			if id >= 0 and len (bl_lang) - 1 >= id and item [1].count ("%s") == bl_lang [id][0].count ("%s"):
				bl_lang [id][1] = item [1]

	for name, value in bl_conf.iteritems ():
		vh.SQL ("insert ignore into `py_bl_conf` (`name`, `value`) values ('%s', '%s')" % (bl_repsql (name), bl_repsql (str (value [0]))))

	sql, rows = vh.SQL ("select * from `py_bl_conf`", 100) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_setconf (item [0], item [1], False)

	sql, rows = vh.SQL ("select * from `py_bl_list` order by `off` asc, `action` desc", 100) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_list.append ([item [0], item [1], item [2], int (item [3]), int (item [4]), int (item [5]), 0])

	out = (bl_getlang ("Blacklist %s startup") + ":\r\n\r\n") % bl_defs ["version"]
	out += bl_reload ()
	sql, rows = vh.SQL ("select * from `py_bl_myli`", 1000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_myli.append ([int (item [0]), int (item [1]), bl_getlang ("My item") if item [2] == "NULL" else item [2]])

	out += " [*] %s: %s\r\n" % (bl_getlang ("My list"), str (len (rows)))
	sql, rows = vh.SQL ("select * from `py_bl_exli`", 1000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_exli.append ([int (item [0]), int (item [1]), bl_getlang ("Exception") if item [2] == "NULL" else item [2]])

	out += " [*] %s: %s\r\n" % (bl_getlang ("Exception"), str (len (rows)))

	if bl_conf ["prox_lookup"][0]:
		fail, res = True, bl_curlver ()
		out += (" [*] " + bl_getlang ("%s version: %s") + "\r\n") % ("cURL", res [1])

		if res [0]:
			res = bl_userip ()
			out += (" [*] " + bl_getlang ("User IP: %s") + "\r\n") % res [1]

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

def bl_import (list, type, title, action, update = False): # gzip-p2p, gzip-emule, gzip-range, gzip-single, zip-p2p, zip-emule, zip-range, zip-single, p2p, emule, range, single
	global bl_conf, bl_item
	file = None

	if "://" in list:
		try:
			file = urllib2.urlopen (urllib2.Request (list, None, {"Referer": bl_referer (), "User-agent": bl_useragent ()}), None, bl_conf ["time_down"][0])
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
				temp.append ([bl_addrtoint (loaddr), bl_addrtoint (hiaddr), name.replace ("\\'", "'").replace ("\\\"", "\"").replace ("\\&", "&").replace ("\\\\", "\\"), action])

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
			out += " [*] %s: %s\r\n" % (item [2], bl_import (item [0], item [1], item [2], item [5]))

			if item [3]:
				bl_list [id][6] = time.time ()

	return out

def bl_lookup (data, addr):
	global bl_defs, bl_conf
	list = None

	try:
		list = json.loads (data)
	except:
		return [False, bl_getlang ("Failed to load JSON")]

	if not list:
		return [False, bl_getlang ("Failed to parse JSON")]

	if not "responseStatus" in list or not str (list ["responseStatus"]).isdigit ():
		return [False, bl_getlang ("Failed to get status")]

	if int (list ["responseStatus"]) != 200:
		return [False, bl_getlang ("Unexpected status: %s") % str (list ["responseStatus"])]

	if not "responseData" in list or not "results" in list ["responseData"]:
		return [False, bl_getlang ("Failed to get results")]

	find, finds, ports = re.compile (re.escape (addr) + "\\:(\\d{1,5})"), 0, {}

	for item in list ["responseData"]["results"]:
		if bl_conf ["prox_lookup"][0] and "url" in item and len (item ["url"]):
			part = urlparse.urlsplit (item ["url"])

			if part and len (part [0]) and len (part [1]):
				url = str (part [0].lower () + "://" + part [1].lower () + "/")

				if len (url) and not url in bl_defs ["referer"][1]:
					bl_defs ["referer"][1].append (url)

					if len (bl_defs ["referer"][1]) >= 100:
						bl_defs ["referer"][1].pop (0)

					if bl_conf ["prox_debug"][0] > 1:
						bl_notify (bl_getlang ("New referer: %s") % url)

		for name in ["content", "title", "url"]:
			if not name in item:
				return [False, bl_getlang ("Failed to get search data")]

			match = find.search (re.sub ("<[^<]+?>", "", item [name].replace ("\r", "").replace ("\n", "")))

			if match:
				port = int (match.group (1))

				if port >= 1 and port <= 65535:
					port = str (port)

					if port in ports:
						ports [port] += 1
					else:
						ports [port] = 1

					finds += 1

					if finds >= bl_conf ["prox_match"][0]:
						return [True, max (ports.iteritems (), key = operator.itemgetter (1)) [0]]

					break

	return [False, finds]

def bl_userip ():
	global bl_defs
	res = bl_httpreq (bl_defs ["userip"])

	if not res [0]:
		return [False, res [1]]

	file = StringIO.StringIO (res [1])

	if not file:
		return [False, bl_getlang ("Failed to create file")]

	ini = ConfigParser.ConfigParser ()

	try:
		ini.readfp (file)
	except:
		file.close ()
		return [False, bl_getlang ("Failed to read INI")]

	file.close ()
	addr = ini.get ("address", "ipv4")

	if not addr or not bl_validaddr (addr):
		return [False, bl_getlang ("Failed to get IP")]

	bl_setconf ("prox_userip", addr)
	return [True, addr]

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
	global bl_conf
	file = None

	try:
		file = urllib2.urlopen (urllib2.Request (url, None, {"Referer": bl_referer (), "User-agent": bl_useragent ()}), None, bl_conf ["time_down"][0])
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

def bl_excheck (addr, intaddr, code, name, stat = True):
	global bl_conf, bl_stat, bl_exli

	if len (bl_conf ["code_except"][0]) and len (code) and str ().join ([" ", code, " "]) in str ().join ([" ", bl_conf ["code_except"][0], " "]):
		if bl_waitfeed (addr):
			bl_notify ((bl_getlang ("Blacklisted connection exception from %s.%s: %s") + " | %s") % (addr, code, name, bl_getlang ("Excepted country")))

		if stat:
			bl_stat ["except"] += 1

		return 1

	for item in bl_exli:
		if intaddr >= item [0] and intaddr <= item [1]:
			if bl_waitfeed (addr):
				bl_notify ((bl_getlang ("Blacklisted connection exception from %s.%s: %s") + " | %s") % (addr, code, name, item [2]))

			if stat:
				bl_stat ["except"] += 1

			return 1

	if bl_waitfeed (addr):
		bl_notify (bl_getlang ("Blocking blacklisted connection from %s.%s: %s") % (addr, code, name))

	if stat:
		bl_stat ["block"] += 1

	return 0

def bl_waitfeed (addr, prev = False):
	global bl_defs, bl_conf, bl_feed
	mins, now = (bl_conf ["time_feed"][0] * 60), time.time ()

	for id, item in enumerate (bl_feed):
		if addr == item [0]:
			dif = now - item [1]

			if dif >= mins or (prev and dif <= bl_defs ["prevfeed"]):
				bl_feed [id][1] = now
				return 1

			return 0

	bl_feed.append ([addr, now])
	return 1

def bl_getlang (data):
	global bl_lang

	for item in bl_lang.itervalues ():
		if data == item [0]:
			return item [1]

	return data

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
		if name == "prox_lookup":
			if new and not old:
				res = bl_curlver ()

				if not res [0]:
					return res [1]

				bl_notify (bl_getlang ("%s version: %s") % ("cURL", res [1]))
				res = bl_userip ()

				if not res [0]:
					return res [1]

				bl_notify (bl_getlang ("User IP: %s") % res [1])
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
				del bl_defs ["referer"][1][:]
				bl_defs ["useragent"][1] = None
		elif name == "prox_userip":
			if not bl_validaddr (new):
				bl_setconf ("prox_lookup", "0")

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

def bl_useragent (rand = False):
	global bl_defs
	res = ""

	if rand and bl_defs ["useragent"][1]:
		res = str (bl_defs ["useragent"][1]["random"])
	else:
		res = bl_defs ["useragent"][0] % bl_defs ["version"]

	return res

def bl_referer (rand = False):
	global bl_defs
	res = ""

	if rand and bl_defs ["referer"][1]:
		res = random.choice (bl_defs ["referer"][1])
	else:
		res = bl_defs ["referer"][0]

	return res

def bl_repsql (data):
	return data.replace (chr (92), chr (92) + chr (92)).replace (chr (34), chr (92) + chr (34)).replace (chr (39), chr (92) + chr (39))

def bl_repnmdc (data, out = False):
	if out:
		return data.replace ("&#124;", "|").replace ("&#36;", "$")
	else:
		return data.replace ("|", "&#124;").replace ("$", "&#36;")

def bl_reply (user, data):
	vh.SendDataToUser ("<%s> %s|" % (vh.botname, bl_repnmdc (data)), user)

def bl_notify (data):
	global bl_conf

	if len (bl_conf ["nick_feed"][0]):
		vh.SendDataToUser ("$To: %s From: %s $<%s> %s|" % (bl_conf ["nick_feed"][0], vh.opchatname, vh.opchatname, bl_repnmdc (data)), bl_conf ["nick_feed"][0])
	else:
		vh.SendPMToAll (bl_repnmdc (data), vh.opchatname, bl_conf ["class_feed"][0], 10)

def OnNewConn (addr):
	global bl_conf, bl_stat, bl_item, bl_myli
	bl_stat ["connect"] += 1
	code = vh.GetIPCC (addr)

	if len (bl_conf ["code_block"][0]) and len (code) and str ().join ([" ", code, " "]) in str ().join ([" ", bl_conf ["code_block"][0], " "]):
		if bl_waitfeed (addr):
			bl_notify (bl_getlang ("Blocking blacklisted connection from %s.%s: %s") % (addr, code, bl_getlang ("Blocked country")))

		bl_stat ["block"] += 1
		return 0

	#if code == "L1" or code == "P1":
		#return 1

	intaddr = bl_addrtoint (addr)

	for item in bl_item [intaddr >> 24]:
		if intaddr >= item [0] and intaddr <= item [1]:
			if not item [3]:
				if bl_waitfeed (addr):
					bl_notify (bl_getlang ("Notifying blacklisted connection from %s.%s: %s") % (addr, code, item [2]))

				bl_stat ["notify"] += 1
				return 1

			return bl_excheck (addr, intaddr, code, item [2])

	for item in bl_myli:
		if intaddr >= item [0] and intaddr <= item [1]:
			if not bl_conf ["action_mylist"][0]:
				if bl_waitfeed (addr):
					bl_notify (bl_getlang ("Notifying blacklisted connection from %s.%s: %s") % (addr, code, item [2]))

				bl_stat ["notify"] += 1
				return 1

			return bl_excheck (addr, intaddr, code, item [2])

	return 1

def OnUserLogin (nick):
	global bl_conf, bl_stat, bl_item, bl_prox, bl_myli

	if vh.GetUserClass (nick) >= bl_conf ["class_skip"][0]:
		return 1

	addr = vh.GetUserIP (nick)

	if not len (addr):
		return 1

	code = vh.GetUserCC (nick)
	intaddr = bl_addrtoint (addr)
	addrpos = intaddr >> 24

	for item in bl_item [addrpos]:
		if intaddr >= item [0] and intaddr <= item [1]:
			if not item [3]:
				if bl_waitfeed (addr, True):
					bl_notify (bl_getlang ("Notifying blacklisted login from %s with IP %s.%s: %s") % (nick, addr, code, item [2]))

				return 1

			break

	for item in bl_myli:
		if intaddr >= item [0] and intaddr <= item [1]:
			if not bl_conf ["action_mylist"][0]:
				if bl_waitfeed (addr, True):
					bl_notify (bl_getlang ("Notifying blacklisted login from %s with IP %s.%s: %s") % (nick, addr, code, item [2]))

				return 1

			break

	if code == "L1" or code == "P1":
		return 1

	now = time.time ()

	if not bl_conf ["prox_lookup"][0] or now - vh.starttime < bl_conf ["prox_start"][0] * 60:
		return 1

	size = 0

	for pos in range (len (bl_prox)):
		for id, item in enumerate (bl_prox [pos]):
			if pos == addrpos and addr == item [0]:
				if item [2] < 2:
					if not nick in item [1]:
						bl_prox [pos][id][1].append (nick)
				elif item [2] == 2:
					if bl_waitfeed (addr):
						bl_notify (bl_getlang ("Blocking blacklisted login from %s with IP %s.%s: %s") % (nick, addr, code, bl_getlang ("Public proxy")))

					bl_stat ["block"] += 1
					return 0
				#elif item [3] == 3:
					#pass

				return 1

			if not item [2]:
				size += 1

	if size < bl_conf ["prox_queue"][0]:
		bl_prox [addrpos].append ([addr, [nick], 0, now])

	return 1

def OnOperatorCommand (user, data):
	global bl_defs, bl_lang, bl_conf, bl_stat, bl_list, bl_item, bl_prox, bl_myli, bl_exli, bl_feed

	if data [1:3] == "bl":
		if vh.GetUserClass (user) < bl_conf ["class_conf"][0]:
			bl_reply (user, bl_getlang ("You don't have access to this command."))
			return 0

		if data [4:8] == "stat":
			size, lists, wcurl, acurl = 0, 0, 0, 0

			for pos in range (len (bl_item)):
				size += len (bl_item [pos])

			for item in bl_list:
				if not item [4]:
					lists += 1

			for pos in range (len (bl_prox)):
				acurl += len (bl_prox [pos])

				for item in bl_prox [pos]:
					if item [2] < 3:
						wcurl += 1

			out = bl_getlang ("Blacklist statistics") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("Version: %s")) % bl_defs ["version"]
			out += ("\r\n [*] " + bl_getlang ("Loaded lists: %s")) % (bl_getlang ("%s of %s") % (str (lists), str (len (bl_list))))
			out += ("\r\n [*] " + bl_getlang ("Blacklisted items: %s")) % str (size)
			out += ("\r\n [*] " + bl_getlang ("My items: %s")) % str (len (bl_myli))
			out += ("\r\n [*] " + bl_getlang ("Excepted items: %s")) % str (len (bl_exli))
			out += ("\r\n [*] " + bl_getlang ("Blocked connections: %s")) % str (bl_stat ["block"])
			out += ("\r\n [*] " + bl_getlang ("Notified connections: %s")) % str (bl_stat ["notify"])
			out += ("\r\n [*] " + bl_getlang ("Excepted connections: %s")) % str (bl_stat ["except"])
			out += ("\r\n [*] " + bl_getlang ("Total connections: %s")) % str (bl_stat ["connect"])
			out += ("\r\n [*] " + bl_getlang ("Waiting proxy lookups") + ": %s") % (bl_getlang ("%s of %s") % (str (wcurl), str (acurl)))
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
					if item [2] < 3:
						size += 1
						out += (" [*] " + bl_getlang ("IP: %s.%s") + " | " + bl_getlang ("Status: %s") + " | " + bl_getlang ("Time: %s") + " | " + bl_getlang ("Users: %s") + "\r\n") % (item [0], vh.GetIPCC (item [0]), (bl_getlang ("Queued") if not item [2] else (bl_getlang ("Waiting") if item [2] == 1 else bl_getlang ("Done"))), time.strftime ("%H:%M:%S", time.localtime (item [3])), (bl_getlang ("None") if item [2] == 2 else ", ".join (item [1])))

			if size:
				out = bl_getlang ("Waiting proxy lookups") + ":\r\n\r\n" + out
				out += ("\r\n " + bl_getlang ("Total: %s") + "\r\n") % str (size)
			else:
				out = bl_getlang ("Waiting proxy lookup list is empty.")

			bl_reply (user, out)
			return 0

		if data [4:8] == "feed":
			if not bl_feed:
				out = bl_getlang ("Waiting feed list is empty.")
			else:
				out, mins = (bl_getlang ("Waiting feed list") + ":\r\n\r\n"), (bl_conf ["time_feed"][0] * 60)

				for item in bl_feed:
					out += (" [*] " + bl_getlang ("IP: %s.%s") + " | " + bl_getlang ("Expires: %s") + "\r\n") % (item [0], vh.GetIPCC (item [0]), time.strftime ("%d/%m %H:%M", time.localtime (item [1] + mins)))

				out += ("\r\n " + bl_getlang ("Total: %s") + "\r\n") % str (len (bl_feed))

			bl_reply (user, out)
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

				if size:
					bl_reply (user, (bl_getlang ("Results for title: %s") + "\r\n\r\n%s") % (data [9:], out))
				else:
					bl_reply (user, bl_getlang ("No results for title: %s") % data [9:])

			return 0

		if data [4:10] == "listre":
			out = bl_reload ()

			if len (out):
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
						out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % pars [0][0]
						out += ("\r\n [*] " + bl_getlang ("Higher IP: %s")) % (pars [0][1] or pars [0][0])
						out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if item [3] else bl_getlang ("Notify"))
						bl_reply (user, out)
						return 0

			bl_reply (user, bl_getlang ("List out of item with range: %s - %s") % (pars [0][0], pars [0][1] or pars [0][0]))
			return 0

		if data [4:8] == "look":
			if not data [9:] or not bl_validaddr (data [9:]):
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("look <" + bl_getlang ("addr") + ">"))
				return 0

			if not len (bl_conf ["prox_userip"][0]):
				bl_reply (user, bl_getlang ("Missing user IP."))
				return 0

			res = bl_httpreq (bl_defs ["google"] % (bl_conf ["prox_userip"][0], data [9:]))

			if not res [0]:
				bl_reply (user, res [1])
				return 0

			res = bl_lookup (res [1], data [9:])

			if res [0]:
				bl_reply (user, bl_getlang ("Public proxy detected: %s:%s.%s") % (data [9:], res [1], vh.GetIPCC (data [9:])))
			else:
				if str (res [1]).isdigit ():
					bl_reply (user, bl_getlang ("Not enough matches for %s.%s: %s of %s") % (data [9:], vh.GetIPCC (data [9:]), str (res [1]), str (bl_conf ["prox_match"][0])))
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
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))

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
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if item [6] else bl_getlang ("Notify"))
					bl_reply (user, out)
					return 0

			bl_list.append ([pars [0][0], pars [0][1], pars [0][2], update, 0, 1, time.time () if update else 0])
			vh.SQL ("insert into `py_bl_list` (`list`, `type`, `title`, `update`) values ('%s', '%s', '%s', %s)" % (bl_repsql (pars [0][0]), bl_repsql (pars [0][1]), bl_repsql (pars [0][2]), str (update)))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_list) - 1)
			out += ("\r\n [*] " + bl_getlang ("List: %s")) % pars [0][0]
			out += ("\r\n [*] " + bl_getlang ("Type: %s")) % pars [0][1]
			out += ("\r\n [*] " + bl_getlang ("Title: %s")) % pars [0][2]
			out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not update else (bl_getlang ("%s minute") + " | %s") % (str (update), time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (update * 60)))) if update == 1 else (bl_getlang ("%s minutes") + " | %s") % (str (update), time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (update * 60)))))
			out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
			out += ("\r\n [*] " + bl_getlang ("Action: %s")) % bl_getlang ("Block")
			out += ("\r\n [*] " + bl_getlang ("Status: %s") + "\r\n") % bl_import (pars [0][0], pars [0][1], pars [0][2], 1)
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
				out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
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
					bl_list [id][4], bl_list [id][6] = 1, 0
					vh.SQL ("update `py_bl_list` set `off` = 1 where `list` = '%s'" % bl_repsql (item [0]))

					out = bl_getlang ("Item now disabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else ((bl_getlang ("%s minute") % item [3]) if item [3] == 1 else (bl_getlang ("%s minutes") % item [3])))
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("Yes")
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					bl_reply (user, out)
				else:
					bl_list [id][4] = 0
					vh.SQL ("update `py_bl_list` set `off` = 0 where `list` = '%s'" % bl_repsql (item [0]))

					if item [3]:
						bl_list [id][6] = time.time ()

					out = bl_getlang ("Item now enabled") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))))
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Status: %s") + "\r\n") % bl_import (item [0], item [1], item [2], item [5])
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
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % bl_getlang ("Notify")
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
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (item [6] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else bl_getlang ("%s minute") % item [3] if item [3] == 1 else bl_getlang ("%s minutes") % item [3])

					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % (bl_getlang ("No") if not item [4] else bl_getlang ("Yes"))
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % bl_getlang ("Block")
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
						bl_list [id][6] = time.time ()

					out = bl_getlang ("Item load result") + ":\r\n"
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("List: %s")) % item [0]
					out += ("\r\n [*] " + bl_getlang ("Type: %s")) % item [1]
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Update: %s")) % (bl_getlang ("On load") if not item [3] else (bl_getlang ("%s minute") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))) if item [3] == 1 else (bl_getlang ("%s minutes") + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.localtime (time.time () + (item [3] * 60)))))
					out += ("\r\n [*] " + bl_getlang ("Disabled: %s")) % bl_getlang ("No")
					out += ("\r\n [*] " + bl_getlang ("Action: %s")) % (bl_getlang ("Block") if item [5] else bl_getlang ("Notify"))
					out += ("\r\n [*] " + bl_getlang ("Status: %s") + "\r\n") % bl_import (item [0], item [1], item [2], item [5])
					bl_reply (user, out)
				else:
					bl_reply (user, bl_getlang ("Item is disabled") % str (id))
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:9] == "myall":
			if not bl_myli:
				out = bl_getlang ("My list is empty.")
			else:
				out = bl_getlang ("My list") + ":\r\n"

				for id, item in enumerate (bl_myli):
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % bl_inttoaddr (item [0])
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s")) % bl_inttoaddr (item [1])
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
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % pars [0][0]
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s")) % (pars [0][1] or pars [0][0])
					out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))
					bl_reply (user, out)
					return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])
			bl_myli.append ([loaddr, hiaddr, pars [0][2] or bl_getlang ("My item")])
			vh.SQL ("insert ignore into `py_bl_myli` (`loaddr`, `hiaddr`, `title`) values (%s, %s, %s)" % (str (loaddr), str (hiaddr), ("'" + bl_repsql (pars [0][2]) + "'" if pars [0][2] else "null")))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_myli) - 1)
			out += ("\r\n [*] " + bl_getlang ("Title: %s")) % (pars [0][2] or bl_getlang ("My item"))
			out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % pars [0][0]
			out += ("\r\n [*] " + bl_getlang ("Higher IP: %s")) % (pars [0][1] or pars [0][0])
			out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))
			bl_reply (user, out)
			return 0

		if data [4:9] == "mydel":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("mydel <" + bl_getlang ("id") + ">"))
				return 0

			if id >= 0 and bl_myli and len (bl_myli) - 1 >= id:
				item, stop = bl_myli.pop (id), False
				vh.SQL ("delete from `py_bl_myli` where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

				out = bl_getlang ("Item deleted from list") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
				out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
				out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % bl_inttoaddr (item [0])
				out += ("\r\n [*] " + bl_getlang ("Higher IP: %s")) % bl_inttoaddr (item [1])
				out += ("\r\n [*] " + bl_getlang ("Action: %s") + "\r\n") % (bl_getlang ("Block") if bl_conf ["action_mylist"][0] else bl_getlang ("Notify"))
				bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		if data [4:9] == "exall":
			if not bl_exli:
				out = bl_getlang ("Exception list is empty.")
			else:
				out = bl_getlang ("Exception list") + ":\r\n"

				for id, item in enumerate (bl_exli):
					out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
					out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % bl_inttoaddr (item [0])
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s") + "\r\n") % bl_inttoaddr (item [1])

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
					out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % pars [0][0]
					out += ("\r\n [*] " + bl_getlang ("Higher IP: %s") + "\r\n") % (pars [0][1] or pars [0][0])
					bl_reply (user, out)
					return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])
			bl_exli.append ([loaddr, hiaddr, pars [0][2] or bl_getlang ("Exception")])
			vh.SQL ("insert ignore into `py_bl_exli` (`loaddr`, `hiaddr`, `title`) values (%s, %s, %s)" % (str (loaddr), str (hiaddr), ("'" + bl_repsql (pars [0][2]) + "'" if pars [0][2] else "null")))

			out = bl_getlang ("Item added to list") + ":\r\n"
			out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (len (bl_exli) - 1)
			out += ("\r\n [*] " + bl_getlang ("Title: %s")) % (pars [0][2] or bl_getlang ("Exception"))
			out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % pars [0][0]
			out += ("\r\n [*] " + bl_getlang ("Higher IP: %s") + "\r\n") % (pars [0][1] or pars [0][0])
			bl_reply (user, out)
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
							bl_item [intaddr >> 24].append ([intaddr, intaddr, bl_getlang ("Public proxy"), bl_conf ["action_proxy"][0]]) # todo: also add to mysql table when we have one
							bl_prox [pos].pop (pid)
							stop = True
							break

					if stop:
						break

				out = bl_getlang ("Item deleted from list") + ":\r\n"
				out += ("\r\n [*] " + bl_getlang ("ID: %s")) % str (id)
				out += ("\r\n [*] " + bl_getlang ("Title: %s")) % item [2]
				out += ("\r\n [*] " + bl_getlang ("Lower IP: %s")) % bl_inttoaddr (item [0])
				out += ("\r\n [*] " + bl_getlang ("Higher IP: %s") + "\r\n") % bl_inttoaddr (item [1])
				bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

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

		if data [4:8] == "lang":
			out = bl_getlang ("Translation list") + ":\r\n\r\n"

			for id, lang in sorted (bl_lang.iteritems ()):
				out += (" %s. %s = %s\r\n") % (str (id), lang [0], lang [1])

			bl_reply (user, out)
			return 0

		if data [4:8] == "tran":
			pars = re.findall ("^(\\S+)[ ]*(.*)$", data [9:])

			if not pars or not pars [0][0] or not pars [0][1]:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("tran <" + bl_getlang ("id") + "> <" + bl_getlang ("value") + ">"))
				return 0

			if pars [0][0].isdigit ():
				id = int (pars [0][0])
			else:
				bl_reply (user, bl_getlang ("Missing command parameters: %s") % ("tran <" + bl_getlang ("id") + "> <" + bl_getlang ("value") + ">"))
				return 0

			if id >= 0 and len (bl_lang) - 1 >= id:
				if pars [0][1].count ("%s") == bl_lang [id][1].count ("%s"):
					vh.SQL ("update `py_bl_lang` set `value` = '%s' where `id` = %s" % (bl_repsql (pars [0][1]), str (id)))
					old, bl_lang [id][1] = bl_lang [id][1], pars [0][1]

					out = (bl_getlang ("Updated translation with ID: %s") + "\r\n") % str (id)
					out += ("\r\n [*] " + bl_getlang ("Old value: %s")) % old
					out += ("\r\n [*] " + bl_getlang ("New value: %s") + "\r\n") % pars [0][1]
					bl_reply (user, out)
				else:
					out = (bl_getlang ("Parameter count mismatch in translation with ID: %s") + "\r\n") % str (id)
					out += ("\r\n [*] " + bl_getlang ("Old value: %s")) % bl_lang [id][1]
					out += ("\r\n [*] " + bl_getlang ("New value: %s") + "\r\n") % pars [0][1]
					bl_reply (user, out)
			else:
				bl_reply (user, bl_getlang ("List out of item with ID: %s") % str (id))

			return 0

		out = bl_getlang ("Blacklist usage") + ":\r\n\r\n"

		out += " stat\t\t\t\t\t- " + bl_getlang ("Script statistics") + "\r\n"
		out += " prox\t\t\t\t\t- " + bl_getlang ("Show waiting proxy lookups") + "\r\n"
		out += " feed\t\t\t\t\t- " + bl_getlang ("Show waiting feed list") + "\r\n\r\n"

		out += " find <" + bl_getlang ("item") + ">\t\t\t\t- " + bl_getlang ("Search in loaded lists") + "\r\n"
		out += " del <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "]\t\t\t- " + bl_getlang ("Delete blacklisted item") + "\r\n\r\n"

		out += " look <" + bl_getlang ("addr") + ">\t\t\t\t- " + bl_getlang ("Public proxy lookup") + "\r\n\r\n"

		out += " listall\t\t\t\t\t- " + bl_getlang ("Show all lists") + "\r\n"
		out += " listadd <" + bl_getlang ("list") + "> <" + bl_getlang ("type") + "> <\"" + bl_getlang ("title") + "\"> [" + bl_getlang ("update") + "]\t- " + bl_getlang ("Load new list") + "\r\n"
		out += " listoff <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Disable or enable list") + "\r\n"
		out += " listact <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Set list block action") + "\r\n"
		out += " listget <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Force load of existing list") + "\r\n"
		out += " listdel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete existing list") + "\r\n"
		out += " listre\t\t\t\t\t- " + bl_getlang ("Reload all lists") + "\r\n\r\n"

		out += " myall\t\t\t\t\t- " + bl_getlang ("Show my list") + "\r\n"
		out += " myadd <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "] [" + bl_getlang ("title") + "]\t\t- " + bl_getlang ("New my item") + "\r\n"
		out += " mydel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete my item") + "\r\n\r\n"

		out += " exall\t\t\t\t\t- " + bl_getlang ("Show exception list") + "\r\n"
		out += " exadd <" + bl_getlang ("addr") + ">-[" + bl_getlang ("range") + "] [" + bl_getlang ("title") + "]\t\t\t- " + bl_getlang ("New exception item") + "\r\n"
		out += " exdel <" + bl_getlang ("id") + ">\t\t\t\t- " + bl_getlang ("Delete an exception") + "\r\n\r\n"

		out += " conf\t\t\t\t\t- " + bl_getlang ("Show current configuration") + "\r\n"
		out += " set <" + bl_getlang ("item") + "> [" + bl_getlang ("value") + "]\t\t\t\t- " + bl_getlang ("Set configuration item") + "\r\n\r\n"

		out += " lang\t\t\t\t\t- " + bl_getlang ("Show current translation") + "\r\n"
		out += " tran <" + bl_getlang ("id") + "> <" + bl_getlang ("value") + ">\t\t\t\t- " + bl_getlang ("Set translation string") + "\r\n"

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
			if not item [4] and item [3] and now - item [6] >= item [3] * 60:
				bl_list [id][6], out = now, bl_import (item [0], item [1], item [2], item [5], True)

				if bl_conf ["notify_update"][0]:
					bl_notify ("%s: %s" % (item [2], out))

	if bl_conf ["prox_lookup"][0] and now - bl_stat ["proxy"] >= bl_conf ["prox_timer"][0]:
		bl_stat ["proxy"], start, dels = now, 0, []

		for pos in range (len (bl_prox)):
			for id, item in enumerate (bl_prox [pos]):
				if not item [2]:
					if start < bl_conf ["prox_maxreq"][0]:
						start += 1

						try:
							os.system (bl_defs ["curlreq"] % (str (1), str (1), str (bl_conf ["time_down"][0]), str (bl_conf ["time_down"][0] * 2), bl_conf ["prox_userip"][0], bl_useragent (True), bl_referer (True), os.path.join (bl_defs ["datadir"], item [0]), (bl_defs ["google"] % (bl_conf ["prox_userip"][0], item [0]))))
							bl_prox [pos][id][2], bl_prox [pos][id][3] = 1, now
						except:
							bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], vh.GetIPCC (item [0]), bl_getlang ("Failed to execute command")))
							dels.insert (0, [pos, id])
				elif item [2] == 1:
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

							if file:
								data = None

								try:
									data = file.read ()
								except:
									pass

								file.close ()

								if data:
									res = bl_lookup (data, item [0])

									if res [0]:
										bl_notify (bl_getlang ("Public proxy detected: %s:%s.%s") % (item [0], res [1], code))
										intaddr = bl_addrtoint (item [0])
										keep = True

										if not bl_conf ["action_proxy"][0]:
											if bl_waitfeed (item [0]):
												bl_notify (bl_getlang ("Notifying blacklisted login from %s with IP %s.%s: %s") % (item [1][0] if len (item [1]) == 1 else str (item [1]), item [0], code, bl_getlang ("Public proxy")))

											bl_stat ["notify"] += 1
											bl_prox [pos][id][2] = 3
										elif bl_excheck (item [0], intaddr, code, bl_getlang ("Public proxy"), False):
											bl_stat ["except"] += len (item [1])
											bl_prox [pos][id][2] = 3
										else:
											for nick in item [1]:
												vh.CloseConnection (nick)

											bl_stat ["block"] += len (item [1])
											bl_prox [pos][id][2] = 2
											bl_item [intaddr >> 24].append ([intaddr, intaddr, bl_getlang ("Public proxy"), bl_conf ["action_proxy"][0]]) # todo: also add to mysql table when we have one
									else:
										if str (res [1]).isdigit ():
											keep = True
											bl_prox [pos][id][2] = 3

											if (bl_conf ["prox_debug"][0] and int (res [1])) or bl_conf ["prox_debug"][0] > 1:
												bl_notify (bl_getlang ("Not enough matches for %s.%s: %s of %s") % (item [0], code, str (res [1]), str (bl_conf ["prox_match"][0])))
										elif not bl_conf ["prox_nofail"][0]:
											bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], code, res [1]))
								else:
									bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], code, bl_getlang ("Failed to read data")))
							else:
								bl_notify (bl_getlang ("Failed proxy detection for %s.%s: %s") % (item [0], code, bl_getlang ("Failed to open file")))

							if keep:
								del bl_prox [pos][id][1][:]
								bl_prox [pos][id][3] = now
							else:
								dels.insert (0, [pos, id])

							bl_remfile (name)
							continue

					if now - item [3] >= (bl_conf ["time_down"][0] * 2) + (bl_conf ["prox_timer"][0] * 2):
						dels.insert (0, [pos, id])

						if isfile:
							bl_remfile (name)
				elif item [2] == 2:
					if now - item [3] >= bl_defs ["delwait"]:
						dels.insert (0, [pos, id])
				#elif item [2] == 3:
					#pass

		for item in dels:
			bl_prox [item [0]].pop (item [1])

bl_main ()

# end of file
