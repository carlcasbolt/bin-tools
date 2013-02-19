#!/usr/bin/python
#!/export/home/ryoung/local/python-2.6.1/bin/python
"""
Takes input from stdin, and colorizes the lines depending on their error level. 
As well as colorizing some module names.

Simple usage:
tail -f log/frontend_dev.log | colour.py
"""
import sys
import re

r = re.compile(r'\[([^]]*)\]+')
reModule = re.compile(r'{([^}]*)}')
pattern = r'\033[0;31m\1\033[0;37m'

colorCode = {'black': '\033[0;30m', 'dark_gray':   '\033[1;30m', 'blue':      '\033[0;34m', 'light_blue':   '\033[1;34m',
            'green': '\033[0;32m', 'light_green': '\033[1;32m', 'cyan':      '\033[0;36m', 'light_cyan':   '\033[1;36m',
            'red':   '\033[0;31m', 'light_red':   '\033[1;31m', 'purple':    '\033[0;35m', 'light_purple': '\033[1;35m',
            'brown': '\033[0;33m', 'yellow':      '\033[1;33m', 'light_gray': '\033[0;37m', 'white':        '\033[1;37m'
            }

colors = {
        'debug':   '\033[1;33m%line%\033[0;37m',
        'info':    '\033[0;37m%line%\033[0;37m',
        'notice':  '\033[1;37m%line%\033[0;37m',
        'warning': '\033[1;31m%line%\033[0;37m',
        'err':     '\033[0;31m%line%\033[0;37m',
        'crit':    '\033[0;35m%line%\033[0;37m',
        'alert':   '\033[1;35m%line%\033[0;37m',
        'emerg':   '\033[0;33m%line%\033[0;37m',
        }

moduleColorCodes = {
                    'sfView':       'green',
                    'sfResponse':   'purple',
                    'sfFilter':     'brown',
                    'sfContext':    'brown',
                    'sfController': 'brown',
                    'sfRequest':    'brown',
                    'sfAction':     'cyan',
                    'sfCreole':     'light_cyan',
                    'sfViewConfig': 'green'
                    }

disabledModules = ['sfTimerManager']

while True:
    line = sys.stdin.readline()
    match = r.search(line)
    level = 'info'
    linestyle = '%line%'
    if match and colors.has_key(match.group(1)):
        level = match.group(1)
        linestyle = colors[match.group(1)]
    line = line.replace('\n', '')
    line = linestyle.replace('%line%', line)
    module_match = reModule.search(line)
    if module_match and moduleColorCodes.has_key(module_match.group(1)):
        line = reModule.sub(colorCode[moduleColorCodes[module_match.group(1)]] + r'{\1}' +  colorCode['light_gray'], line, 1)
    if module_match and not module_match.group(1) in disabledModules:
        sys.stdout.write(line + '\n');
    elif not module_match:
        sys.stdout.write(line + '\n');
