# coding: latin-1

# PasteBot 0.0.2.1
# © 2016 RoLex

import vh, urllib, urllib2

pb_defs = {
	"paste": "http://paste.ubuntu.com/",
	"poster": "poster",
	"syntax": "syntax",
	"content": "content",
	"text": "text",
	"agent": "PasteBot/0.0.2.1",
	"timeout": 5,
	"command": "paste",
	"shortcut": "p",
	"class": 3,
	"rights": "You have no rights to do this.",
	"empty": "Here you go: %s",
	"failed": "Failed to paste, please do it yourself: %s"
}

def pb_paste (nick, data):
	global pb_defs

	try:
		file = urllib2.urlopen (urllib2.Request (pb_defs ["paste"], urllib.urlencode ({pb_defs ["poster"]: pb_unicode (nick), pb_defs ["syntax"]: pb_defs ["text"], pb_defs ["content"]: pb_unicode (pb_nmdc (data, True))}), {"User-agent": pb_defs ["agent"]}), None, pb_defs ["timeout"])
	except:
		return None

	if not file:
		return None

	try:
		url = file.geturl ()
	except:
		pass

	file.close ()

	if not url:
		return None

	return url

def pb_unicode (data, bad = "cp1252"):
	enc = vh.GetConfig (vh.config_name, "hub_encoding", bad)

	if enc and len (enc):
		enc = enc.lower ()
	else:
		enc = bad

	try:
		conv = data.decode (enc, "ignore").encode ("utf-8", "ignore")
	except:
		conv = data

	return conv

def pb_nmdc (data, out = False):
	if out:
		return data.replace ("&#124;", "|").replace ("&#36;", "$")
	else:
		return data.replace ("|", "&#124;").replace ("$", "&#36;")

def pb_notify (nick, data, oc):
	if oc:
		vh.SendToOpChat (pb_nmdc (data), nick)
		vh.ScriptCommand ("opchat_to_all", "<%s> %s" % (nick, data))
	else:
		vh.mc (pb_nmdc (data), nick)
		vh.ScriptCommand ("chat_to_all", "<%s> %s" % (nick, data))

def pb_reply (nick, data, oc):
	if oc:
		vh.pm (pb_nmdc (data), nick, vh.opchatname, vh.botname)
	else:
		vh.usermc (pb_nmdc (data), nick)

def pb_command (nick, data, oc):
	global pb_defs

	if data [1:len (pb_defs ["shortcut"]) + 1] == pb_defs ["shortcut"] and (data [len (pb_defs ["shortcut"]) + 1:len (pb_defs ["shortcut"]) + 2] == " " or len (data) == len (pb_defs ["shortcut"]) + 1):
		par = data [len (pb_defs ["shortcut"]) + 2:]
	elif data [1:len (pb_defs ["command"]) + 1] == pb_defs ["command"]:
		par = data [len (pb_defs ["command"]) + 2:]
	else:
		return 1

	if vh.GetUserClass (nick) < pb_defs ["class"]:
		pb_reply (nick, pb_defs ["rights"], oc)
		return 0

	if not len (par):
		pb_reply (nick, pb_defs ["empty"] % pb_defs ["paste"], oc)
		return 0

	url = pb_paste (nick, par)

	if not url:
		pb_reply (nick, pb_defs ["failed"] % pb_defs ["paste"], oc)
		return 0

	pb_notify (nick, url, oc)
	return 0

def OnOperatorCommand (nick, data):
	return pb_command (nick, data, False)

def OnParsedMsgPM (nick, data, user):
	if len (vh.opchatname) and user == vh.opchatname:
		return pb_command (nick, data, True)

	return 1

# end of file
