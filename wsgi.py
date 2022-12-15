import ast
from werkzeug.wrappers import Response, Request
class WSGI:
    def __init__(self):
        self.Routes = []
        self.Config = {}
    def wsgi_handler(self, environ, start_response):
        path = environ.get('PATH_INFO')
        for route in self.Routes:
            if route.route().url == path:
                if not route.route().method == environ['REQUEST_METHOD']: 
                    rsp = Response("<h1>405 Method Not Allowed</h1>")
                    rsp.status_code = 405
                    rsp.headers['Content-Type'] = 'text/html'
                    return rsp(environ, start_response)
                controler = route.route().controler()
                request = Request(environ)
                if hasattr(controler, "auth"):
                    auth = controler.auth()
                    verifier = auth[0]
                    auth = auth[1]
                    claims = auth.get('claims')
                    location = auth.get('cookie') #Can be 'cookie' or 'header'
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

                    #TODO: Check if the JWT is valid
                    try:
                        ans:bool = verifier.verify(jwt)
                    except Exception as e:
                        ans = False
                    if ans:
                        rsp = controler.onRequest(request)
                    else:
                        rsp = Response('{"error":"Invalid Jwt"}', status=403)
                        rsp.headers['Content-Type'] = "application/json"
                        return rsp(environ, start_response)

                if hasattr(controler, "blueprint"):
                    blueprint = controler.blueprint()
                    targetMimetypes = blueprint[1]
                    blueprint = blueprint[0].blueprint
                    if not request.mimetype in targetMimetypes:
                        rsp = Response("<h1>Incorrect mimetype.</h1><p>Sodium v2.00</p>")
                        rsp.headers['Content-Type'] = 'text/html' 
                        return rsp(environ, start_response)
                    if request.mimetype == "application/x-www-form-urlencoded":
                        target = request.form
                    elif request.mimetype == "multipart/form":
                        target = request.form
                    elif request.mimetype == "application/json":
                        target = request.json
                    else:
                        target = request.raw
                    for rule in blueprint:
                        name = rule[0]
                        targetType = rule[1]
                        if not name in list(target.keys()):
                            if request.mimetype == "application/json":
                                rsp = Response('{"status_code":"400", "error":"The route requires a '+ name + ' but it was not found"}')
                                rsp.headers['Content-Type'] = 'application/json'
                            else:
                                rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a {name} but it was not found</p>")
                                rsp.headers['Content-Type'] = 'text/html'
                            return rsp(environ, start_response)
                        clientType = type(target[name]) 
                        if not clientType == targetType:
                            if request.mimetype == "application/json":
                                rsp = Response('{"status_code":"400", "error":"The route requires a the ' + name + ' parameter to be the data type ' + str(targetType) + ' but the ' + str(clientType) + ' type was provided"}')                                
                                rsp.headers['Content-Type'] = 'application/json'
                            else:
                                rsp = Response(f"<h1>400 Bad Request</h1><p>The route requires a the {name} parameter to be the data type {targetType} but the {clientType} type was provided</p>")
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
    def __call__(self, environ, start_response):
        return self.wsgi_handler(environ, start_response)
