# Verlihub Blacklist 1.1.8
# Written by RoLex, 2010-2016
# Special thanks to Frog

# Changelog:

# 0.0.1 - Initial release
# 1.0.0 - Added "find_maxres" configuration to limit number of results on find action
# 1.0.0 - Added country codes of addresses in waiting feed list
# 1.1.0 - Added "time_down" configuration to specify timeout of download operation in seconds
# 1.1.1 - Added "listoff" command to disable or enable lists
# 1.1.2 - Added another read failure check
# 1.1.3 - Fixed display of item configuration old value when changing from zero
# 1.1.3 - Fixed default exception file creation in wrong directory
# 1.1.3 - Added translation ability with list command "lang" and update command "trans"
# 1.1.4 - Added compression file format "zip"
# 1.1.4 - Added data file format "emule"
# 1.1.5 - Added "listget" command to force list load
# 1.1.6 - Added exception notifications to waiting feed list aswell
# 1.1.7 - Fixed OnTimer callback
# 1.1.8 - Added referer and user agent headers for URL requests
# 1.1.8 - Added different method of validating numbers
# 1.1.8 - Added different method of getting hub bot nicks
# 1.1.8 - Added public proxy lookup based on number of Google search results
# 1.1.8 - Added "listre" command to reload all blacklist lists
# 1.1.8 - Added "del" command to delete single blacklisted item in real time
# 1.1.8 - Added "code_block" configuration for space separated list of blocked country codes
# 1.1.8 - Added "code_except" configuration for space separated list of excepted country codes
# 1.1.8 - Added short configuration explanations
# 1.1.8 - Added custom blacklist to manage with "my*" commands
# 1.1.8 - Added exception list to database instead of text file
# 1.1.8 - Fixed missing global variable declarations

import vh, re, urllib2, urlparse, gzip, zipfile, StringIO, time, os, subprocess, socket, struct, operator, random, json, ConfigParser

bl_defs = {
	"version": "1.1.8", # todo: update on release
	"curlver": ["curl", "-V"],
	"curlreq": "curl -G -L --max-redirs %s --retry %s --connect-timeout %s -m %s --interface %s -A \"%s\" -e \"%s\" -s -o \"%s\" \"%s\" &",
	"google": "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&userip=%s&rsz=8&q=proxy%%20OR%%20socks%%20%%22%s%%3a1..65535%%22",
	"userip": "http://www.te-home.net/?do=tools&action=whatismyip",
	"referer": ["https://github.com/verlihub/python/", []],
	"useragent": ["Blacklist/%s", None],
	"datadir": os.path.join (vh.basedir, "blackdata")
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
	171: "New referer: %s"
}

bl_conf = {
	"nick_feed": ["", "str", 0, 255, 150],
	"code_block": ["", "str", 0, 255, 151],
	"code_except": ["", "str", 0, 255, 152],
	"class_feed": [5, "int", 0, 11, 153],
	"class_conf": [10, "int", 3, 11, 154],
	"class_skip": [3, "int", 0, 11, 155],
	"time_feed": [60, "int", 0, 1440, 156],
	"time_down": [5, "int", 1, 300, 157],
	"notify_update": [1, "int", 0, 1, 158],
	"find_maxres": [1000, "int", 1, 10000, 159],
	"prox_lookup": [0, "int", 0, 1, 160],
	"prox_userip": ["", "str", 0, 15, 161],
	"prox_match": [3, "int", 1, 8, 162],
	"prox_start": [5, "int", 0, 30, 163],
	"prox_timer": [3, "int", 1, 300, 164],
	"prox_queue": [100, "int", 1, 10000, 165],
	"prox_maxreq": [1, "int", 1, 100, 166],
	"prox_nofail": [0, "int", 0, 1, 168],
	"prox_debug": [0, "int", 0, 2, 169]
}

bl_stat = {
	"connect": 0l,
	"block": 0l,
	"except": 0l,
	"update": time.time (),
	"proxy": time.time ()
}

