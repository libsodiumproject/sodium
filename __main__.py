#!/usr/bin/env python3
import sys
import os
import time
import json

from libsodium import Deamon

def getCurrentTime():
    localtime = time.localtime()
    return f"{localtime[0]}-{localtime[1]}-{localtime[2]}: {localtime[3]}:{localtime[4]}:{localtime[5]}"

def createRoute(method, jconfig, name, url):
    jconfig = dict(jconfig)
    config = jconfig.get("config")
    if not config:
        print("'sodiumconfig.json' does not contain a config object.")
    routes = config.get("routes")

    if not routes:
        print("The 'sodiumconfig.json' file does not contain a route section")
    mappings = config.get("mappings")

    if not mappings:
        print("The 'sodiumconfig.json' file does not contain a mappings section")
    os.mkdir(routes+"/"+name)
    main = open(routes+"/"+name+"/main.py", "w")
    init = open(routes+"/"+name+"/__init__.py", "w")

    main.write(f"""from libsodium import Route, Response

def route():
    class {name}:
        def onRequest(self, request):
            rsp = Response(f'<h1>Hello World!</h1>')
            rsp.headers['Content-Type'] = 'text/html'
            return rsp
    return Route('{method}', '{url}', {name})
""")
    init.write("from .main import route")
    
    init.close()
    main.close()

    try:
        mappingfile = open(mappings, 'r')
    except FileNotFoundError:
        print("The mappings file does not exist. Check the sodiumconfig.json file and make sure the file exists")
        exit()
    maplines = mappingfile.readlines()
    mappingfile.close()
    insert = [f"from src.routes import {name}\n", f"routelist.append({name})\n"]
    for i in maplines:
        if str(i) == "routelist = []\n":
            print("it is made it")
            print(insert)
            insert.insert(0, i)
        else:
            insert.append(i)
    mappings = open(mappings, "w")
    mappings.write("".join(insert))
    mappings.close()

args = sys.argv
del args[0]

if len(args) == 0:
    x = r"""                                                                                                          
                                                dddddddd                                                  
   SSSSSSSSSSSSSSS                              d::::::d  iiii                                            
 SS:::::::::::::::S                             d::::::d i::::i                                           
S:::::SSSSSS::::::S                             d::::::d  iiii                                            
S:::::S     SSSSSSS                             d:::::d                                                   
S:::::S               ooooooooooo       ddddddddd:::::d iiiiiii uuuuuu    uuuuuu     mmmmmmm    mmmmmmm   
S:::::S             oo:::::::::::oo   dd::::::::::::::d i:::::i u::::u    u::::u   mm:::::::m  m:::::::mm 
 S::::SSSS         o:::::::::::::::o d::::::::::::::::d  i::::i u::::u    u::::u  m::::::::::mm::::::::::m
  SS::::::SSSSS    o:::::ooooo:::::od:::::::ddddd:::::d  i::::i u::::u    u::::u  m::::::::::::::::::::::m
    SSS::::::::SS  o::::o     o::::od::::::d    d:::::d  i::::i u::::u    u::::u  m:::::mmm::::::mmm:::::m
       SSSSSS::::S o::::o     o::::od:::::d     d:::::d  i::::i u::::u    u::::u  m::::m   m::::m   m::::m
            S:::::So::::o     o::::od:::::d     d:::::d  i::::i u::::u    u::::u  m::::m   m::::m   m::::m
            S:::::So::::o     o::::od:::::d     d:::::d  i::::i u:::::uuuu:::::u  m::::m   m::::m   m::::m
SSSSSSS     S:::::So:::::ooooo:::::od::::::ddddd::::::ddi::::::iu:::::::::::::::uum::::m   m::::m   m::::m
S::::::SSSSSS:::::So:::::::::::::::o d:::::::::::::::::di::::::i u:::::::::::::::um::::m   m::::m   m::::m
S:::::::::::::::SS  oo:::::::::::oo   d:::::::::ddd::::di::::::i  uu::::::::uu:::um::::m   m::::m   m::::m
 SSSSSSSSSSSSSSS      ooooooooooo      ddddddddd   dddddiiiiiiii    uuuuuuuu  uuuummmmmm   mmmmmm   mmmmmm
"""
    print("\x1b[32m"+x+"\x1b[0m")
    print("v1.02\nMade by ahsan")
    exit()

