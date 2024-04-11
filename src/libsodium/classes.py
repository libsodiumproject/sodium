from .wsgi import WSGI
from functools import wraps
import json
import base64

class Runtime:
    def __init__(self):
        self.routes = []
    def addRoute(self, route):
        self.routes.append(route)

class Route:
    def __init__(self, method, url, controler):
        self.method = method
        self.url = url
        self.controler = controler

class Deamon(WSGI):
    def addRoute(self, route: Route):
        self.Routes.append(route)

    def addRoutes(self, routes):
        try:
            for i in routes:
                self.Routes.append(i)
        except:
            raise Exception("Error while processing routes. Function 'addRoutes' requires data in format List[Route]. The format specified was not a list. You may have ment to use the Function 'addRoute' instead")
        self.onMount()

"""
Blueprint API(v1):
Blueprints allow you to filter content that comes from the client. This
allows you to allways expect your data in a format you define. For
example, lets say you had a POST route under /signup. Instead of writing
lots of checks to insure that the client has provided the required
information to create an account. Lets say that the /signup route requires
a username and password. Without blueprints you would have to write checks 
to ensure that the client has provided a username and password. That would
look something like this:

from libsodium import Route
def route():
    class signup:
        def onRequest(self, request):
            if request.form.get('username') == None:
                return 'Please provide a username'
            if request.form.get('password') == None:
                return 'Please provide a password'
            create_account(request.form['username'], request.form.get['password'])
            return 'Account Created'
    return Route('POST', '/signup', signup)

With blueprints, all of the checks are automaticly accounted for, before
you even see a request. Using the sodium cli you can create a blueprint like
this:

python3 -m libsodium create blueprint signupBlueprint

It will create a file in the src/blueprints directory, that after editing would
look like this:

from libsodium import Blueprint

signupBlueprint = Blueprint([
('username', str),
('password', str)
])

Now in our updated route:

from libsodium import Route, useBlueprint
from src.blueprints import signupBlueprint
def route():
    @useBlueprint(signupBlueprint)
    class signup:
        def __init__(self, request):
            create_account(request.form['username'], request.form['password'])
    
    return Route('POST', '/signup', signup)

In the sinario above it doesn't save alot of time, but as your requests get
bigger, the benifits of blueprinting become clear.
"""
class Blueprint:
    def __init__(self, blueprint:list):
        for i in blueprint:
            if not isinstance(i, tuple):
                raise Exception("The blueprint provided had a rule that was not a tuple.")
            if len(i) > 2:
                raise Exception("The blueprint provided had a rule that contained too much info")
        self.blueprint = blueprint

class Rule:
    def __init__(self, typ, **kwargs) -> None:
        self.typ = typ
        self.regex = kwargs.get("regex")
        self.min = kwargs.get("min")
        self.max = kwargs.get("max")
        
class JWT:
    def __init__(self, jwt) -> None:
        self.jwt_original = jwt
        try:
            self.header = json.loads(base64.urlsafe_b64decode(jwt.split(".")[0]+"=="))
            self.body = json.loads(base64.urlsafe_b64decode(jwt.split(".")[1]+"=="))
        except Exception as e:
            raise Exception(f"JWT could not be created due to issue with string, {e}")

def useBlueprint(b, mimetypes):
    def decorator(aclass):
        @wraps(aclass)
        def wrapper(*args,  **kwargs):
            def blueprint(self):
                return b, mimetypes 
            aclass.blueprint = blueprint
            return aclass
        return wrapper()
    return decorator

def useAuthorization(jwt, **kwargs):
    def decorator(aclass):
        @wraps(aclass)
        def wrapper(*args):
            def auth(self):
                return jwt, kwargs 
            aclass.auth = auth
            return aclass
        return wrapper()
    return decorator
