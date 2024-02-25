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
        exit()
    routes = config.get("routes")

    if not routes:
        print("The 'sodiumconfig.json' file does not contain a route section")

    mappings = config.get("mappings")

    if not mappings:
        print("The 'sodiumconfig.json' file does not contain a mappings section")

    os.mkdir(routes+"/"+name)
    main = open(routes+"/"+name+"/main.py", "w")
    init = open(routes+"/"+name+"/__init__.py", "w")
    x = open(routes+"/"+name+"/.sodium", "w")
    x.write(os.getcwd())
    x.close()

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
    print("v2.70\nMade by Ahsan")
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
    os.mkdir(prefix+"src/models")
    os.mkdir(prefix+"src/websockets")
    os.mkdir(prefix+"src/gRPC")
    os.mkdir(prefix+"src/gRPC/protobufs")
    os.mkdir(prefix+"src/.vault")
    
    x = open(prefix+"src/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()
    
    x = open(prefix+"src/websockets/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/gRPC/protobufs/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/gRPC/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/routes/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/plugins/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/blueprints/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/utilities/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/models/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/.vault/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/gRPC/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/gRPC/protobufs/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"src/gRPC/addServices.py", "w")
    x.write("""import os
def addAll(server):
    os.chdir("src/gRPC")
    for file in os.listdir("protobufs"):
        if not file == ".sodium":
            x = __import__("src.gRPC." + file[:len(file)-6]+"."+file[:len(file)-6])
            print(file[:len(file)-6]+"."+file[:len(file)-6])
            exec(f"server = x.{file[:len(file)-6]}.serve(server)")

    return server

if __name__ == "__main__":
    import grpc
    from concurrent import futures
    addAll(grpc.server(futures.ThreadPoolExecutor(max_workers=10)))""")

    os.mkdir(prefix+"src/templates")
    x = open(prefix+"src/templates/.sodium", "w")
    x.write(os.getcwd()+f"/{project_name}")
    x.close()

    x = open(prefix+"start.py", 'w')
    x.write('''from libsodium import Deamon
from sonora.wsgi import grpcWSGI
from socketio import WSGIApp
import eventlet
import json
import importlib
import time

# Foreground
F_Green = "\x1b[32m"
F_Magenta = "\x1b[35m"
F_End = "\x1b[0m"
F_Red = "\033[31m"
F_Yellow = "\x1b[33m"
F_LightCyan = "\x1b[96m"

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


if __name__ == "__main__":    
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
    print("v2.70")
    print(f"{getCurrentTime()} [{F_Magenta}INFO{F_End}] Creating Deamon... ")
    MainDeamon = Deamon()

    print(f"{getCurrentTime()} [{F_LightCyan}SocketIO{F_End}] Loading SocketIO app...")
    from src.websockets.app import sio
    from os import listdir
    from os.path import isfile

    files = [f for f in listdir(path="src/websockets") if isfile("src/websockets/" + f) and not f == "app.py" and f.endswith(".py")]
    for file in files:
        eval(f"importlib.import_module('src.websockets.{file[:len(file)-3]}')")

    print(f"{getCurrentTime()} [{F_Red}DEAMON{F_End}] Loading Mappings")
    mappings = importlib.import_module(Mappings)
    mappings.addRoutes(MainDeamon)

    print(f"{getCurrentTime()} [{F_Red}DEAMON{F_End}] Running Middleware...")

    #import a2wsgi
    #MainDeamon = a2wsgi.WSGIMiddleware(MainDeamon)

    print(f"{getCurrentTime()} [{F_LightCyan}SocketIO{F_End}] Binding SocketIO app...")

    MainDeamon = WSGIApp(sio, MainDeamon)

    print(f"{getCurrentTime()} [{F_Yellow}gRPC{F_End}] Binding gRPC app...")

    from src.gRPC import addServices
    MainDeamon = grpcWSGI(MainDeamon)
    addServices.addAll(MainDeamon)

    print(f"{getCurrentTime()} [{F_Red}DEAMON{F_End}] Starting Sodium...")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), MainDeamon)''')
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
    "version": "2.41",
    "mappings": "src/mappings.py",
    "plugins": "src/plugins",
    "routes": "src/routes",
    "intp": "''' + interpreter + '''",
    "blueprints": "src/blueprints",
    "models":"src/models",
    "utilities":"src/utilities",
    "websockets":"src/websockets"
  },
  "scripts": {}
}''')
    x.close()
    x = open(prefix+"src/models/dev.db", "w")
    x.close()
    x = open(prefix+"src/models/config.py", "w")
    x.write('''from libsodium.db import connection
