#!/usr/bin/python
# -*- coding:utf-8 -*-
#
# Python string translation module
# Copyright (C) 2016 Frog (frogged on GitHub), the_frog at wp dot pl
# Distributed under the Boost Software License, Version 1.0.
# See the license terms at http://www.boost.org/LICENSE_1_0.txt
# Get this script at https://github.com/Verlihub/python/tree/master/simple_i18n
# This copy is version 1.2.0 from 2016-03-06
#
# This script was inspired by Rolex and his blacklist.py script
# available here: https://github.com/Verlihub/python/blob/master/blacklist.py
#
# This module allows for using simpler translation techniques than gettext
# but is missing an important gettext feature, namely pluralization.
# Use it if you want to store translation strings in a file or database.
# The database table will have two columns: integer id, and a string.
#
# When you prepare a translation, you keep the id and change the string.
# Make sure that the format strings are compatible (do_format_strings_match
# will help you with that). Incompatible string won't be loaded (the English
# version of them will be used) and you'll get an error on stderr to help you
# correct the mistake.
#
# This module does not require Verlihub, but without it you will have to supply
# your own version of SQL function inside a vh dict as a function argument.
#
# update_translation_strings is probably the only function you will need.
# Look at the translation_example.py script to see how you can use it:
# https://github.com/Verlihub/python/tree/master/simple_i18n


from __future__ import print_function
import sys

try:
    import vh
except:
    if __name__ != "__main__":
        print("Warning: VH module not found", file=sys.stderr)

    # vh module wasn't found so we create a dummy "module" with disabled SQL function
    class dummy_vh_module(object):
        def SQL(self, a, b=0): return (False, [])

    vh = dummy_vh_module()


def escape_sql(data):
    return data.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


class FormatStringError(Exception): pass
class FormatUnrecognized(FormatStringError): pass
class FormatMixedArgs(FormatStringError): pass
class FormatNotFinished(FormatStringError): pass
class TranslateError(FormatStringError): pass


format_types = "diouxXeEfFgGcrs"
format_flags = "#0- +"
format_length_mods = "hlL"
format_num = "0123456789"


def parse_format_string(string, full=False):
    """A parser for Python format strings."""
    report = []
    mapping = {}
    states = ['out', 'in', 'name', 'flag', 'width', 'in_width', 'prec', 'in_prec', 'mod', 'type']
    state = 'out'
    name_start = 0
    name = ""
    flags = "" # ignore
    width = "" # ignore, except when it is '*'
    precision = "" # ignore
    length_mod = "" # ignore
    format_type = ""
    named_args = 0
    positional_args = 0
    uses_width_from_arg = 0

    for i, c in enumerate(string):
        if state in ['out', 'in'] and c == '%':
            if state == 'out':
                state = 'in'
            elif state == 'in':
                state = 'out'  # got an escaped percent (%%)
            continue
        if state == 'in':
            if c == '(':
                state = 'name'
                name_start = i + 1
                continue
            else:
                state = 'flag'
        if state == 'name' and c == ')':
            name = string[name_start:i]
            named_args += 1
            state = 'flag'
            continue
        if state == 'flag':
            if c in format_flags:
                flags += c
                continue
            else:
                state = 'width'
        if state == 'width':
            if c == '*':
                uses_width_from_arg += 1
                positional_args += 1
                width = '*'
                state = 'prec'
                continue
            else:
                state = 'in_width'
        if state == 'in_width':
            if c in format_num:
                width += c
                continue
            else:
                state = 'prec'
        if state == 'prec':
            if c == '.':
                state = 'in_prec'
                continue
            else:
                state = 'mod'
        if state == 'in_prec':
            if c in format_num:
                precision += c
                continue
            else:
                state = 'mod'
        if state == 'mod':
            if c in format_length_mods:
                length_mod = c
                state = 'type'
                continue
            else:
                state = 'type'
        if state == 'type':
            if c in format_types:
                format_type = c.lower()
                compatibility = 'f'
                if format_type == 'c':
                    compatibility = "c"
                elif format_type in ['s', 'r']:
                    compatibility = 's'
                if not name:
                    positional_args += 1
                report.append(dict(name=name, type=format_type, flags=flags, width=width, prec=precision,
                    len=length_mod, is_width='', compat=compatibility, compat_list=[compatibility]))
                if width == '*':
                    report.append(dict(name='', type='*', flags='', width='', prec='',
                        len='', is_width='*', compat='*', compat_list=['*']))
                name = flags = width = precision = length_mod = format_type = ""
                state = 'out'
                continue
            else:
                raise FormatUnrecognized("Invalid char '%s' at position %d in format string %s" % (c, i, repr(string)))

    if state != 'out':
        raise FormatNotFinished("Format string cut abruptly: %s" % repr(string))
    if named_args and uses_width_from_arg:
        raise FormatMixedArgs("Cannot use both mapping and '*' width specifiers in format string %s" % repr(string))
    if named_args and positional_args:
        raise FormatMixedArgs("Cannot use both mapping and positional args in format string %s" % repr(string))
    if named_args:
        for x in report:
            if x['name'] in mapping:
                mapping[x['name']]['compat_list'].append(x['compat'])
            else:
                mapping[x['name']] = x
        for k, v in mapping.items():
            # compat_list must show only represent the compatibility types used, not their number
            v['compat_list'] = sorted(list(set(v['compat_list'])))
            v['compat'] = ''.join(v['compat_list'])
        if not full:
            return ['%s/%s' % (x[1]['name'], x[1]['compat']) for x in sorted(mapping.items())]
        return mapping
    if not full:
        return ['%s/%s' % (x['name'], x['compat']) for x in report]
    return report