bl_list = [
	# ["http://list.iblocklist.com/?list=ijfqtofzixtwayqovmxn&fileformat=p2p&archiveformat=gz", "gzip-p2p", "Primary threat", 0, 0, 0],
	# ["http://list.iblocklist.com/?list=xoebmbyexwuiogmbyprb&fileformat=p2p&archiveformat=gz", "gzip-p2p", "Proxy", 0, 0, 0],
	# ["http://ledo.feardc.net/mirror/torexit.list", "single", "Tor exit", 60, 0, 0],
	# ["http://ledo.feardc.net/mirror/torserver.list", "single", "Tor server", 60, 0, 0]
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
			"`off` tinyint(1) unsigned not null default 0"\
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL (
		"create table if not exists `py_bl_myli` ("\
			"`loaddr` int(10) unsigned not null,"\
			"`hiaddr` int(10) unsigned not null,"\
			"`title` varchar(255) collate utf8_unicode_ci null default null,"\
			"unique `addr_index` (`loaddr`, `hiaddr`)"
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL (
		"create table if not exists `py_bl_exli` ("\
			"`loaddr` int(10) unsigned not null,"\
			"`hiaddr` int(10) unsigned not null,"\
			"`title` varchar(255) collate utf8_unicode_ci null default null,"\
			"unique `addr_index` (`loaddr`, `hiaddr`)"
		") engine = myisam default character set utf8 collate utf8_unicode_ci"
	)

	vh.SQL ("alter ignore table `py_bl_list` add column `off` tinyint(1) unsigned not null default 0 after `update`")

	for id, item in bl_lang.iteritems ():
		vh.SQL ("insert ignore into `py_bl_lang` (`id`, `value`) values (%s, '%s')" % (str (id), bl_repsql (item)))

	sql, rows = vh.SQL ("select * from `py_bl_lang`", 300) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			id = int (item [0])

			if id >= 0 and len (bl_lang) - 1 >= id and item [1].count ("%s") == bl_lang [id].count ("%s"):
				bl_lang [id] = item [1]

	for name, value in bl_conf.iteritems ():
		vh.SQL ("insert ignore into `py_bl_conf` (`name`, `value`) values ('%s', '%s')" % (bl_repsql (name), bl_repsql (str (value [0]))))

	sql, rows = vh.SQL ("select * from `py_bl_conf`", 100) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_setconf (item [0], item [1], False)

	sql, rows = vh.SQL ("select * from `py_bl_list`", 100) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_list.append ([item [0], item [1], item [2], int (item [3]), int (item [4]), 0])

	out = (bl_lang [0] + ":\r\n\r\n") % bl_defs ["version"]
	out += bl_reload ()
	sql, rows = vh.SQL ("select * from `py_bl_myli`", 1000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_myli.append ([int (item [0]), int (item [1]), bl_lang [142] if item [2] == "NULL" else item [2]])

	out += " [*] %s: %s\r\n" % (bl_lang [11], str (len (rows)))
	sql, rows = vh.SQL ("select * from `py_bl_exli`", 1000) # todo: dont forget about limit

	if sql and rows:
		for item in rows:
			bl_exli.append ([int (item [0]), int (item [1]), bl_lang [1] if item [2] == "NULL" else item [2]])

	out += " [*] %s: %s\r\n" % (bl_lang [1], str (len (rows)))

	if bl_conf ["prox_lookup"][0]:
		fail, res = True, bl_curlver ()
		out += (" [*] " + bl_lang [137] + "\r\n") % ("cURL", res [1])

		if res [0]:
			res = bl_userip ()
			out += (" [*] " + bl_lang [115] + "\r\n") % res [1]

			if res [0]:
				res = bl_makedir (bl_defs ["datadir"])
				out += (" [*] " + bl_lang [123] + "\r\n") % res [1]

				if res [0]:
					try:
						import fake_useragent
						bl_defs ["useragent"][1] = fake_useragent.UserAgent ()
					except:
						pass

					out += (" [*] " + bl_lang [170] + "\r\n") % bl_useragent (True)
					fail = False

		if fail:
			bl_setconf ("prox_lookup", "0")

	bl_notify (out)

def bl_import (list, type, title, update = False): # gzip-p2p, gzip-emule, gzip-range, gzip-single, zip-p2p, zip-emule, zip-range, zip-single, p2p, emule, range, single
	global bl_lang, bl_conf, bl_item
	file = None

	if "://" in list:
		try:
			file = urllib2.urlopen (urllib2.Request (list, None, {"Referer": bl_referer (), "User-agent": bl_useragent ()}), None, bl_conf ["time_down"][0])
		except urllib2.HTTPError:
			return bl_lang [2]
		except urllib2.URLError:
			return bl_lang [3]
		except:
			return bl_lang [4]
	else:
		try:
			file = open (list, "r")
		except:
			pass

	if not file:
		return bl_lang [110 if "://" in list else 10]

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
		return bl_lang [9]

	try:
		find = re.compile ("^" + find + "$")
	except:
		file.close ()
		return bl_lang [5]

	if "gzip" in type or "zip" in type:
		data = None

		try:
			data = StringIO.StringIO (file.read ())
		except:
			pass

		file.close ()

		if not data:
			return bl_lang [7]

		if "gzip" in type:
			try:
				file = gzip.GzipFile (fileobj = data)
				file.read (1)
			except:
				return bl_lang [6]
		elif "zip" in type:
			try:
				arch = zipfile.ZipFile (file = data)
				file = arch.open (arch.namelist () [0])
				arch.close ()
				file.read (1)
			except:
				return bl_lang [101]

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
				temp.append ([bl_addrtoint (loaddr), bl_addrtoint (hiaddr), name.replace ("\\'", "'").replace ("\\\"", "\"").replace ("\\&", "&").replace ("\\\\", "\\")])

	file.close ()

	for item in temp:
		for pos in xrange (item [0] >> 24, (item [1] >> 24) + 1):
			if not update or not item in bl_item [pos]:
				bl_item [pos].append (item)

	return bl_lang [8] % str (len (temp))

def bl_reload ():
	global bl_list, bl_item
	del bl_item [:]
	bl_item = [[] for pos in xrange (256)]
	out = ""

	for id, item in enumerate (bl_list):
		if not item [4]:
			out += " [*] %s: %s\r\n" % (item [2], bl_import (item [0], item [1], item [2]))

			if item [3]:
				bl_list [id][5] = time.time ()

	return out

def bl_lookup (data, addr):
	global bl_defs, bl_lang, bl_conf
	list = None

	try:
		list = json.loads (data)
	except:
		return [False, bl_lang [105]]

	if not list:
		return [False, bl_lang [106]]

	if not "responseStatus" in list or not str (list ["responseStatus"]).isdigit ():
		return [False, bl_lang [107]]

	if int (list ["responseStatus"]) != 200:
		return [False, bl_lang [108] % str (list ["responseStatus"])]

	if not "responseData" in list or not "results" in list ["responseData"]:
		return [False, bl_lang [109]]

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
						bl_notify (bl_lang [171] % url)

		for name in ["content", "title", "url"]:
			if not name in item:
				return [False, bl_lang [111]]

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
	global bl_defs, bl_lang
	res = bl_httpreq (bl_defs ["userip"])

	if not res [0]:
		return [False, res [1]]

	file = StringIO.StringIO (res [1])

	if not file:
		return [False, bl_lang [113]]

	ini = ConfigParser.ConfigParser ()

	try:
		ini.readfp (file)
	except:
		file.close ()
		return [False, bl_lang [112]]

	file.close ()
	addr = ini.get ("address", "ipv4")

	if not addr or not bl_validaddr (addr):
		return [False, bl_lang [114]]

	bl_setconf ("prox_userip", addr)
	return [True, addr]

def bl_curlver ():
	global bl_defs, bl_lang
	out = None

	try:
		out = subprocess.check_output (bl_defs ["curlver"])
	except:
		pass

	if not out:
		return [False, bl_lang [125]]

	find = re.compile ("(\\d+[\\.\\d]+)").search (out)

	if not find:
		return [False, bl_lang [136]]

	return [True, find.group (1)]

def bl_httpreq (url):
	global bl_lang, bl_conf
	file = None

	try:
		file = urllib2.urlopen (urllib2.Request (url, None, {"Referer": bl_referer (), "User-agent": bl_useragent ()}), None, bl_conf ["time_down"][0])
	except urllib2.HTTPError:
		return [False, bl_lang [2]]
	except urllib2.URLError:
		return [False, bl_lang [3]]
	except:
		return [False, bl_lang [4]]

	if not file:
		return [False, bl_lang [110]]

	data = None

	try:
		data = file.read ()
	except:
		pass

	file.close ()

	if data:
		return [True, data]
	else:
		return [False, bl_lang [7]]

def bl_remfile (file):
	res = True

	try:
		os.unlink (file)
	except:
		res = False

	return res

def bl_makedir (dir):
	global bl_lang

	if not os.path.exists (dir):
		try:
			os.makedirs (dir)
		except:
			return [False, bl_lang [124]]
	else:
		for file in os.listdir (dir):
			file = os.path.join (dir, file)

			if os.path.isfile (file):
				bl_remfile (file)

	return [True, dir]

def bl_excheck (addr, intaddr, code, name, stat = True):
	global bl_lang, bl_conf, bl_stat, bl_exli

	if len (bl_conf ["code_except"][0]) and len (code) and str ().join ([" ", code, " "]) in str ().join ([" ", bl_conf ["code_except"][0], " "]):
		if bl_waitfeed (addr):
			bl_notify ((bl_lang [18] + " | %s") % (addr, code, name, bl_lang [148]))

		if stat:
			bl_stat ["except"] += 1

		return 1

	for item in bl_exli:
		if intaddr >= item [0] and intaddr <= item [1]:
			if bl_waitfeed (addr):
				bl_notify ((bl_lang [18] + " | %s") % (addr, code, name, item [2]))

			if stat:
				bl_stat ["except"] += 1

			return 1

	if bl_waitfeed (addr):
		bl_notify (bl_lang [19] % (addr, code, name))

	if stat:
		bl_stat ["block"] += 1

	return 0

def bl_waitfeed (addr):
	global bl_conf, bl_feed
	mins, now = (bl_conf ["time_feed"][0] * 60), time.time ()

	for id, item in enumerate (bl_feed):
		if addr == item [0]:
			if now - item [1] >= mins:
				bl_feed [id][1] = now
				return 1

			return 0

	bl_feed.append ([addr, now])
	return 1

def bl_getconf (name):
	global bl_conf

	if not name in bl_conf:
		return None

	return bl_conf [name][0]

def bl_setconf (name, value, update = True):
	global bl_defs, bl_lang, bl_conf, bl_prox

	if not name in bl_conf:
		return bl_lang [17]

	old, new = bl_conf [name][0], str (value)

	if bl_conf [name][1] == "int":
		if not new.isdigit ():
			return bl_lang [14]

		new = int (new)

		if new < bl_conf [name][2]:
			return bl_lang [12]
		elif new > bl_conf [name][3]:
			return bl_lang [13]
	else:
		if len (new) < bl_conf [name][2]:
			return bl_lang [15]
		elif len (new) > bl_conf [name][3]:
			return bl_lang [16]

	if update:
		if name == "prox_lookup":
			if new and not old:
				res = bl_curlver ()

				if not res [0]:
					return res [1]

				bl_notify (bl_lang [137] % ("cURL", res [1]))
				res = bl_userip ()

				if not res [0]:
					return res [1]

				bl_notify (bl_lang [115] % res [1])
				res = bl_makedir (bl_defs ["datadir"])

				if not res [0]:
					return res [1]

				bl_notify (bl_lang [123] % res [1])

				try:
					import fake_useragent
					bl_defs ["useragent"][1] = fake_useragent.UserAgent ()
				except:
					pass

				bl_notify (bl_lang [170] % bl_useragent (True))
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
	global bl_lang, bl_conf, bl_stat, bl_item, bl_myli
	bl_stat ["connect"] += 1
	code = None

	if len (bl_conf ["code_block"][0]):
		code = vh.GetIPCC (addr)

		if len (code) and str ().join ([" ", code, " "]) in str ().join ([" ", bl_conf ["code_block"][0], " "]):
			if bl_waitfeed (addr):
				bl_notify (bl_lang [19] % (addr, code, bl_lang [149]))

			bl_stat ["block"] += 1
			return 0

	intaddr = bl_addrtoint (addr)

	for item in bl_item [intaddr >> 24]:
		if intaddr >= item [0] and intaddr <= item [1]:
			return bl_excheck (addr, intaddr, code or vh.GetIPCC (addr), item [2])

	for item in bl_myli:
		if intaddr >= item [0] and intaddr <= item [1]:
			return bl_excheck (addr, intaddr, code or vh.GetIPCC (addr), item [2])

	return 1

def OnUserLogin (nick):
	global bl_lang, bl_conf, bl_stat, bl_prox
	now = time.time ()

	if not bl_conf ["prox_lookup"][0] or now - vh.starttime < bl_conf ["prox_start"][0] * 60:
		return 1

	if vh.GetUserClass (nick) >= bl_conf ["class_skip"][0]:
		return 1

	addr = vh.GetUserIP (nick)

	if not len (addr):
		return 1

	addrpos, size = (bl_addrtoint (addr) >> 24), 0

	for pos in range (len (bl_prox)):
		for id, item in enumerate (bl_prox [pos]):
			if pos == addrpos and addr == item [0]:
				if item [2] < 2:
					if not nick in item [1]:
						bl_prox [pos][id][1].append (nick)
				elif item [2] == 2:
					if bl_waitfeed (addr):
						bl_notify (bl_lang [19] % (addr, vh.GetIPCC (addr), bl_lang [126]))

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
			bl_reply (user, bl_lang [20])
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

			out = bl_lang [21] + ":\r\n"
			out += ("\r\n [*] " + bl_lang [22]) % bl_defs ["version"]
			out += ("\r\n [*] " + bl_lang [23]) % (bl_lang [138] % (str (lists), str (len (bl_list))))
			out += ("\r\n [*] " + bl_lang [24]) % str (size)
			out += ("\r\n [*] " + bl_lang [147]) % str (len (bl_myli))
			out += ("\r\n [*] " + bl_lang [25]) % str (len (bl_exli))
			out += ("\r\n [*] " + bl_lang [26]) % str (bl_stat ["block"])
			out += ("\r\n [*] " + bl_lang [27]) % str (bl_stat ["except"])
			out += ("\r\n [*] " + bl_lang [28]) % str (bl_stat ["connect"])
			out += ("\r\n [*] " + bl_lang [129] + ": %s") % (bl_lang [138] % (str (wcurl), str (acurl)))
			out += ("\r\n [*] " + bl_lang [70] + ": %s\r\n") % str (len (bl_feed))
			bl_reply (user, out)
			return 0

		if data [4:8] == "prox":
			if not bl_conf ["prox_lookup"][0]:
				bl_reply (user, bl_lang [132])
				return 0

			size, out = 0, ""

			for pos in range (len (bl_prox)):
				for item in bl_prox [pos]:
					if item [2] < 3:
						size += 1
						out += (" [*] " + bl_lang [71] + " | " + bl_lang [51] + " | " + bl_lang [130] + " | " + bl_lang [131] + "\r\n") % (item [0], vh.GetIPCC (item [0]), (bl_lang [134] if not item [2] else (bl_lang [135] if item [2] == 1 else bl_lang [139])), time.strftime ("%H:%M:%S", time.gmtime (item [3])), (bl_lang [95] if item [2] == 2 else ", ".join (item [1])))

			if size:
				out = bl_lang [129] + ":\r\n\r\n" + out
				out += ("\r\n " + bl_lang [133] + "\r\n") % str (size)
			else:
				out = bl_lang [128]

			bl_reply (user, out)
			return 0

		if data [4:8] == "feed":
			if not bl_feed:
				out = bl_lang [69]
			else:
				out, mins = (bl_lang [70] + ":\r\n\r\n"), (bl_conf ["time_feed"][0] * 60)

				for item in bl_feed:
					out += (" [*] " + bl_lang [71] + " | " + bl_lang [72] + "\r\n") % (item [0], vh.GetIPCC (item [0]), time.strftime ("%d/%m %H:%M", time.gmtime (item [1] + mins)))

				out += ("\r\n " + bl_lang [133] + "\r\n") % str (len (bl_feed))

			bl_reply (user, out)
			return 0

		if data [4:8] == "find":
			if not data [9:]:
				bl_reply (user, bl_lang [29] % ("find <" + bl_lang [87] + ">"))
				return 0

			out, size = "", 0

			if bl_validaddr (data [9:]):
				intaddr = bl_addrtoint (data [9:])

				for item in bl_item [intaddr >> 24]:
					if intaddr >= item [0] and intaddr <= item [1]:
						out += " %s - %s : %s\r\n" % (bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2])
						size += 1

						if size >= bl_conf ["find_maxres"][0]:
							break

				if size:
					bl_reply (user, (bl_lang [30] + "\r\n\r\n%s") % (data [9:], out))
				else:
					bl_reply (user, bl_lang [31] % data [9:])
			else:
				lowdata = data [9:].lower ()

				for pos in range (len (bl_item)):
					for item in bl_item [pos]:
						if lowdata in item [2].lower ():
							out += " %s - %s : %s\r\n" % (bl_inttoaddr (item [0]), bl_inttoaddr (item [1]), item [2])
							size += 1

							if size >= bl_conf ["find_maxres"][0]:
								break

					if size >= bl_conf ["find_maxres"][0]:
						break

				if size:
					bl_reply (user, (bl_lang [32] + "\r\n\r\n%s") % (data [9:], out))
				else:
					bl_reply (user, bl_lang [33] % data [9:])

			return 0

		if data [4:10] == "listre":
			out = bl_reload ()

			if len (out):
				out = bl_lang [143] + ":\r\n\r\n" + out
			else:
				out = bl_lang [34]

			bl_reply (user, out)
			return 0

		if data [4:7] == "del":
			pars = re.findall ("^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})[\\- ]*(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?$", data [8:])

			if not pars or not pars [0][0]:
				bl_reply (user, bl_lang [29] % ("del <" + bl_lang [89] + ">-[" + bl_lang [90] + "]"))
				return 0

			if not bl_validaddr (pars [0][0]):
				bl_reply (user, bl_lang [60] % pars [0][0])
				return 0

			if pars [0][1] and not bl_validaddr (pars [0][1]):
				bl_reply (user, bl_lang [61] % pars [0][1])
				return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])

			for pos in xrange (loaddr >> 24, (hiaddr >> 24) + 1):
				for id, item in enumerate (bl_item [pos]):
					if loaddr == item [0] and hiaddr == item [1]: # todo: exact match only for now
						bl_item [pos].pop (id)
						out = bl_lang [52] + ":\r\n"
						out += ("\r\n [*] " + bl_lang [39]) % item [2]
						out += ("\r\n [*] " + bl_lang [58]) % pars [0][0]
						out += ("\r\n [*] " + bl_lang [59] + "\r\n") % (pars [0][1] or pars [0][0])
						bl_reply (user, out)
						return 0

			bl_reply (user, bl_lang [122] % (pars [0][0], pars [0][1] or pars [0][0]))
			return 0

		if data [4:8] == "look":
			if not data [9:] or not bl_validaddr (data [9:]):
				bl_reply (user, bl_lang [29] % ("look <" + bl_lang [89] + ">"))
				return 0

			if not len (bl_conf ["prox_userip"][0]):
				bl_reply (user, bl_lang [117])
				return 0

			res = bl_httpreq (bl_defs ["google"] % (bl_conf ["prox_userip"][0], data [9:]))

			if not res [0]:
				bl_reply (user, res [1])
				return 0

			res = bl_lookup (res [1], data [9:])

			if res [0]:
				bl_reply (user, bl_lang [119] % (data [9:], res [1], vh.GetIPCC (data [9:])))
			else:
				if str (res [1]).isdigit ():
					bl_reply (user, bl_lang [118] % (data [9:], vh.GetIPCC (data [9:]), str (res [1]), str (bl_conf ["prox_match"][0])))
				else:
					bl_reply (user, res [1])

			return 0

		if data [4:11] == "listall":
			if not bl_list:
				out = bl_lang [34]
			else:
				out = bl_lang [35] + ":\r\n"

				for id, item in enumerate (bl_list):
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [37]) % item [0]
					out += ("\r\n [*] " + bl_lang [38]) % item [1]
					out += ("\r\n [*] " + bl_lang [39]) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else (bl_lang [42] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (item [5] + (item [3] * 60)))) if item [3] == 1 else (bl_lang [43] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (item [5] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else bl_lang [42] % item [3] if item [3] == 1 else bl_lang [43] % item [3])

					out += ("\r\n [*] " + bl_lang [44] + "\r\n") % (bl_lang [45] if not item [4] else bl_lang [46])

			bl_reply (user, out)
			return 0

		if data [4:11] == "listadd":
			pars = re.findall ("^(\\S+)[ ]+(\\S+)[ ]+\"(.+)\"[ ]*(\\d+)?$", data [12:])

			if not pars or not pars [0][0] or not pars [0][1] or not pars [0][2]:
				bl_reply (user, bl_lang [29] % ("listadd <" + bl_lang [92] + "> <" + bl_lang [93] + "> <\"" + bl_lang [91] + "\"> [" + bl_lang [94] + "]"))
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
				bl_reply (user, bl_lang [47] % ", ".join (types))
				return 0

			update = 0

			if pars [0][3].isdigit ():
				update = int (pars [0][3])

			if update < 0 or update > 10800:
				bl_reply (user, bl_lang [48] % (str (0), str (10800)))
				return 0

			for id, item in enumerate (bl_list):
				if item [0].lower () == pars [0][0].lower ():
					out = bl_lang [49] + ":\r\n"
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [37]) % item [0]
					out += ("\r\n [*] " + bl_lang [38]) % item [1]
					out += ("\r\n [*] " + bl_lang [39]) % item [2]

					if not item [4]:
						out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else (bl_lang [42] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (item [5] + (item [3] * 60)))) if item [3] == 1 else (bl_lang [43] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (item [5] + (item [3] * 60)))))
					else:
						out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else bl_lang [42] % item [3] if item [3] == 1 else bl_lang [43] % item [3])

					out += ("\r\n [*] " + bl_lang [44] + "\r\n") % (bl_lang [45] if not item [4] else bl_lang [46])
					bl_reply (user, out)
					return 0

			bl_list.append ([pars [0][0], pars [0][1], pars [0][2], update, 0, time.time () if update else 0])
			vh.SQL ("insert into `py_bl_list` (`list`, `type`, `title`, `update`) values ('%s', '%s', '%s', %s)" % (bl_repsql (pars [0][0]), bl_repsql (pars [0][1]), bl_repsql (pars [0][2]), str (update)))
			out = bl_lang [50] + ":\r\n"
			out += ("\r\n [*] " + bl_lang [36]) % str (len (bl_list) - 1)
			out += ("\r\n [*] " + bl_lang [37]) % pars [0][0]
			out += ("\r\n [*] " + bl_lang [38]) % pars [0][1]
			out += ("\r\n [*] " + bl_lang [39]) % pars [0][2]
			out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not update else (bl_lang [42] + " | %s") % (str (update), time.strftime ("%d/%m %H:%M", time.gmtime (time.time () + (update * 60)))) if update == 1 else (bl_lang [43] + " | %s") % (str (update), time.strftime ("%d/%m %H:%M", time.gmtime (time.time () + (update * 60)))))
			out += ("\r\n [*] " + bl_lang [44]) % bl_lang [45]
			out += ("\r\n [*] " + bl_lang [51] + "\r\n") % bl_import (pars [0][0], pars [0][1], pars [0][2])
			bl_reply (user, out)
			return 0

		if data [4:11] == "listdel":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_lang [29] % ("listdel <" + bl_lang [88] + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list.pop (id)
				vh.SQL ("delete from `py_bl_list` where `list` = '%s'" % bl_repsql (item [0]))
				out = bl_lang [52] + ":\r\n"
				out += ("\r\n [*] " + bl_lang [36]) % str (id)
				out += ("\r\n [*] " + bl_lang [37]) % item [0]
				out += ("\r\n [*] " + bl_lang [38]) % item [1]
				out += ("\r\n [*] " + bl_lang [39]) % item [2]
				out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else ((bl_lang [42] % item [3]) if item [3] == 1 else (bl_lang [43] % item [3])))
				out += ("\r\n [*] " + bl_lang [44] + "\r\n") % (bl_lang [45] if not item [4] else bl_lang [46])
				bl_reply (user, out)
			else:
				bl_reply (user, bl_lang [53] % str (id))

			return 0

		if data [4:11] == "listoff":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_lang [29] % ("listoff <" + bl_lang [88] + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if not item [4]:
					bl_list [id][4], bl_list [id][5] = 1, 0
					vh.SQL ("update `py_bl_list` set `off` = 1 where `list` = '%s'" % bl_repsql (item [0]))
					out = bl_lang [54] + ":\r\n"
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [37]) % item [0]
					out += ("\r\n [*] " + bl_lang [38]) % item [1]
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else ((bl_lang [42] % item [3]) if item [3] == 1 else (bl_lang [43] % item [3])))
					out += ("\r\n [*] " + bl_lang [44] + "\r\n") % bl_lang [46]
					bl_reply (user, out)
				else:
					bl_list [id][4] = 0
					vh.SQL ("update `py_bl_list` set `off` = 0 where `list` = '%s'" % bl_repsql (item [0]))

					if item [3]:
						bl_list [id][5] = time.time ()

					out = bl_lang [55] + ":\r\n"
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [37]) % item [0]
					out += ("\r\n [*] " + bl_lang [38]) % item [1]
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else (bl_lang [42] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (time.time () + (item [3] * 60)))) if item [3] == 1 else (bl_lang [43] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (time.time () + (item [3] * 60)))))
					out += ("\r\n [*] " + bl_lang [44]) % bl_lang [45]
					out += ("\r\n [*] " + bl_lang [51] + "\r\n") % bl_import (item [0], item [1], item [2])
					bl_reply (user, out)
			else:
				bl_reply (user, bl_lang [53] % str (id))

			return 0

		if data [4:11] == "listget":
			if data [12:].isdigit ():
				id = int (data [12:])
			else:
				bl_reply (user, bl_lang [29] % ("listget <" + bl_lang [88] + ">"))
				return 0

			if id >= 0 and bl_list and len (bl_list) - 1 >= id:
				item = bl_list [id]

				if not item [4]:
					if item [3]:
						bl_list [id][5] = time.time ()

					out = bl_lang [104] + ":\r\n"
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [37]) % item [0]
					out += ("\r\n [*] " + bl_lang [38]) % item [1]
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [40]) % (bl_lang [41] if not item [3] else (bl_lang [42] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (time.time () + (item [3] * 60)))) if item [3] == 1 else (bl_lang [43] + " | %s") % (item [3], time.strftime ("%d/%m %H:%M", time.gmtime (time.time () + (item [3] * 60)))))
					out += ("\r\n [*] " + bl_lang [44]) % bl_lang [45]
					out += ("\r\n [*] " + bl_lang [51] + "\r\n") % bl_import (item [0], item [1], item [2])
					bl_reply (user, out)
				else:
					bl_reply (user, bl_lang [103] % str (id))
			else:
				bl_reply (user, bl_lang [53] % str (id))

			return 0

		if data [4:9] == "myall":
			if not bl_myli:
				out = bl_lang [140]
			else:
				out = bl_lang [11] + ":\r\n"

				for id, item in enumerate (bl_myli):
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [58]) % bl_inttoaddr (item [0])
					out += ("\r\n [*] " + bl_lang [59] + "\r\n") % bl_inttoaddr (item [1])

			bl_reply (user, out)
			return 0

		if data [4:9] == "myadd":
			pars = re.findall ("^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})[\\- ]*(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?[ ]*(.*)$", data [10:])

			if not pars or not pars [0][0]:
				bl_reply (user, bl_lang [29] % ("myadd <" + bl_lang [89] + ">-[" + bl_lang [90] + "] [" + bl_lang [91] + "]"))
				return 0

			if not bl_validaddr (pars [0][0]):
				bl_reply (user, bl_lang [60] % pars [0][0])
				return 0

			if pars [0][1] and not bl_validaddr (pars [0][1]):
				bl_reply (user, bl_lang [61] % pars [0][1])
				return 0

			for id, item in enumerate (bl_myli):
				if item [0] == bl_addrtoint (pars [0][0]) and item [1] == bl_addrtoint (pars [0][1] or pars [0][0]):
					out = bl_lang [49] + ":\r\n"
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [58]) % pars [0][0]
					out += ("\r\n [*] " + bl_lang [59] + "\r\n") % (pars [0][1] or pars [0][0])
					bl_reply (user, out)
					return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])
			bl_myli.append ([loaddr, hiaddr, pars [0][2] or bl_lang [142]])
			vh.SQL ("insert ignore into `py_bl_myli` (`loaddr`, `hiaddr`, `title`) values (%s, %s, %s)" % (str (loaddr), str (hiaddr), ("'" + bl_repsql (pars [0][2]) + "'" if pars [0][2] else "null")))
			out = bl_lang [50] + ":\r\n"
			out += ("\r\n [*] " + bl_lang [36]) % str (len (bl_myli) - 1)
			out += ("\r\n [*] " + bl_lang [39]) % (pars [0][2] or bl_lang [142])
			out += ("\r\n [*] " + bl_lang [58]) % pars [0][0]
			out += ("\r\n [*] " + bl_lang [59] + "\r\n") % (pars [0][1] or pars [0][0])
			bl_reply (user, out)
			return 0

		if data [4:9] == "mydel":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_lang [29] % ("mydel <" + bl_lang [88] + ">"))
				return 0

			if id >= 0 and bl_myli and len (bl_myli) - 1 >= id:
				item, stop = bl_myli.pop (id), False
				vh.SQL ("delete from `py_bl_myli` where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))
				out = bl_lang [52] + ":\r\n"
				out += ("\r\n [*] " + bl_lang [36]) % str (id)
				out += ("\r\n [*] " + bl_lang [39]) % item [2]
				out += ("\r\n [*] " + bl_lang [58]) % bl_inttoaddr (item [0])
				out += ("\r\n [*] " + bl_lang [59] + "\r\n") % bl_inttoaddr (item [1])
				bl_reply (user, out)
			else:
				bl_reply (user, bl_lang [53] % str (id))

			return 0

		if data [4:9] == "exall":
			if not bl_exli:
				out = bl_lang [56]
			else:
				out = bl_lang [57] + ":\r\n"

				for id, item in enumerate (bl_exli):
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [58]) % bl_inttoaddr (item [0])
					out += ("\r\n [*] " + bl_lang [59] + "\r\n") % bl_inttoaddr (item [1])

			bl_reply (user, out)
			return 0

		if data [4:9] == "exadd":
			pars = re.findall ("^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})[\\- ]*(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})?[ ]*(.*)$", data [10:])

			if not pars or not pars [0][0]:
				bl_reply (user, bl_lang [29] % ("exadd <" + bl_lang [89] + ">-[" + bl_lang [90] + "] [" + bl_lang [91] + "]"))
				return 0

			if not bl_validaddr (pars [0][0]):
				bl_reply (user, bl_lang [60] % pars [0][0])
				return 0

			if pars [0][1] and not bl_validaddr (pars [0][1]):
				bl_reply (user, bl_lang [61] % pars [0][1])
				return 0

			for id, item in enumerate (bl_exli):
				if item [0] == bl_addrtoint (pars [0][0]) and item [1] == bl_addrtoint (pars [0][1] or pars [0][0]):
					out = bl_lang [49] + ":\r\n"
					out += ("\r\n [*] " + bl_lang [36]) % str (id)
					out += ("\r\n [*] " + bl_lang [39]) % item [2]
					out += ("\r\n [*] " + bl_lang [58]) % pars [0][0]
					out += ("\r\n [*] " + bl_lang [59] + "\r\n") % (pars [0][1] or pars [0][0])
					bl_reply (user, out)
					return 0

			loaddr = bl_addrtoint (pars [0][0])
			hiaddr = bl_addrtoint (pars [0][1] or pars [0][0])
			bl_exli.append ([loaddr, hiaddr, pars [0][2] or bl_lang [1]])
			vh.SQL ("insert ignore into `py_bl_exli` (`loaddr`, `hiaddr`, `title`) values (%s, %s, %s)" % (str (loaddr), str (hiaddr), ("'" + bl_repsql (pars [0][2]) + "'" if pars [0][2] else "null")))
			out = bl_lang [50] + ":\r\n"
			out += ("\r\n [*] " + bl_lang [36]) % str (len (bl_exli) - 1)
			out += ("\r\n [*] " + bl_lang [39]) % (pars [0][2] or bl_lang [1])
			out += ("\r\n [*] " + bl_lang [58]) % pars [0][0]
			out += ("\r\n [*] " + bl_lang [59] + "\r\n") % (pars [0][1] or pars [0][0])
			bl_reply (user, out)
			return 0

		if data [4:9] == "exdel":
			if data [10:].isdigit ():
				id = int (data [10:])
			else:
				bl_reply (user, bl_lang [29] % ("exdel <" + bl_lang [88] + ">"))
				return 0

			if id >= 0 and bl_exli and len (bl_exli) - 1 >= id:
				item, stop = bl_exli.pop (id), False
				vh.SQL ("delete from `py_bl_exli` where `loaddr` = %s and `hiaddr` = %s" % (str (item [0]), str (item [1])))

				for pos in range (len (bl_prox)):
					for pid, prox in enumerate (bl_prox [pos]):
						intaddr = bl_addrtoint (prox [0])

						if intaddr >= item [0] and intaddr <= item [1]:
							bl_item [intaddr >> 24].append ([intaddr, intaddr, bl_lang [126]]) # todo: also add to mysql table when we have one
							bl_prox [pos].pop (pid)
							stop = True
							break

					if stop:
						break

				out = bl_lang [52] + ":\r\n"
				out += ("\r\n [*] " + bl_lang [36]) % str (id)
				out += ("\r\n [*] " + bl_lang [39]) % item [2]
				out += ("\r\n [*] " + bl_lang [58]) % bl_inttoaddr (item [0])
				out += ("\r\n [*] " + bl_lang [59] + "\r\n") % bl_inttoaddr (item [1])
				bl_reply (user, out)
			else:
				bl_reply (user, bl_lang [53] % str (id))

			return 0

		if data [4:8] == "conf":
			out = bl_lang [62] + ":\r\n"

			for name, item in sorted (bl_conf.iteritems ()):
				out += ("\r\n [*] " + bl_lang [63]) % name
				out += ("\r\n [*] " + bl_lang [38]) % item [1]
				out += ("\r\n [*] " + bl_lang [64]) % (item [2], item [3])
				out += ("\r\n [*] " + bl_lang [65]) % item [0]
				out += ("\r\n [*] " + bl_lang [167] + "\r\n") % bl_lang [item [4]]

			bl_reply (user, out)
			return 0

		if data [4:7] == "set":
			pars = re.findall ("^(\\S+)[ ]*(.*)$", data [8:])

			if pars and pars [0][0]:
				out = bl_lang [66] + ":\r\n"
				out += ("\r\n [*] " + bl_lang [63]) % pars [0][0]
				out += ("\r\n [*] " + bl_lang [38]) % (bl_conf [pars [0][0]][1] if pars [0][0] in bl_conf else bl_lang [95])
				out += ("\r\n [*] " + bl_lang [64]) % ((bl_conf [pars [0][0]][2] if pars [0][0] in bl_conf else 0), (bl_conf [pars [0][0]][3] if pars [0][0] in bl_conf else 0))
				out += ("\r\n [*] " + bl_lang [67]) % (bl_lang [95] if bl_getconf (pars [0][0]) == None else bl_getconf (pars [0][0]))
				out += ("\r\n [*] " + bl_lang [68]) % pars [0][1]
				out += ("\r\n [*] " + bl_lang [51]) % bl_setconf (pars [0][0], pars [0][1])
				out += ("\r\n [*] " + bl_lang [167] + "\r\n") % (bl_lang [bl_conf [pars [0][0]][4]] if pars [0][0] in bl_conf else bl_lang [17])
			else:
				out = bl_lang [29] % ("set <" + bl_lang [87] + "> [" + bl_lang [86] + "]")

			bl_reply (user, out)
			return 0

		if data [4:8] == "lang":
			out = bl_lang [98] + ":\r\n\r\n"

			for id, lang in sorted (bl_lang.iteritems ()):
				out += (" %s = %s\r\n") % (str (id), lang)

			bl_reply (user, out)
			return 0

		if data [4:9] == "trans":
			pars = re.findall ("^(\\S+)[ ]*(.*)$", data [10:])

			if not pars or not pars [0][0] or not pars [0][1]:
				bl_reply (user, bl_lang [29] % ("trans <" + bl_lang [88] + "> <" + bl_lang [86] + ">"))
				return 0

			if pars [0][0].isdigit ():
				id = int (pars [0][0])
			else:
				bl_reply (user, bl_lang [29] % ("trans <" + bl_lang [88] + "> <" + bl_lang [86] + ">"))
				return 0

			if id >= 0 and len (bl_lang) - 1 >= id:
				if pars [0][1].count ("%s") == bl_lang [id].count ("%s"):
					vh.SQL ("update `py_bl_lang` set `value` = '%s' where `id` = %s" % (bl_repsql (pars [0][1]), str (id)))
					old, bl_lang [id] = bl_lang [id], pars [0][1]
					out = (bl_lang [99] + "\r\n") % str (id)
					out += ("\r\n [*] " + bl_lang [67]) % old
					out += ("\r\n [*] " + bl_lang [68] + "\r\n") % pars [0][1]
					bl_reply (user, out)
				else:
					out = (bl_lang [100] + "\r\n") % str (id)
					out += ("\r\n [*] " + bl_lang [67]) % bl_lang [id]
					out += ("\r\n [*] " + bl_lang [68] + "\r\n") % pars [0][1]
					bl_reply (user, out)
			else:
				bl_reply (user, bl_lang [53] % str (id))

			return 0

		out = bl_lang [73] + ":\r\n\r\n"

		out += " stat\t\t\t\t\t- " + bl_lang [74] + "\r\n"
		out += " prox\t\t\t\t\t- " + bl_lang [127] + "\r\n"
		out += " feed\t\t\t\t\t- " + bl_lang [85] + "\r\n\r\n"

		out += " find <" + bl_lang [87] + ">\t\t\t\t- " + bl_lang [75] + "\r\n"
		out += " del <" + bl_lang [89] + ">-[" + bl_lang [90] + "]\t\t\t- " + bl_lang [121] + "\r\n\r\n"

		out += " look <" + bl_lang [89] + ">\t\t\t\t- " + bl_lang [116] + "\r\n\r\n"

		out += " listall\t\t\t\t\t- " + bl_lang [76] + "\r\n"
		out += " listadd <" + bl_lang [92] + "> <" + bl_lang [93] + "> <\"" + bl_lang [91] + "\"> [" + bl_lang [94] + "]\t- " + bl_lang [77] + "\r\n"
		out += " listoff <" + bl_lang [88] + ">\t\t\t\t- " + bl_lang [78] + "\r\n"
		out += " listget <" + bl_lang [88] + ">\t\t\t\t- " + bl_lang [102] + "\r\n"
		out += " listdel <" + bl_lang [88] + ">\t\t\t\t- " + bl_lang [79] + "\r\n"
		out += " listre\t\t\t\t\t- " + bl_lang [141] + "\r\n\r\n"

		out += " myall\t\t\t\t\t- " + bl_lang [144] + "\r\n"
		out += " myadd <" + bl_lang [89] + ">-[" + bl_lang [90] + "] [" + bl_lang [91] + "]\t\t- " + bl_lang [145] + "\r\n"
		out += " mydel <" + bl_lang [88] + ">\t\t\t\t- " + bl_lang [146] + "\r\n\r\n"

		out += " exall\t\t\t\t\t- " + bl_lang [80] + "\r\n"
		out += " exadd <" + bl_lang [89] + ">-[" + bl_lang [90] + "] [" + bl_lang [91] + "]\t\t\t- " + bl_lang [81] + "\r\n"
		out += " exdel <" + bl_lang [88] + ">\t\t\t\t- " + bl_lang [82] + "\r\n\r\n"

		out += " conf\t\t\t\t\t- " + bl_lang [83] + "\r\n"
		out += " set <" + bl_lang [87] + "> [" + bl_lang [86] + "]\t\t\t\t- " + bl_lang [84] + "\r\n\r\n"

		out += " lang\t\t\t\t\t- " + bl_lang [97] + "\r\n"
		out += " trans <" + bl_lang [88] + "> <" + bl_lang [86] + ">\t\t\t- " + bl_lang [96] + "\r\n"

		bl_reply (user, out)
		return 0

	return 1

