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
                if hasattr(controler, "blueprint"):
                    blueprint = controler.blueprint()
                    targetMimetypes = blueprint[1]
                    blueprint = blueprint[0].blueprint
                    request = Request(environ)
                    if not request.mimetype in targetMimetypes:
                        rsp = Response("<h1>Incorrect mimetype.</h1><p>Sodium v1.02</p>")
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