def do_format_strings_match(s1, s2):
    return parse_format_string(s1) == parse_format_string(s2)


def create_translation_db_table(db_table, vh=vh):
    """Creates a DB translation table if it does not exist and optionally fills missing entries."""
    return vh.SQL(
            "create table if not exists `%s` (" \
                "`id` bigint unsigned not null primary key," \
                "`value` text collate utf8_unicode_ci not null" \
            ") engine = myisam default character set utf8 collate utf8_unicode_ci" \
            % db_table)[0]


def store_translation_string(id, text, db_table, vh=vh):
    """Stores a string to the DB translation table unless it already exists."""
    return vh.SQL("insert ignore into `%s` (`id`, `value`) values (%s, '%s')" % (
            db_table, str(id), escape_sql(text)))[0]


def fetch_translation_strings(db_table, limit=10000, vh=vh, silent=False):
    """Create a translation dict from strings stored in a DB table."""
    success, rows = vh.SQL("select `id`, `value` from `%s`" % db_table, limit)
    if success and len(rows):
        result = {}
        for item in rows:
            result[int(item[0])] = item[1]
        return result

    if not silent:
        print("No string translations found in database table %s" % db_table)

    return {}


def update_translation_strings(english, translated={}, db_table=None,
    use_translated=False, vh=vh, silent=False, filename=None, create=True):
    """Use this function to update your translation strings from a DB table or a dictionary.

        english dictionary must be in the form: { 0: "string", 1: "something else", ... }.
        translated must also be a dictionary; it will be cleared and filled here.
        db_table is the name of the database table storing the translations.

        If db_table is not provided, nothing will be written to or read from the database.
        If use_translated is true, translation will be read from translated instead of the DB
        and if db_table is given, they will be stored in the database (unless create == False).

        You can also read strings from a file, by setting filename.
        If the file didn't exist, it will be created and filled with English unless create == False.
        Each line in the file is a translation string and the line number is the ID, starting from 1.
        That's why you should not use the 0 ID in translations.
        If you need to embed a newline, write \\n, and for carriage return use \\r.

        This function returns a callable object that works like the gettext function.
    """
    if not isinstance(english, dict):
        raise TranslateError("english must be a dictionary")
    if not isinstance(translated, dict):
        raise TranslateError("translated must be a dictionary")
    if not isinstance(db_table, str) and db_table:
        raise TranslateError("db_table must be a string or be empty")
    if not isinstance(filename, str) and filename:
        raise TranslateError("filename must be a string or be empty")
    if not len(english) > 0:
        raise TranslateError("english cannot be empty")
    if db_table and filename:
        raise TranslateError("You cannot use db_table and filename at the same time")

    for k, v in english.items():
        if not isinstance(k, int):
            raise TranslateError("all english keys must be ints")
        if k < 0:
            raise TranslateError("english keys cannot be negative")
        if not isinstance(v, str):
            raise TranslateError("all english values must be strings")
    
    source = {}
    
    if use_translated:
        for k, v in translated.items():
            if not isinstance(k, int):
                raise TranslateError("all translated keys must be ints")
            if k < 0:
                raise TranslateError("translated keys cannot be negative")
            if not isinstance(v, str):
                raise TranslateError("all translated values must be strings")
        source = translated.copy()

    translated.clear()
    mapping = {}
    for k, v in english.items():
        translated[k] = v


    if db_table and create:
        if not create_translation_db_table(db_table, vh):
            raise TranslateError("failed to create database translation table (if required)")

        for id, text in english.iteritems():
            if not store_translation_string(id, text, db_table):
                raise TranslateError("failed to insert to DB item %s: %s" % (id, repr(text)))

    if db_table:
        limit = max(english.keys()) + 1
        source = fetch_translation_strings(db_table, limit, vh, silent)

    if filename:
        f = ff = None
        try:
            f = open(filename, "r")
        except IOError, e:
            if create:
                try:
                    ff = open(filename, "w")
                except IOError, ee:
                    if not silent:
                        print("Cannot read file %s (%s) nor create it (%s)" % (filename, e, ee), file=sys.stderr)
                if ff:
                    for k, v in english.items():
                        if k == 0:
                            continue  # because file editors do not number from zero!
                        ff.write(v.replace('\n', '\\n').replace('\r', '\\r'))
                        ff.write('\n')
                    ff.close()
            elif not silent:
                print("Cannot read file %s (%s)" % (filename, e), file=sys.stderr)
        if f:
            data = [x.strip('\n\r').replace('\\n', '\n').replace('\\r', '\r') for x in f.readlines()]
            source = dict([(i+1, x) for i, x in enumerate(data)])
            f.close()

    if source:
        for id, text in source.items():
            if id in english:
                try:
                    if do_format_strings_match(text, english[id]):
                        translated[id] = text
                    elif not silent:
                        print("Wrong number of placeholders in translation of %d: '%s'" % (
                                id, english[id]), file=sys.stderr)
                except FormatStringError, e:
                    if not silent:
                        print("Bad translation string: %s" % e, file=sys.stderr)

    for key in english:
        mapping[english[key]] = translated[key]

    class gettext(object):
        def __init__(self, mapping):
            self.mapping = mapping.copy()  # we copy the mapping, so you can destroy the dicts

        def __call__(self, string):
            result = self.mapping.get(string)
            if result:
                return result
            else:
                if not silent:
                    print("Using missing translation string: %s" % string, file=sys.stderr)
                return string

    return gettext(mapping)



