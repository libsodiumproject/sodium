#!/usr/bin/env python3
import sys
import os
import time
import json

F_Green = "\x1b[32m"
F_Cyan = "\033[0;36m"
F_Magenta = "\x1b[35m"
F_Red = "\x1b[31m"
F_End = "\033[0m"

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
    print("v2.00\nMade by ahsan")
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
    os.mkdir(prefix+"src/.vault")
    
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
print("v2.00")
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
    "version": "2.00",
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
        x.write(f"""from libsodium import Blueprint

{name}Blueprint = Blueprint([
('example',str)
]) 
""")
    elif str(args[1]) == "utility":
        if not len(args) == 3:
            print("tool not provided")
            exit()
        if args[2] == "jwt":
            contents = contents.get("config")
            if not contents:
                print("The sodiumconfig.json file does not have a config object. Use sodium fix config to atempt to repair the json file")
                exit()
            print(f"Name for the {F_Magenta}j{F_End}{F_Red}w{F_End}{F_Cyan}t{F_End} service:")
            answer1 = input(f"{F_Green}> ")
            print(f"{F_End}Use key maker utility(y/n)?")
            answer2 = input(f"{F_Green}> ")
            mod = ""
            signer = ""
            if not answer2 == "n" or answer2 == "N" or answer2 == "no" or answer2 == "No":
                print(f"{F_End}Select algorithim:")
                print(f"{F_Green}(1) DSA{F_End}")
                print(f"{F_Red}(2) ECDSA{F_End}")
                print(f"{F_Magenta}(3) PKCS{F_End}")
                print(f"{F_Cyan}(4) EdDSA{F_End}")
                answer3 = input(f"{F_Green}> ")
                try:
                    answer3 = int(answer3)
                except:
                    print(f"{F_End}{F_Red}Error:{F_End} {answer3} is not a number")
                    exit()
                if answer3 > 4:
                    print(f"{F_Red}Error:{F_End} {answer3} is not an option")
                    exit()
                options = ["DSA", "ECDSA", "PKCS", "EdDSA"]
                selection = options[answer3-1]
                print(f"{F_End}Select key size:")
                answer4 = input(f"{F_Green}> ")
                try:
                    answer4 = int(answer4)
                except:
                    print(f"{F_End}{F_Red}Error:{F_End} {answer4} is not a number")
                    exit()
                if selection == "DSA":
                    from Crypto.PublicKey import DSA
                    mod = "DSS"
                    signer = "signer = DSS.new(key, 'fips-186-3')"
                    key = DSA.generate(answer4)
                    f = open(f"src/.vault/{answer1}pubkey.pem", "wb")
                    f.write(key.publickey().export_key())
                    f.close()
                    f = open(f"src/.vault/{answer1}privkey.pem", "wb")
                    f.write(key.export_key())
                    f.close()
                if selection == "ECDSA" or selection == "EdDSA":
                    from Crypto.PublicKey import ECC
                    if selection == "ECDSA":
                        mod = "DSS"
                        signer = "signer = DSS.new(key, 'fips-186-3')"
                    else:
                        mod = "eddsa"
                        signer = "signer = eddsa.new(key, 'rfc8032')"
                    selection = "ECC"
                    key = ECC.generate(curve='P-256')
                    f = open(f"src/.vault/{answer1}privkey.pem", "wt")
                    f.write(key.export_key(format='PEM'))
                    f.close()
                    f = open(f"src/.vault/{answer1}pubkey.pem", "wt")
                    f.write(key.public_key().export_key(format='PEM'))
                if selection == "PKCS":
                    from Crypto.PublicKey import RSA
                    selection = "RSA"
                    mod = "pkcs1_15"
                    signer = "signer = pkcs1_15.new(key)"
                    key = RSA.generate(answer4)
                    f = open(f'src/.vault/{answer1}pubkey.pem','wb')
                    f.write(key.publickey().export_key('PEM'))
                    f.close()
                    f = open(f'src/.vault/{answer1}privkey.pem','wb')
                    f.write(key.export_key(format="PEM"))
                    f.close()
                f = open(f"src/utilities/{answer1}JwtLoader.py", "w")
                f.write(f"""from Crypto.PublicKey import {selection}
def getKeys():
    publickey = {selection}.import_key(open('src/.vault/{answer1}pubkey.pem').read())
    privatekey = {selection}.import_key(open('src/.vault/{answer1}privkey.pem').read())
    return publickey, privatekey
                    """)
                f.close()
            else:
                f = open(f"src/utilities/{answer1}JwtLoader.py", "w")
                f.write("""def getKeys():\n    pass""")
                f.close()
            f = open(f"src/utilities/{answer1}JwtPrinter.py", "w")
            f.write(f"""import base64
from .testJwtLoader import getKeys
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import json
def makeJwt(header:dict, body:dict):
    encoded_header = str(base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')), 'utf-8').strip('=')
    encoded_body = str(base64.urlsafe_b64encode(json.dumps(body).encode('utf-8')), 'utf-8').strip('=')
    unsigned_jwt = encoded_header + '.' + encoded_body
    hash = SHA256.new(unsigned_jwt.encode('utf-8'))
    key = getKeys()[1]
    signer = DSS.new(key, 'fips-186-3') 
    signature = base64.urlsafe_b64encode(signer.sign(hash)).decode()
    return unsigned_jwt.strip('=') + '.' + signature.strip('=')
""")
            f = open(f"src/utilities/{answer1}JwtVerifier.py", "w")
            f.write(f"""from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from .testJwtLoader import getKeys
import base64
def verify(jwt):
    jwt = jwt.split('.')
    unsigned_jwt = jwt[0]+'.'+jwt[1]
    h = SHA256.new(unsigned_jwt.encode())
    print(unsigned_jwt)
    print(h.hexdigest())
    key = getKeys()[0] #This will get the public key
    signature = jwt[2]+"="
    try:
        signature = base64.urlsafe_b64decode(signature)
    except:
        signature = base64.urlsafe_b64decode(signature+"=")
    signer = DSS.new(key, 'fips-186-3')
    try:
        signer.verify(h, signature)
        return True
    except Exception as e:
        return False""")
            f.close()
        else:
            print(f"The utility {args[2]} is not creatable")
            exit()
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
