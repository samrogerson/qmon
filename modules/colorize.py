#! /usr/bin/env python
from commands import getoutput
from os import getenv
from getpass  import getuser

# when imported set bold etc for the terminal you're running in
setup_highlighting()

class bcolors :
    BOLD   = '\033[1m'
    BRIGHT = '\033[97m'
    LGREEN = '\033[36m'
    PINK   = '\033[35m'
    BLUE   = '\033[34m'
    ORANGE = '\033[33m'
    GREEN  = '\033[32m'
    RED    = '\033[31m'
    OFF    = '\033[0m'
    HIGHLIGHT = '\033[97m'


def colorize(str,color):
    col = getattr(bcolors,color,"")
    return "{color}{str}{reset}".format(col,str,bcolors.OFF)


def gethighlight(s):
    col = ''
    if s > 127 :
        col = '\033[38;5;16m'
    else :
        col = '\033[38;5;253m'
    return col


def getsubhighlight(s):
    col = ''
    if s > 127 :
        col = '\033[38;5;239m'
    else :
        col = '\033[1m'
    return col


def setuphighlighting():
    user = getuser()
    exception_users = ["jm1103", "kjd110"]
    mac_weirdness = ["mk1009"]
    if user in exception_users:
        bcolors.HIGHLIGHT = gethighlight(0)
        bcolors.BOLD = getsubhighlight(0)
    elif user in mac_weirdness:
        bcolors.HIGHLIGHT = getsubhighlight(0)
        bcolors.BOLD = gethighlight(0)
    else:
        term = getenv('TERM')
        termstring = """xrdb -query | grep "^"""+term+"""\*background" | awk -F"#" '{print $2}' """
        hexcol = getoutput(termstring)
        if not hexcol:
            hexcol =  getoutput("""xrdb -query | grep ^\*background | awk -F"#" '{print $2}' """)
        if hexcol:
            try:
                r  = int(hexcol[:2], 16)
                g  = int(hexcol[2:4], 16)
                b  = int(hexcol[4:], 16)
                saturation = ((r+g+b)/3)
                bcolors.HIGHLIGHT = gethighlight(saturation)
                bcolors.BOLD = getsubhighlight(saturation)
            except ValueError:
                hexcol = ""