def OnTimer (msec):
	global bl_defs, bl_lang, bl_conf, bl_stat, bl_list, bl_item, bl_prox, bl_feed
	now = time.time ()

	if now - bl_stat ["update"] >= 60:
		bl_stat ["update"], mins = now, (bl_conf ["time_feed"][0] * 60)
		bl_feed = [item for item in bl_feed if now - item [1] < mins]

		for id, item in enumerate (bl_list):
			if not item [4] and item [3] and now - item [5] >= item [3] * 60:
				bl_list [id][5], out = now, bl_import (item [0], item [1], item [2], True)

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
							bl_notify (bl_lang [120] % (item [0], vh.GetIPCC (item [0]), bl_lang [125]))
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
										bl_notify (bl_lang [119] % (item [0], res [1], code))
										intaddr = bl_addrtoint (item [0])
										keep = True

										if bl_excheck (item [0], intaddr, code, bl_lang [126], False):
											for nick in item [1]:
												bl_stat ["except"] += 1

											bl_prox [pos][id][2] = 3
										else:
											for nick in item [1]:
												vh.CloseConnection (nick)
												bl_stat ["block"] += 1

											bl_prox [pos][id][2] = 2
											bl_item [intaddr >> 24].append ([intaddr, intaddr, bl_lang [126]]) # todo: also add to mysql table when we have one
									else:
										if str (res [1]).isdigit ():
											keep = True
											bl_prox [pos][id][2] = 3

											if (bl_conf ["prox_debug"][0] and int (res [1])) or bl_conf ["prox_debug"][0] > 1:
												bl_notify (bl_lang [118] % (item [0], code, str (res [1]), str (bl_conf ["prox_match"][0])))
										elif not bl_conf ["prox_nofail"][0]:
											bl_notify (bl_lang [120] % (item [0], code, res [1]))
								else:
									bl_notify (bl_lang [120] % (item [0], code, bl_lang [7]))
							else:
								bl_notify (bl_lang [120] % (item [0], code, bl_lang [10]))

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
					if now - item [3] >= 60:
						dels.insert (0, [pos, id])
				#elif item [2] == 3:
					#pass

		for item in dels:
			bl_prox [item [0]].pop (item [1])

bl_main ()

# end of file
