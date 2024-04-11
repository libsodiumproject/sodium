import json
import re
import base64
from werkzeug.wrappers import Response, Request
from routes import Mapper
from .exceptions import HttpError

class Route:
    def __init__(self, method, url, controler):
        self.method = method
        self.url = url
        self.controler = controler

class WSGI:
    def __init__(self):
        self.Routes = []
        self.Config = {}
        self.map = Mapper()
        self.secondary_map = {}

    def runControler(self, controler, request, params):
        try:
            rsp = controler.onRequest(request, *list(params.values()))
        except HttpError as e:
            rsp = Response(e.message)
            rsp.headers["Content-Type"] = "text/html"
            rsp.status_code = e.code
        
        return rsp

    def wsgi_handler(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if self.map.match(path):
            route = self.secondary_map[self.map.match(path)["controler"]]
            params = dict(self.map.match(path))
            del params["controler"]
            print(list(params.values()))
            if not route.method == environ['REQUEST_METHOD']: 
                rsp = Response("<h1>405 Method Not Allowed</h1>")
                rsp.status_code = 405
                rsp.headers['Content-Type'] = 'text/html'
                return rsp(environ, start_response)
            controler = route.controler()
            request = Request(environ)
            if hasattr(controler, "auth"):
                auth = controler.auth()
                verifier = auth[0]
                extra = auth[1]
                scopes = extra.get('scopes')
                location = extra.get('cookie') 
                if not location:
                    location = "header"
                if location == "header":
                    header = request.headers.get("Authorization")
                    if not header:
                        rsp = Response('{"error":"JWT not found"}')
                        rsp.headers['Content-Type'] = "application/json"
                        return rsp(environ, start_response)
                    header = header.split(" ")
                    if len(header) == 1:
                        jwt = header[0]
                    elif len(header) == 2 and header[0] == "Bearer":
                        jwt = header[1]
                    else:
                        rsp = Response('{"error":"JWT is formated incorrectly"}')
                        rsp.headers['Content-Type'] = "application/json"
                        return rsp(environ, start_response)
                else:
                    c = request.cookies.get(location)
                    if not c:
                        rsp = Response('{"error":"JWT not found"}')
                        rsp.headers['Content-Type'] = "application/json"
                        return rsp(environ, start_response)
                    jwt = c

                try:
                    ans:bool = verifier.verify(jwt)
                except Exception as e:
                    ans = False
                if ans:
                    #Check for scopes
                    if scopes:
                        jwt = jwt.split(".")
                        header = jwt[0]
                        body = jwt[1]
                        body = json.loads(base64.urlsafe_b64decode(body+"=="))
                        found_scopes = body.get("scopes")
                        if not found_scopes:
                            rsp = Response('{"error":"Invalid Jwt", "detail":"No scopes specified"}', status=403)
                            rsp.headers["Content-Type"] = "application/json"
                            return rsp(environ, start_response)
                        for scope in scopes:
                            if not isinstance(scope, tuple) and not scope in found_scopes:
                                rsp = Response('{"error":"Scope Error", "detail":"Scope ' + f"'{scope}'" + ' not found"}', status=403)
                                rsp.headers["Content-Type"] = "application/json"
                                return rsp(environ, start_response)
                            elif isinstance(scope, tuple):
                                found1scope = False
                                for optional_scope in scope:
                                    if optional_scope in found_scopes:
                                        found1scope = True

                                if not found1scope:
                                    rsp = Response('{"error":"Scope Error", "detail":"Scope ' + f"'{scope}'" + ' not found(you need at least one of those scopes)"}', status=403)
                                    rsp.headers["Content-Type"] = "application/json"
                                    return rsp(environ, start_response)


                    rsp = self.runControler(controler, request, params)
                else:
                    rsp = Response('{"error":"Invalid Jwt"}', status=403)
                    rsp.headers['Content-Type'] = "application/json"
                    return rsp(environ, start_response)

            if hasattr(controler, "blueprint"):
                from .classes import Blueprint
                blueprint = controler.blueprint()
                targetMimetypes = blueprint[1]
                blueprint = blueprint[0]
                #If reached, the blueprint was created using the class syntax
                if not type(blueprint) == Blueprint:
                    #Filter out everything but class varibles
                    classattrs = dir(blueprint)
                    names = []
                    for i in classattrs:
                        if not i.startswith("__"):
                            names.append(i)
                    #Get The Values
                    values = []
                    for i in names:
                        values.append(eval(f"blueprint.{i}"))

                    #Convert to an (internal) blueprint
                    rules = []
                    for name, value in zip(names, values):
                        rules.append((name, value))
                    blueprint = Blueprint(rules)

                blueprint = blueprint.blueprint
                if not request.mimetype in targetMimetypes:
                    rsp = Response("<h1>Incorrect mimetype.</h1><p>Sodium v2.70</p>")
                    rsp.headers['Content-Type'] = 'text/html' 
                    return rsp(environ, start_response)
                if request.mimetype == "application/x-www-form-urlencoded":
                    target = request.form
                elif request.mimetype == "multipart/form":
                    target = request.form
                elif request.mimetype == "application/json":
                    target = request.json
                else:
                    rsp = Response('<h1>This mimetype is unsupported.</h1>')
                    rsp.headers['Content-Type'] = 'application/json'
                    return rsp(environ, start_response)
                if target == None:
                    #This should be unreachable, it can't be None
                    return

                for rule in blueprint:
                    name = rule[0]
                    targetType = rule[1].typ
                    
                    #check to see if all the keys are present
                    try:
                        value = target[name]
                    except:
                        rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a {name} but it was not found</p>")
                        if request.mimetype == "aplication/json":
                            rsp = Response('{"status_code":"400", "error":"The route requires a '+ name + ' but it was not found"}')
                        rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)

                    #check to see if all the values are the right type
                    try:
                        clientType = int(value)
                        clientType = type(clientType)
                    except:
                        clientType = type(value)
                    if not clientType == targetType:
                        if request.mimetype == "application/json":
                            rsp = Response('{"status_code":"400", "error":"The route requires a the ' + name + ' parameter to be the data type ' + str(targetType) + ' but the ' + str(clientType) + ' type was provided"}')                                
                            rsp.headers['Content-Type'] = 'application/json'
                        else:
                            rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a the {name} parameter to be the data type {targetType} but the {clientType} type was provided</p>")
                            rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)

                    #Check the min/max requirements
                    min = rule[1].min
                    max = rule[1].max
                    if not min == None:
                        if len(str(value)) < min:
                            if request.mimetype == "application/json":
                                rsp = Response('{"status_code":"400", "error":"The route requires the ' + name + ' parameter to have a minimum of ' + str(min) + ' letters' + '}')                                
                                rsp.headers['Content-Type'] = 'application/json'
                            else:
                                rsp = Response('<h1>The route requires the ' + name + ' parameter to have a minimum of ' + str(min) + ' letters</h1>')
                                rsp.headers['Content-Type'] = 'text/html'
                            return rsp(environ, start_response)
                    if not max == None:
                        if len(str(value)) > max:
                            if request.mimetype == "application/json":
                                rsp = Response('{"status_code":"400", "error":"The route requires the ' + name + ' parameter to have a maximum of ' + str(max) + ' letters' + '}')                                
                                rsp.headers['Content-Type'] = 'application/json'
                            else:
                                rsp = Response('<h1>The route requires the ' + name + ' parameter to have a maximum of ' + str(max) + ' letters</h1>')
                                rsp.headers['Content-Type'] = 'text/html'
                            return rsp(environ, start_response)

                    #Check the regex's
                    regex = "."
                    if not rule[1].regex == None:
                        regex = rule[1].regex
                    if not re.search(regex, str(value)):
                        if request.mimetype == "application/json":
                            rsp = Response('{"status_code":"400", "error":"The route requires the ' + name + ' parameter to follow this regex: ' + str(regex) + '}')                                
                            rsp.headers['Content-Type'] = 'application/json'
                        else:
                            rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires the {name} parameter to follow this regex {str(regex)}</p>")
                            rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)

                rsp = self.runControler(controler, request, params)
            else:
                rsp = self.runControler(controler, request, params)

            if not isinstance(rsp, Response):
                rsp = Response(rsp) 
            return rsp(environ, start_response)
            
        rsp = Response("<h1>404 Not Found</h1>")
        rsp.status_code = 404
        rsp.headers['Content-Type'] = 'text/html'
        return rsp(environ, start_response)

    def onMount(self):
        temp = []
        for route in self.Routes:
            rt = route.route()
            temp.append(rt)
            if len(rt.url) == 1:
                self.map.connect(None, rt.url, controler=rt)
                self.secondary_map[str(rt)] = rt
            elif rt.url[len(rt.url)-1] == "/":
                rt.url = list(rt.url)
                del rt.url[len(rt.url)-1]
                rt.url = ''.join(rt.url)
                self.map.connect(None, rt.url, controler=rt)
                self.secondary_map[str(rt)] = rt
            else:
                self.map.connect(None, rt.url, controler=rt)
                self.secondary_map[str(rt)] = rt 

        self.Routes = temp

    def __call__(self, environ, start_response):
        return self.wsgi_handler(environ, start_response)