if args[0] == "init":
    print("\033[93m"+"Name for project(leave blank to use current directory):"+"\x1b[0m")
    project_name = input("\x1b[32m"+"> ")
    print("\033[93m"+"What is your interpreter(ex. python3, python, py)"+"\x1b[0m")
    interpreter = input("\x1b[32m"+"> ")
    prefix = ""
    print("Creating project...")
    if project_name:
        os.mkdir(project_name)
        prefix = project_name+"/"

    #Create file structure
    os.mkdir(prefix+"src")
    os.mkdir(prefix+"src/routes")
    os.mkdir(prefix+"src/plugins")
    os.mkdir(prefix+"src/blueprints")
    os.mkdir(prefix+"src/utilities")
    
    x = open(prefix+"start.py", 'w')
    x.write('''from werkzeug import run_simple
import json
import importlib
import time
from libsodium import Deamon
# Foreground
F_Green = "\x1b[32m"
F_Magenta = "\x1b[35m"
F_End = "\033[0m"
F_Red = "\x1b[31m"

def getCurrentTime():
    localtime = time.localtime()
    return f"{localtime[0]}-{localtime[1]}-{localtime[2]}: {localtime[3]}:{localtime[4]}:{localtime[5]}"

try:
    config = open("sodiumconfig.json", "r+")
    contents = dict(json.load(config))
    config.close()
except FileNotFoundError:
    print("[91m[1mError code 0: [0m")
    print("File: 'sodiumconfig.json' not found")
    exit()
except:
    print("[91m[1mError code 1: [0m")
    print("File: 'sodiumconfig.json' has improper json")
    exit()

Mappings = contents.get("config")
if not Mappings:
    print("[91m[1mError code 1: [0m")
    print("File: 'sodiumconfig.json' has improper json. The 'mappings' atribute was not found")
    exit() 
    
Mappings = Mappings.get("mappings").split('.')
del Mappings[len(Mappings)-1]
Mappings = ''.join(Mappings)
Mappings = str(Mappings).replace("/", ".")
x = r"""                                                                                                       
                                                dddddddd                                                  
   SSSSSSSSSSSSSSS                              d::::::d  iiii                                            
 SS:::::::::::::::S                             d::::::d i::::i                                           
S:::::SSSSSS::::::S                             d::::::d  iiii                                            
S:::::S     SSSSSSS                             d:::::d                                                   
S:::::S               ooooooooooo       ddddddddd:::::d iiiiiii uuuuuu    uuuuuu     mmmmmmm    mmmmmmm   
S:::::S             oo:::::::::::oo   dd::::::::::::::d i:::::i u::::u    u::::u   mm:::::::m  m:::::::mm 
 S::::SSSS         o:::::::::::::::o d::::::::::::::::d  i::::i u::::u    u::::u  m::::::::::mm::::::::::m
  SS::::::SSSSS    o:::::ooooo:::::od:::::::ddddd:::::d  i::::i u::::u    u::::u  m::::::::::::::::::::::m
    SSS::::::::SS  o::::o     o::::od::::::d    d:::::d  i::::i u::::u    u::::u  m:::::mmm::::::mmm:::::m
       SSSSSS::::S o::::o     o::::od:::::d     d:::::d  i::::i u::::u    u::::u  m::::m   m::::m   m::::m
            S:::::So::::o     o::::od:::::d     d:::::d  i::::i u::::u    u::::u  m::::m   m::::m   m::::m
            S:::::So::::o     o::::od:::::d     d:::::d  i::::i u:::::uuuu:::::u  m::::m   m::::m   m::::m
SSSSSSS     S:::::So:::::ooooo:::::od::::::ddddd::::::ddi::::::iu:::::::::::::::uum::::m   m::::m   m::::m
S::::::SSSSSS:::::So:::::::::::::::o d:::::::::::::::::di::::::i u:::::::::::::::um::::m   m::::m   m::::m
S:::::::::::::::SS  oo:::::::::::oo   d:::::::::ddd::::di::::::i  uu::::::::uu:::um::::m   m::::m   m::::m
 SSSSSSSSSSSSSSS      ooooooooooo      ddddddddd   dddddiiiiiiii    uuuuuuuu  uuuummmmmm   mmmmmm   mmmmmm

"""
print(F_Green+x+F_End)
print("v1.02")
print(f"{getCurrentTime()} [{F_Magenta}INFO{F_End}] Creating Deamon... ")
MainDeamon = Deamon()
print(f"{getCurrentTime()} [{F_Red}DEAMON{F_End}] Loading Mappings")
mappings = importlib.import_module(Mappings)
mappings.addRoutes(MainDeamon)
print(f"{getCurrentTime()} [{F_Red}DEAMON{F_End}] Starting Sodium...")                                 
run_simple('127.0.0.1', 5000, MainDeamon)''')
    x.close()
    x = open(prefix+"src/mappings.py", "w")
    x.write("""routelist = []
def addRoutes(app):
    app.addRoutes(routelist)
    return app
""")
    x.close()

    x = open(prefix+"sodiumconfig.json", "w")
    x.write('''{
  "config": {
    "version": "1.02",
    "mappings": "src/mappings.py",
    "mappinglst":"src/mappings.txt",
    "plugins": "src/plugins",
    "routes": "src/routes",
    "intp": "''' + interpreter + '''",
    "blueprints": "src/blueprints",
    "utilities":"src/utilities"
  },
  "scripts": {}
}''')
    x.close()
    exit()
