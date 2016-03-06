#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Example multi-language script.
# Created in 2016 by Frog (frogged on GitHub), the_frog at wp dot pl
# This file is in public domain. Do whatever you want at yuor own risk.
# Get new version at https://github.com/Verlihub/python/tree/master/simple_i18n
# This copy is version 1.1.0 from 2016-03-06
#
# Nothing stops you from using gettext, but it might be easier to simply store
# all translated strings in the database (or anywhere else). This script shows
# you how it can be done in a manner that resembles gettext (noticed the _?).
# A special DB table will be created and you can dump and replace with your
# strings in any language you choose. You just have to keep the same IDs.
#
# When developing scripts the strings can soon go out od sync, which would
# cause the script to raise exceptions and not work properly. To mitigate that
# run translation_check.py over your script, available here:
# https://github.com/Verlihub/python/tree/master/simple_i18n
#
# In the case of this script, run:
# python translation_check.py translation_example.py english_strings _
# and make sure that there are no undefined strings reported.


from __future__ import print_function
import sys
import vh

# This script depends on the translation_helper.py script, so you need to get it as well.
# If we put the module in the scripts directory, we need to add the directory to the path:
sys.path.append(vh.basedir + "/scripts")
from translation_helper import update_translation_strings


my_name = "Translation Example"


# Put all strings you wish to translate here. The number correspond with the ids in the database.
# Only use %s to mark placeholders and never put an "s" after "%%" (that would confuse the counting).

english_strings = {
    1: "Script %s is ready.",
    2: "Sorry, but I speak only %s.",
    3: "OK, English now!",
    4: "I'm shutting down...",
}


# We provide german_string for this example. Normally you'd put the translation strings
# in the database or in a separate file.

german_strings = {
    1: "Script %s ist fertig.",
    2: "Es tut mir Leid, aber ich spreche nur %s.",
    3: "Jawohl, jetzt Deutsch!",
    4: "Ich schalte aus...",
}

# Replace this with your script's unique table name:
translation_db_table = "translation_example_py_strings"

# Replace this with path to your script's translation strings file:
translation_file = vh.basedir + "/scripts/my_translations.txt"


# This would only prepare the English strings for use with _[text]:
# _ = update_translation_strings(english_strings)

# This loads the default strings from the database in whatever language is stored there:
_ = update_translation_strings(english_strings, db_table=translation_db_table)

# This will print in English or the language in the database if the table already existed:
vh.classmc(_("Script %s is ready.") % my_name, 3, 10)


def OnOperatorCommand(nick, data):
    global _   # has to be global, because we assign it here

    if data[1:].startswith("tr_example "):
        lang = data[1 + len("tr_example "):]

        if lang == "en":
            # Reset translations to default English:
            _ = update_translation_strings(english_strings)
            vh.usermc(_("OK, English now!"), nick)

        elif lang == "de":
            # Load German from our local dictionary, but copy it first so it is not overwritten.
            # (Missing or bad strings would be replaced by English versions, and extra strings would be removed.)
            # If you don't care about german_strings being modified, you can leave out the ".copy()".
            #
            _ = update_translation_strings(english_strings, german_strings.copy(), use_translated=True)
            vh.usermc(_("OK, English now!"), nick)  # This will show up in German!

        elif lang == "database":
            # Load whatever language is used in the strings stored in the database:
            _ = update_translation_strings(english_strings, db_table=translation_db_table)
            vh.usermc(_("OK, English now!"), nick)  # Anything is possible here

        elif lang == "file":
            # Load whatever language is used in the translation file:
            _ = update_translation_strings(english_strings, filename=translation_file, create=False)
            vh.usermc(_("OK, English now!"), nick)  # Anything is possible here

        else:
            vh.usermc(_("Sorry, but I speak only %s.") % "en, de, database, file", nick)

        return 0


def UnLoad():
    vh.classmc(_("I'm shutting down..."), 3, 10)

