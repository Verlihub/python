Python scripts for Verlihub
===========================

To use scripts in this directory make sure you get the most recent Verlihub from <https://github.com/Verlihub/verlihub> and build it with the Python plugin — that should happen automatically when the necessary development header files are detected on your system (for example on Debian you have to install `python-dev`, preferably `python2.7-dev`, but not `python3-dev`). You will find more information about building Verlihub here: <https://github.com/Verlihub/verlihub/wiki>.

Once you have a running hub, you can load the Python plugin with the `!onplug python` command. If that goes well, you can set the hub to automatically load the plugin on start-up using the `modplug python -a 1` command. Turning the plugin on will automatically load python scripts from the `./scripts` subdirectory of your hub instalation (where you keep the `dbconfig` file) in alphabetical (ASCII) order. Python scripts are recognized by their `.py` filename extension.

Here are the commands you can use:

 -  `!pyfiles` — shows a numbered list of scripts found in the `./scripts` directory.

 -  `!pyload <filename>` or `!pyload <id>` — loads the script from the `./scripts` directory using its filename (for example `test.py`) or the number that was displayed next to the script by the `!pyfiles` command. Note that this number can change if you do any changes to Python scripts in that directory. You can also specify a full or relative path instead of `<filename>`, but that will depend on the hub's installation or working directory.

 -  `!pylist` — shows a list of running scripts together with the id numbers given them by the plugin.

 -  `!pyunload <filename>` or `!pyload <id>` — unloads a running script (`<id>` is the number displayed by `!pylist`).

 -  `!pyreload <filename>` or `!pyload <id>` — unloads a reloads a script (`<id>` is the number displayed by `!pylist`). This is useful when you edit the script or want to clear its memory.

 - `!pylog <n>` (where `<n>` is 0, 1, 2, 3, 4, 5 or 6) — changes the amount of debug info the plugin sends to the console (stdout or the log file). You should be fine with "0". Use higher nimbers only for debugging, but beware: they generate lots of output.



Example scripts
---------------

Several Python scripts have been gathered online at <https://github.com/Verlihub/python> to eplain how to write Python scripts for Verlihub and to show their capabilities.


### blacklist.py

...


### mean.py

A funny script providing you with the silly extra functionality YnHub offers. It allows you to "kennylize", "lunarize" and reverse the chat messages of certain users. Changes are stored by nick in the database, so they are still in effect after the user reconnects. For available commands write: `!help mean`.


### myinfo.py

A demonstrative script showing a powerful feature available in the Python plugin. You can use scripts to modify user's myinfo. In real hubs you would use that to implement share hiding or to add important information to people's descriptions.

The command `!myinfo <flags>` specifies which part of myinfo should be modified. `<flags>` is a number created by adding the numbers of fields you want modified: 1=description, 2=tag, 4=speed, 8=email, 16=sharesize, so to turn everything on write: `!myinfo 31`, and to disable changes write: `!myinfo 0`.


### pastebot.py

...


### python1.py

A general purpose script, designed for everyday use — you might want to keep it. The script includes several commands that might be proven useful, some of them known from other hubs, like `!sr`, `!say`, `!mc`, `!ui`, `!ck`, `!block`, `!unblock`.
For a complete list of provided commands write: `!help`


### vh_event_log.py

Use this script only for testing and development. It prints all received hub events and their arguments to the console (or the log file). To turn on logging, use the `!vh_event_log 1` admin command (yes, you need to have class 5 or above), and to turn off, write `!vh_event_log 0`. The command `!vh_event_log` without arguments will show the current state of the script. You can also turn it on and off from another script using `vh.ScriptQuery("vh_event_log", ...)`.



More informations
-----------------

To learn more about enhancing Verlihub with Python scripts, read the documentation about Verlihub's Python API:

 -  handling events: <https://github.com/Verlihub/verlihub/wiki/API-Python-Events>,

 -  using callbacks: <https://github.com/Verlihub/verlihub/wiki/API-Python-Methods>.


