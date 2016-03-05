#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Example multi-language script.
# Created in 2016 by Frog (frogged on GitHub), the_frog at wp dot pl
# This file is in public domain. Do whatever you want at yuor own risk.
#
# Nothing stops you from using gettext, but it might be easier to simply store
# all translated strings in the database (or anywhere else). This script shows
# you how it can be done in a manner that resembles gettext (noticed the _?).
# A special DB table will be created and you can dump and replace with your
# strings in any language you choose. You just have to keep the same IDs.
#
# When developing scripts the strings can soon go out od sync, which would
# cause the script to raise exceptions and not work properly. To mitigate that
# run translation_checke over your script, available here:
# https://github.com/Verlihub/python/blob/master/translation_check.py
#
# In the case of this script, run:
# python translation_check.py translation_example.py english_strings _
# and make sure that there are no undefined strings reported.


from __future__ import print_function
import sys
import vh

# If we put the module in the scripts directory, we need to add the directory to the path
sys.path.append(vh.basedir + "/scripts")
from translation_helper import update_translation_strings


my_name = "Translation Example"


# Put all strings you wish to translate here. The number correspond with the ids in the database.
# Only use %s to mark placeholders and never put an "s" after "%%" (that would confuse the counting).

english_strings = {
    0: "Script %s is ready.",
    1: "Sorry, but I speak only %s.",
    2: "OK, English now!",
    3: "I'm shutting down...",
}


# We provide german_string for this example. Normally you'd put the translation strings
# in the database or in a separate file.

german_strings = {
    0: "Script %s ist fertig.",
    1: "Es tut mir Leid, aber ich spreche nur %s.",
    2: "Jawohl, jetzt Deutsch!",
    3: "Ich schalte aus...",
}

# Replace this with your script's unique table name:
translation_db_table = "translation_example_py_strings"

translated_strings = {}
_ = {}

# This would only prepare the English strings for use with _[text]:
# update_translation_strings(english_strings, translated_strings, _)

# This loads the default strings from the database in whatever language is stored there:
update_translation_strings(english_strings, translated_strings, _, translation_db_table)

# This will print in English or the language in the database if the table already existed:
vh.classmc(_["Script %s is ready."] % my_name, 10, 10)


def OnOperatorCommand(nick, data):
    if data[1:].startswith("tr_example "):
        lang = data[1 + len("tr_example "):]

        if lang == "en":
            # Load English from our local dictionary (copy it first, so it's mpt overwritten):
            translated_strings = english_strings.copy()
            update_translation_strings(english_strings, translated_strings, _, None, True)
            vh.usermc(_["OK, English now!"], nick)

        elif lang == "de":
            # Load German from our local dictionary:
            translated_strings = german_strings.copy()
            update_translation_strings(english_strings, translated_strings, _, None, True)
            vh.usermc(_["OK, English now!"], nick)  # This will show up in German!

        elif lang == "xx":
            # Load whatever language is used in the strings stored in the database:
            translated_strings = german_strings.copy()
            update_translation_strings(english_strings, translated_strings, _, translation_db_table)
            vh.usermc(_["OK, English now!"], nick)  # Anything is possible here

        else:
            vh.usermc(_["Sorry, but I speak only %s."] % "en, de, xx", nick)

        return 0


def UnLoad():
    vh.classmc(_["I'm shutting down..."], 10, 10)

