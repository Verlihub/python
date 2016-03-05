Example scripts
---------------

Several Python scripts have been gathered online at <https://github.com/Verlihub/python> to eplain how to write Python scripts for Verlihub and to show their capabilities. Let's see their brief descriptions.


### mean.py

A funny script providing you with the silly extra functionality YnHub offers. It allows you to "kennylize", "lunarize" and reverse the chat messages of certain users. Changes are stored by nick in the database, so they are still in effect after the user reconnects. For available commands write: `!help mean`.


### myinfo.py

A demonstrative script showing a powerful feature available in the Python plugin. You can use scripts to modify user's myinfo. In real hubs you would use that to implement share hiding or to add important information to people's descriptions.

The command `!myinfo <flags>` specifies which part of myinfo should be modified. `<flags>` is a number created by adding the numbers of fields you want modified: 1=description, 2=tag, 4=speed, 8=email, 16=sharesize, so to turn everything on write: `!myinfo 31`, and to disable changes write: `!myinfo 0`.


### python1.py

A general purpose script, designed for everyday use — you might want to keep it. The script includes several commands that might be proven useful, some of them known from other hubs, like `!sr`, `!say`, `!mc`, `!ui`, `!ck`, `!block`, `!unblock`.
For a complete list of provided commands write: `!help`


### vh_event_log.py

Use this script only for testing and development. It prints all received hub events and their arguments to the console (or the log file). To turn on logging, use the `!vh_event_log 1` admin command (yes, you need to have class 5 or above), and to turn off, write `!vh_event_log 0`. The command `!vh_event_log` without arguments will show the current state of the script. You can also turn it on and off from another script using `vh.ScriptQuery("vh_event_log", ...)`.
