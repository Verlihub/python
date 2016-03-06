Simple Internationalization
===========================

Internationalization (i18n) is a broad subject, but at the very least you would want to be able to make the script you installed print messages in the language of your choice. The preferable way to do this is the one that doesn't require you to change the script when you add a new language. Gettext is the obvious choice, but it requires some work: extracting strings, compiling POT files, finding them. Therefore a simpler solution is proposed here.

The solution involves creating a dictionary where all strings that are to be translated are given their unique numbers and using a database table to store those strings with their IDs (if they aren't already present in the database) and retrieve them. Then someone else can dump the database table, replace the strings with their translations, and import the new table to the database.

Since many scripts would need similar functionality to handle the translations, a special Python module (translation_helper.py) was written to ease the task. It checks that the translated format strings use the same conversion specifiers (%s, %d, %(name)s and similar), so you don't have to worry about script crashing because of that. If the strings don't match, the English default will be used. In your script you will need to import the `update_translation_strings` functions from the `translation_helper` module, and define the untranslated strings in a dictionary, like this:

    from translation_helper import update_translation_strings
    
    english_strings = {
        0: "",  # We do not use the zeroth string, so that text file approach also works
        1: "Script %s is ready.",
        2: "Sorry, but I speak only %s.",
        3: "OK, English now!",
        4: "I'm shutting down...",
    }

Then, to load the translated strings from the database table (which will be created, if it didn't exist before, and populated), and use them, all you need to do is write this:

    #.py
    _ = update_translation_strings(english_strings, db_table="my_translations")
    
    print _("Script %s is ready.") % "test.py"
    print _("I'm shutting down...")

After running this, if the translation table did not exist, it will be created and look like this:

    mysql> select * from my_translations;
    +----+-----------------------------+
    | id | value                       |
    +----+-----------------------------+
    |  1 | Script %s is ready.         |
    |  2 | Sorry, but I speak only %s. |
    |  3 | OK, English now!            |
    |  4 | I'm shutting down...        |
    +----+-----------------------------+
    4 rows in set (0.00 sec)

Now, if you edit those values and run the script again, the strings from this database table will be used — but only if the type and number of the `%` conversion specifications match.

Or, instead of using the database, you could load the strings from a text file, where the ID is the line number (and that is why we left the zeroth string unused!). Let's say the file is called my_translations.txt and looks like this:

    Script %s ist fertig.
    Es tut mir Leid, \naber ich spreche nur %s.
    Jawohl, jetzt Deutsch!
    Ich schalte aus...

You could load it and use like this:

```py
    with open("my_translations.txt") as f:
        data = [x.replace('\\n', '\n').replace('\\r', '\r') for x in f.readlines()]
        translations = dict([(i+1, x) for i, x in enumerate(data)])

    _ = update_translation_strings(english_strings, translations, use_translated=True)
```

and afterwards you can print the strings in the same way as you would with strings loaded from the database. Please note that there is a `\n` in the second line in the translations file to denote a newline, because we obviously could not split the string into two lines. Therefore we had to use `replace('\\n', '\n')` to convert all escaped newlines into real newlines (and we did the same for carriage return, `\r`).

As the script grows it can be hard to track if all the `_("string")` in the file match the strings present in the translation dictionary (`english_strings` in this example). The translation_check.py script can help you with that. For example, to check the translation_example.py script, you would use the command:

    python translation_check.py translation_example.py english_strings _

That's about it. Unfortunately pluralization is not supported, so you will have to bend the strings to make them look decent. For example instead of writing "There are %d files available", which would look strange if only one file were available, you could write "The number of available files is %d". If you need pluralization, you'll have to use Gettext instead (or reinvent it).


> Document last updated on 2016-03-06

