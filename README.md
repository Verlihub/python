Python scripts for Verlihub
===========================

To use scripts in this directory make sure you get the most recent Verlihub from <https://github.com/Verlihub/verlihub> and that it builds with the Python plugin — that should happen automatically when the necessary development header files are detected on your system (for example on Debian you have to install `python-dev` or preferably `python2.7-dev`; but do not install `python3-dev`). You will find more information about building Verlihub here: <https://github.com/Verlihub/verlihub/wiki>.

Once you have a running hub, you can load the Python plugin with the `!onplug python` command. If that goes well, you can set the hub to automatically load the plugin on start-up using the `!modplug python -a 1` command. Turning the plugin on will automatically load python scripts from the `./scripts` subdirectory of your hub instalation (where you keep the `dbconfig` file) in alphabetical (ASCII) order. Python scripts are recognized by their `.py` filename extension.

Here are the commands you can use:

 -  `!pyfiles` — shows a numbered list of scripts found in the `./scripts` directory.

 -  `!pyload <filename>` or `!pyload <id>` — loads the script from the `./scripts` directory using its filename (for example `test.py`) or the number that was displayed next to the script by the `!pyfiles` command. Note that this number can change if you do any changes to Python scripts in that directory. You can also specify a full or relative path instead of `<filename>`, but that will depend on the hub's installation or working directory.

 -  `!pylist` — shows a list of running scripts together with the id numbers given them by the plugin.

 -  `!pyunload <filename>` or `!pyload <id>` — unloads a running script (`<id>` is the number displayed by `!pylist`).

 -  `!pyreload <filename>` or `!pyload <id>` — unloads a reloads a script (`<id>` is the number displayed by `!pylist`). This is useful when you edit the script or want to clear its memory.

 - `!pylog <n>` (where `<n>` is 0, 1, 2, 3, 4, 5 or 6) — changes the amount of debug info the plugin sends to the console (stdout or the log file). You should be fine with "0". Use higher nimbers only for debugging, but beware: they generate lots of output.

More information
----------------

To learn more about enhancing Verlihub with Python scripts, read the documentation about Verlihub's Python API:

 -  handling events — <https://github.com/Verlihub/verlihub/wiki/API-Python-Events>,

 -  using callbacks — <https://github.com/Verlihub/verlihub/wiki/API-Python-Methods>.
