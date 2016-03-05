#!/usr/bin/python
import ast
import _ast
import sys

program_info = """
Python script translation strings checker
Copyright (C) 2016 Frog (frogged on GitHub), the_frog at wp dot pl
Distributed under the Boost Software License, Version 1.0.
See the license terms at http://www.boost.org/LICENSE_1_0.txt

Usage: %(app_name)s <filename> <storage_dict> <retrieval_dict> <is_dict=0>

This program checks for missing or redundant tranlation strings in script
<filename> where instead of gettext you have a dict of English strings
indexed by numbers (<storage_dict>), a copy of that dictionary with those
strings translated, and a <retrieval_dict> mapping strings from the first
to the second dictionary. For rhw program to work, <storage_dict> must be
defined as a whole in one step, and <retrieval_dict> must always be used
using the form, retrieval_dict["string"].

Here is an example Python script, where <storage_dict> is called en_strings
and <retrieval_dict> is called _ (to immitate gettext):

    en_strings = {
        0: "This is script X, version %%s",
        1: "Hello and welcome!",
        2: "There was an error",
    }
    user_strings = en_strings.copy()
    # Now replace user_strings values with translations from another source,
    # for example a database table (id, string). This step isn't shown here.

    mapping = {}
    for key in en_strings:
        mapping[en_strings[key]] = user_strings[key]

    # Afterwards, we use the same strings from en_strings but using _.
    print mapping["This is script ABC, version %%s"] %% "1.2.3"
    print mapping["Hello and welcome!"]

    # Or you can define a gettext-like function and use it:
    def _(s): return mapping[s]
    print _("This is script ABC, version %%s") %% "1.2.3"
    print _("Hello and welcome!")

Notice that we made a mistake: X was changed to ABC. The script would crash.
Spotting such errors is the exactly the purpose of this program. It will show
you missing and redundant string together with their position in the script.

Set optional argument <is_dict> to 1 if instead of gettext_like function,
_("string"), you use a string-to-string dictionary, _["string"].
"""



class TranslationStringsChecker(object):
    def __init__(self, stored_dict_name, retrieved_dict_name="_", using_function=False):
        self.stored_dict_name = stored_dict_name
        self.retrieved_dict_name = retrieved_dict_name
        self.using_function = using_function
        self.clear()

    def clear(self):
        self.filename = "?"
        self.stored_raw = []
        self.retrieved_raw = []
        self.stored = {}
        self.retrieved = {}
        self.missing = set()
        self.redundant = set()

    def parse(self, source, filename="source"):
        self.clear()
        self.filename = filename
        data = ast.parse(source, filename)
        for a in ast.walk(data):
            if isinstance(a, _ast.Assign) and isinstance(a.targets[0], _ast.Name):
                name = a.targets[0].id
                if name == self.stored_dict_name:
                    if isinstance(a.value, _ast.Dict):
                        for x in a.value.values:
                            if isinstance(x, _ast.Str):
                                self.stored_raw.append((x.s, x.lineno, x.col_offset))
                            else:
                                print "Error in %s:%d:%d: nonstring dict value" % (
                                    self.filename, x.lineno, x.col_offset)

        if not self.using_function:
            for a in ast.walk(data):
                if isinstance(a, _ast.Subscript) and isinstance(a.value, _ast.Name):
                    name = a.value.id
                    if name == self.retrieved_dict_name:
                        if hasattr(a.slice, "value") and isinstance(a.slice.value, _ast.Str):
                            x = a.slice.value
                            self.retrieved_raw.append((x.s, x.lineno, x.col_offset))
        else:
            for a in ast.walk(data):
                if isinstance(a, _ast.Call) and isinstance(a.func, _ast.Name):
                    name = a.func.id
                    if name == self.retrieved_dict_name:
                        if len(a.args) == 1 and isinstance(a.args[0], _ast.Str):
                            x = a.args[0]
                            self.retrieved_raw.append((x.s, x.lineno, x.col_offset))
                        else:
                            print "Suspicious use of '%s' in %s:%d:%d" % (
                                self.retrieved_dict_name, self.filename, a.lineno, a.col_offset)

        for item in self.stored_raw:
            if item[0] in self.stored:
                self.stored[item[0]].append(item)
            else:
                self.stored[item[0]] = [item]

        for item in self.retrieved_raw:
            if item[0] in self.retrieved:
                self.retrieved[item[0]].append(item)
            else:
                self.retrieved[item[0]] = [item]

        s_set = set(self.stored.keys())
        r_set = set(self.retrieved.keys())
        self.missing = r_set - s_set
        self.redundant = s_set - r_set


    def print_stats(self):
        print "\nFound %s stored strings and %s retrieved strings in file %s" % (
                len(self.stored), len(self.retrieved), self.filename)
        print "%s strings are not defined and %s strings are defined but unused" % (
                len(self.missing), len(self.redundant))

        if self.missing:
            print "\nWARNING: Following strings are used but are not defined (program will crash!):"
            results = []
            for key in self.missing:
                for x in self.retrieved[key]:
                    results.append(x)

            for x in sorted(results, key=lambda a: a[1]):
                print "%-16s" % ("Line %4d:%d" % (x[1], x[2])), repr(x[0])

        if self.redundant:
            print "\nFollowing strings have translations but are not used:"
            results = []
            for key in self.redundant:
                for x in self.stored[key]:
                    results.append(x)

            for x in sorted(results, key=lambda a: a[1]):
                print "%-16s" % ("Line %4d:%d" % (x[1], x[2])), repr(x[0])

        print



# First test that the checker works:

src = """
data = { 1: "blah", 2: "test", 3: "qwerty", 4: "abc", 5: "another" }
data[6] = "extra"
x = _["blah"] + _["blah"] + _["blah"] + _["test"] + _["qwerty"]
print _["abc"], _["fubar"], _["crash"]
"""
checker = TranslationStringsChecker("data")
checker.parse(src, "test1")
# checker.print_stats()
assert(checker.missing == set(["fubar", "crash"]))
assert(checker.redundant == set(["another"]))



if __name__ == "__main__":
    if len(sys.argv) in [4, 5]:
        filename = sys.argv[1]
        stored_dict_name = sys.argv[2]
        retrieved_dict_name = sys.argv[3]
        using_function = True
        if len(sys.argv) == 5 and sys.argv[4] == "1":
            using_function = False
        with open(filename) as f:
            source = f.read()
            checker = TranslationStringsChecker(stored_dict_name, retrieved_dict_name, using_function)
            checker.parse(source, filename)
            checker.print_stats()
    else:
        print program_info % dict(app_name=sys.argv[0])