Connection = connection("sqlite:///src/models/dev.db", echo=False)
#Connection.Engine - The engine
#Connection.Session - The session connected to the db''')
    x.close()
    x = open(prefix+"src/models/base.py", "w")
    x.write("""from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def createModels():
    import src.models.config as config
    from os import listdir
    from os.path import isfile
    files = [f for f in listdir(path="src/models") if isfile("src/models/" + f) and f.endswith(".py")]
    for file in files:
        if not file == "base.py" and not file == "config.py":
            b = __import__("src.models." + file.strip('.py'))
    Base.metadata.create_all(config.Connection.Engine)""")
    x.close()
    x = open(prefix+"src/websockets/app.py", "w")
    x.write("""from socketio import Server
sio = Server()""")
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
        try:
            x = open(".sodium", "r")
            xc = x.read()
            x.close()
            os.chdir(xc.strip("\n"))
            config = open("sodiumconfig.json", "r+")
            contents = dict(json.load(config))
            config.close()
        except FileNotFoundError as e:
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
    elif str(args[1]) == "model":
        if not len(args) == 3:
            print("Name not provided")
            exit()
        contents = contents.get("config")
        if not contents:
            print("The sodiumconfig.json file does not have a config object. Use sodium fix config to atempt to repair the json file")
            exit()
        models = contents.get("models")
        if not models:
            print("File: sodiumconfig.json is missing a 'models' field. The default Blueprint location should be src/blueprints")
            exit()
        x = open(f"{models}/{args[2]}.py", "w")
        x.write(f'''from src.models.base import Base
from libsodium.db import Column, Integer

class {args[2]}(Base):
    __tablename__ = "{args[2]}"
    id = Column(Integer, primary_key=True)
''')
    elif str(args[1]) == "utility":
        if not len(args) == 3:
            print("tool not provided")
            exit()
        if args[2] == "jwt":
            contents = contents.get("config")
            if not contents:
                print("The sodiumconfig.json file does not have a config object. Use sodium fix config to atempt to repair the json file")
                exit()
            utildir = contents.get("utilities")
            if not utildir:
                print("The sodiumconfig.json file does not conain a 'utilities' field")
            print(f"Name for the {F_Magenta}j{F_End}{F_Red}w{F_End}{F_Cyan}t{F_End} service:")
            answer1 = input(f"{F_Green}> ")
            print(f"{F_End}Use key maker utility(y/n)?")
            answer2 = input(f"{F_Green}> ")
            mod = ''
            signer = ''
            header = '{"alg":"", "typ":"jwt"}'
            if not answer2 == "n" or answer2 == "N" or answer2 == "no" or answer2 == "No":
                print(f"{F_End}Select algorithim:")
                print(f"{F_Red}(1) ECDSA{F_End}")
                print(f"{F_Magenta}(2) PKCS{F_End}")
                answer3 = input(f"{F_Green}> ")
                try:
                    answer3 = int(answer3)
                except:
                    print(f"{F_End}{F_Red}Error:{F_End} {answer3} is not a number")
                    exit()
                if answer3 > 2:
                    print(f"{F_Red}Error:{F_End} {answer3} is not an option")
                    exit()
                options = ["ECDSA", "PKCS"]
                selection = options[answer3-1]
                print(f"{F_End}Select key size:")
                answer4 = input(f"{F_Green}> ")
                try:
                    answer4 = int(answer4)
                except:
                    print(f"{F_End}{F_Red}Error:{F_End} {answer4} is not a number")
                    exit()
                if selection == "ECDSA": 
                    from Crypto.PublicKey import ECC
                    mod = "DSS"
                    signer = "signer = DSS.new(key, 'fips-186-3')"
                    selection = "ECC"
                    key = ECC.generate(curve='P-256')
                    header = 'header = {"alg":"ES256", "typ":"jwt"}'
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
                    header = 'header = {"alg":"ES256", "typ":"jwt"}'
                    f = open(f'src/.vault/{answer1}pubkey.pem','wb')
                    f.write(key.publickey().export_key('PEM'))
                    f.close()
                    f = open(f'src/.vault/{answer1}privkey.pem','wb')
                    f.write(key.export_key(format="PEM"))
                    f.close()
                f = open(f"{utildir}/{answer1}JwtImporter.py", "w")
                f.write(f"""from Crypto.PublicKey import {selection}
class {answer1}JwtImporter:
    @staticmethod
    def getKeys():
        publickey = {selection}.import_key(open('src/.vault/{answer1}pubkey.pem').read())
        privatekey = {selection}.import_key(open('src/.vault/{answer1}privkey.pem').read())
        return publickey, privatekey

    @staticmethod
    def getPrivateKey():
        privatekey = {selection}.import_key(open('src/.vault/{answer1}privkey.pem').read())
        return privatekey

    @staticmethod
    def getPublicKey():
        publickey = {selection}.import_key(open('src/.vault/{answer1}pubkey.pem').read())
        return publickey

                    """)
                f.close()
            else:
                f = open(f"{utildir}/{answer1}JwtImporter.py", "w")
                f.write("""class {answer1}:\n    pass""")
                f.close()
            f = open(f"src/utilities/{answer1}JwtFactory.py", "w")
            f.write(f"""import base64
from .{answer1}JwtImporter import {answer1}JwtImporter
from Crypto.Signature import {mod}
from Crypto.Hash import SHA256
import json
import time

class {answer1}JwtFactory:
    def __init__(self) -> None:
        self.importer = {answer1}JwtImporter()
        #self.keys = self.importer.getKeys()
        self.private_key = self.importer.getPrivateKey()
        #self.public_key = self.importer.getPublicKey()

    def generateJWT(self, payload="""+"{}" + f""", **kwargs):
        jwt  = """ + """{
            "iat": int(time.time()),
        }""" + f"""

        jwt.update(kwargs)
        jwt.update(payload)
        return self._makeJwt(jwt)

    def _makeJwt(self, body:dict):
        header = """ + '{"alg":"ES256", "typ":"jwt"}' + f"""
        encoded_header = str(base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')), 'utf-8').strip('=')
        encoded_body = str(base64.urlsafe_b64encode(json.dumps(body).encode('utf-8')), 'utf-8').strip('=')
        unsigned_jwt = encoded_header + '.' + encoded_body
        hash = SHA256.new(unsigned_jwt.encode('utf-8'))
        key = self.private_key
        {signer}
        signature = base64.urlsafe_b64encode(signer.sign(hash)).decode()
        return unsigned_jwt.strip('=') + '.' + signature.strip('=')
""")
            f = open(f"src/utilities/{answer1}JwtVerifier.py", "w")
            f.write(f"""from Crypto.Hash import SHA256
from Crypto.Signature import {mod}
from .{answer1}JwtImporter import {answer1}JwtImporter
import base64

class {answer1}JwtVerifier:
    def __init__(self) -> None:
        self.importer = {answer1}JwtImporter()
        self.public_key = self.importer.getPublicKey()

    def verify(self, jwt):
        jwt = jwt.split('.')
        unsigned_jwt = jwt[0]+'.'+jwt[1]
        try:
            if int(json.loads(unsigned_jwt)['exp']) < time.time():
                return False
        except:
            pass
        h = SHA256.new(unsigned_jwt.encode())
        key = self.public_key
        signature = jwt[2]+"="
        try:
            signature = base64.urlsafe_b64decode(signature)
        except:
            signature = base64.urlsafe_b64decode(signature+"=")
        {signer}
        try:
            signer.verify(h, signature)
            return True
        except Exception as e:
            return False""")
            f.close()
        else:
            print(f"The utility {args[2]} is not creatable")
            exit()
    elif args[1] == "gRPC":
        if not len(args) >= 3:
            print("Invalid amount of arugments please check out the code below\npython3 -m libsodium create gRPC example.proto")
            exit(1)
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
        try:
            x = open("src/gRPC/protobufs/"+args[2], "r")
        except FileNotFoundError:
            x = open("src/gRPC/protobufs/"+args[2], "w")
            x.close()
            os.mkdir("src/gRPC/"+args[2][:len(args[2])-6])
            exit()
        x.close()
        try:
            os.mkdir("src/gRPC/"+args[2][:len(args[2])-6])
        except FileExistsError:
            pass
        
        exit_code = os.system(f"{interpreter} -m grpc_tools.protoc -I src/gRPC/protobufs --python_out=src/gRPC/{args[2][:len(args[2])-6]} --grpc_python_out=src/gRPC/{args[2][:len(args[2])-6]} src/gRPC/protobufs/{args[2]}")

        if not exit_code == 0:
            print("Process is shutting down")
            if not args[3] == "--regen":
                os.rmdir(f"src/gRPC/{args[2][:len(args[2])-6]}")
            exit(1)

        if args[3] == "--regen":
            exit()

        f = open(f"src/gRPC/{args[2][:len(args[2])-6]}/{args[2][:len(args[2])-6]}.py", "w")
        f.write(f"""import src.gRPC.{args[2][:len(args[2])-6]}.{args[2][:len(args[2])-6]}_pb2_grpc as {args[2][:len(args[2])-6]}_pb2_grpc 

def serve(server):
    {args[2][:len(args[2])-6]}_pb2_grpc.add_ExampleServicer_to_server(
        AppServicerHere(), server
    )""")
        f.close()
        f = open(f"src/gRPC/{args[2][:len(args[2])-6]}/.sodium", "w")
        f.write(os.getcwd())
        f.close()

        f = open(f"src/gRPC/{args[2][:len(args[2])-6]}/{args[2][:len(args[2])-6]}_pb2_grpc.py", "r")
        print(f"src/gRPC/{args[2][:len(args[2])-6]}/{args[2][:len(args[2])-6]}_pb2_grpc.py")
        lines = f.read().split("\n")
        lines[4] = f"import src.gRPC.{args[2][:len(args[2])-6]}.{args[2][:len(args[2])-6]}_pb2 as {args[2][:len(args[2])-6]}__pb2"
        f.close()
        f = open(f"src/gRPC/{args[2][:len(args[2])-6]}/{args[2][:len(args[2])-6]}_pb2_grpc.py", "w")
        f.write('\n'.join(lines))
        f.close()

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
    os.system("clear")
    os.system(f'{interpreter} start.py')