if args[0] == "create":
    if len(args) < 2:
        print(f"The function create requires a minnimum of 2 arguments, but only {len(args)} were provided")
        exit()
    try:
        config = open("sodiumconfig.json", "r+")
        contents = dict(json.load(config))
        config.close()
    except FileNotFoundError:
        print("\033[91m\033[1mError code 0: \033[0m")
        print("File: 'sodiumconfig.json' not found")
        exit()
    except:
        print("\033[91m\033[1mError code 1: \033[0m")
        print("File: 'sodiumconfig.json' has improper json")
        exit()
    if str(args[1]).endswith("Route"):
        if not len(args) == 4:
            print("\033[91m\033[1mWhen creating a route the function must have 3 arguments, but only "+str(len(args))+" were given"+"\033[0m")
            exit()
        name = args[2]
        url = args[3]
        if args[1] == "GETRoute":
            createRoute("GET", contents, name, url)
        elif args[1] == "POSTRoute":
            createRoute("POST", contents, name, url)
        elif args[1] == "PUTRoute":
            createRoute("PUT", contents, name, url)
        elif args[1] == "HEADRoute":
            createRoute("HEAD", contents, name, url)
        elif args[1] == "DELETERoute":
            createRoute("DELETE", contents, name, url)
        elif args[1] == "CONNECTRoute":
            createRoute("CONNECT", contents, name, url)
        elif args[1] == "OPTIONSRoute":
            createRoute("OPTIONS", contents, name, url)
        elif args[1] == "TRACERoute":
            createRoute("TRACE", contents, name, url)
        elif args[1] == "PATCHRoute":
            createRoute("PATCH", contents, name, url)

    elif str(args[1]) == "blueprint":
        if not len(args) == 3:
            print("Blueprints require a name. Which was not provided.")
        name = args[2]
        contents = contents.get("config")
        if not contents:
            print("The sodiumconfig.json file does not have a config object. Use sodium fix config to atempt to repair the json file")
            exit()
        blueprintLocations = contents.get("blueprints")
        if not blueprintLocations:
            print("File: sodiumconfig.json is missing a 'blueprints' field. The default Blueprint location should be src/blueprints")
            exit()
        x = open(f"{blueprintLocations}/{name}Blueprint.py", 'w')
        x.write(f"""from sodium import Blueprint

{name}Blueprint = Blueprint([
('example',str)
]) 
""")

    else:
        print("'"+str(args[1])+"'"+" is not creatable")

if args[0] == "start":
    try:
        open('start.py', 'r')
    except:
        print("The start.py files is missing. ")
    try:
        config = open('sodiumconfig.json', 'r')
    except:
        print("The sodiumconfig.json file was not found")
        exit()
    try:
        config = json.load(config)
    except Exception as e:
        print("JSON Parse error: " + str(e))
        exit()
    if config.get('config'):
        config  = config.get('config')
    else:
        print("The sodiumconfig.json file does not have a config object")
        exit()
    if config.get("intp"):
        interpreter = config.get("intp")
    else:
        print("The sodiumconfig.json file does not have a intp field in the config object")
        exit()
    os.system(f'{interpreter} start.py')