##################### UNIT TESTS #####################



def test_eq(a, b, msg=None):
    if a != b:
        if not msg:
            msg = "%s != %s" % (repr(a), repr(b))
        raise AssertionError(msg)

def run_format_strings_test():
    p = parse_format_string
    match = do_format_strings_match

    def throws(s, exc=Exception):
        try:
            p(s)
        except exc:
            return True
        return False

    test_eq(p(""), [])
    test_eq(p("blah blah"), [])
    test_eq(p("blah %% blah %%"), [])

    assert(throws("%w", FormatUnrecognized))
    assert(throws("%123w", FormatUnrecognized))
    assert(throws("%S", FormatUnrecognized))
    assert(throws("%((s", FormatNotFinished))
    assert(throws("%(s", FormatNotFinished))
    assert(throws("blah %", FormatNotFinished))
    assert(throws("blah % P", FormatUnrecognized))
    assert(not throws("blah % s"))
    assert(throws("blah %(a)s %s", FormatMixedArgs))
    assert(throws("blah %(a)s %(b)*s", FormatMixedArgs))

    x = p("test %u", True)[0]
    test_eq(x.get("name"), '')
    test_eq(x.get("type"), 'u')
    test_eq(x.get("flags"), '')
    test_eq(x.get("width"), '')
    test_eq(x.get("prec"), '')
    test_eq(x.get("len"), '')
    test_eq(x.get("is_width"), '')
    test_eq(x.get("compat"), 'f')
    test_eq(x.get("compat_list"), ['f'])

    x = p("test %020.4lG", True)[0]
    test_eq(x.get("name"), '')
    test_eq(x.get("type"), 'g')
    test_eq(x.get("flags"), '0')
    test_eq(x.get("width"), '20')
    test_eq(x.get("prec"), '4')
    test_eq(x.get("len"), 'l')
    test_eq(x.get("is_width"), '')
    test_eq(x.get("compat"), 'f')
    test_eq(x.get("compat_list"), ['f'])

    x = p("test %(test me) -8.2F", True)["test me"]
    test_eq(x.get("name"), 'test me')
    test_eq(x.get("type"), 'f')
    test_eq(x.get("flags"), ' -')
    test_eq(x.get("width"), '8')
    test_eq(x.get("prec"), '2')
    test_eq(x.get("len"), '')
    test_eq(x.get("is_width"), '')
    test_eq(x.get("compat"), 'f')
    test_eq(x.get("compat_list"), ['f'])

    test_eq(p("test %d"), ["/f"])
    test_eq(p("test %g"), ["/f"])
    test_eq(p("test %x"), ["/f"])
    test_eq(p("test %d %s"), ["/f", "/s"])
    test_eq(p("test %*d %s"), ["/f", "/*", "/s"])
    test_eq(p(" %(*)g"), ["*/f"])
    test_eq(p(" %(abc)d"), ["abc/f"])
    test_eq(p(" %(abc)d %(x)s"), ["abc/f", "x/s"])
    test_eq(p(" %(x)s %(abc)d"), ["abc/f", "x/s"])
    test_eq(p(" %(x)s %(abc)d %%%(x)-06.3f"), ["abc/f", "x/fs"])
    test_eq(p(" %(x)s %(x)d %(x)f %(x)s %(x)c %(x)x"), ["x/cfs"])

    assert(match("", "test"))
    assert(match("whatever %%", "test"))
    assert(match("Hi, %s", "Hello, %20s"))
    assert(match("Add %g", "add %6.2f"))
    assert(match("%(x)g", "%(x)f"))
    assert(match("%(x)g %(x)8.1f %(x)-6d %(x)u", "%(x)d"))

    assert(not match("Hi, %d", "Hello, %20s"))
    assert(not match("%c", "%s"))
    assert(not match("%d", "%s"))
    assert(not match("%f", "%f%f"))
    assert(not match("%(x)f", "%(a)f"))
    assert(not match("%(x)f", "%(a)f %(x)f"))


