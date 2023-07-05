import json
import re
import base64
from werkzeug.wrappers import Response, Request
from routes import Mapper

class Route:
    def __init__(self, method, url, controler):
        self.method = method
        self.url = url
        self.controler = controler

class WSGI:
    def __init__(self):
        self.Routes = []
        self.Config = {}
        self._secondary_map = {}
        self.map = Mapper()

    def wsgi_handler(self, environ, start_response):
        path = environ.get('PATH_INFO')
        if self.map.match(path):
            route = self._secondary_map[self.map.match(path).get("controler")]
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


                    rsp = controler.onRequest(request)
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

                    #Convert to a normal blueprint
                    rules = []
                    for name, value in zip(names, values):
                        rules.append((name, value.typ, value.regex))
                    blueprint = Blueprint(rules)

                blueprint = blueprint.blueprint
                if not request.mimetype in targetMimetypes:
                    rsp = Response("<h1>Incorrect mimetype.</h1><p>Sodium v2.60</p>")
                    rsp.headers['Content-Type'] = 'text/html' 
                    return rsp(environ, start_response)
                if request.mimetype == "application/x-www-form-urlencoded":
                    target = request.form
                elif request.mimetype == "multipart/form":
                        target = request.form
                elif request.mimetype == "application/json":
                        target = request.json
                else:
                    target = None 
                for rule in blueprint:
                    name = rule[0]
                    targetType = rule[1]
                    try:
                        if not name in list(target.keys()):
                            if request.mimetype == "application/json":
                                rsp = Response('{"status_code":"400", "error":"The route requires a '+ name + ' but it was not found"}')
                                rsp.headers['Content-Type'] = 'application/json'
                                return rsp(environ, start_response)
                            else:
                                rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a {name} but it was not found</p>")
                                rsp.headers['Content-Type'] = 'text/html'
                                return rsp(environ, start_response)
                    except:
                        rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a {name} but it was not found</p>")
                        rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)

                    try:
                        value = target[name]
                    except:
                        rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a {name} but it was not found</p>")
                        rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)

                    clientType = type(value)
                    if not clientType == targetType:
                        if request.mimetype == "application/json":
                            rsp = Response('{"status_code":"400", "error":"The route requires a the ' + name + ' parameter to be the data type ' + str(targetType) + ' but the ' + str(clientType) + ' type was provided"}')                                
                            rsp.headers['Content-Type'] = 'application/json'
                        else:
                            rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a the {name} parameter to be the data type {targetType} but the {clientType} type was provided</p>")
                            rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)
                    regex = "."
                    if len(rule) == 3:
                        regex = rule[2] 
                    if not re.search(regex, str(value)):
                        if request.mimetype == "application/json":
                            rsp = Response('{"status_code":"400", "error":"The route requires a the ' + name + ' parameter to follow this regex: ' + str(regex) + '}')                                
                            rsp.headers['Content-Type'] = 'application/json'
                        else:
                            rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a the {name} parameter to follow this regex {str(regex)}</p>")
                            rsp.headers['Content-Type'] = 'text/html'
                        return rsp(environ, start_response)

                rsp = controler.onRequest(request)
            else:
                rsp = controler.onRequest(Request(environ))
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
            if not rt.url[len(rt.url)-1] == "/":
                self.map.connect(None, rt.url+"/", controler=rt)
                self._secondary_map[str(rt)] = rt
            else:
                self.map.connect(None, rt.url[:len(rt.url)-1], controler=rt)
                self._secondary_map[str(rt)] = rt
                
            self.map.connect(None, rt.url, controler=rt)
            self._secondary_map[str(rt)] = rt
        self.Routes = temp

    def __call__(self, environ, start_response):
        return self.wsgi_handler(environ, start_response)