def run_update_translation_strings_test():
    english = { 1: "a test", 2: "catastrophy", 3: "welcome %s!", 5: "%d users online", 6: "" }
    german = { 1: "ein Test", 2: "Katastrophe", 3: "Willkommen, %s!", 4: "Nichts", 5: "%u Nutzer online" }

    _ = update_translation_strings(english, german, use_translated=True, silent=True)
    test_eq(german, { 1: "ein Test", 2: "Katastrophe", 3: "Willkommen, %s!", 5: "%u Nutzer online", 6: "" })
    assert(_("a test") == "ein Test")
    assert(_("catastrophy") == "Katastrophe")
    assert(_("welcome %s!") == "Willkommen, %s!")
    assert(_("%d users online") == "%u Nutzer online")
    assert(_("missing") == "missing")
    old = _

    german[2] = "Katastrophe!!!"
    german[3] = "%sWillkommen, %s"
    german[5] = "%(num)s Nutzer online"
    _ = update_translation_strings(english, german, use_translated=True, silent=True)
    test_eq(german, { 1: "ein Test", 2: "Katastrophe!!!", 3: "welcome %s!", 5: "%d users online", 6: "" })
    german[1] = "xxxxxx"  # to make sure later changes don't change the mapping
    english[2] = "cat"  # same here
    assert(_("a test") == "ein Test")
    assert(_("catastrophy") == "Katastrophe!!!")
    assert(_("welcome %s!") == "welcome %s!")
    assert(_("%d users online") == "%d users online")
    assert(_("test") == "test")
    # print(_.mapping)

    _ = update_translation_strings(english, {1: "x", 2: "y", 5: "%d"}, use_translated=True, silent=True)
    assert(_("a test") == "x")
    assert(_("cat") == "y")
    assert(_("welcome %s!") == "welcome %s!")
    assert(_("%d users online") == "%d")
    assert(_("aaa") == "aaa")
    # print(_.mapping)

    # check that the old translation mapping is still valid
    assert(old("a test") == "ein Test")
    assert(old("catastrophy") == "Katastrophe")
    assert(old("welcome %s!") == "Willkommen, %s!")
    assert(old("%d users online") == "%u Nutzer online")
    assert(old("missing") == "missing")


run_format_strings_test()
run_update_translation_strings_test()

