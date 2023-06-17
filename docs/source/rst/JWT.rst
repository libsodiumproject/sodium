JWT's in sodium
===============
If your a backend developer, you have probebly heard about JWT's.
JWT's are the defacto standered for dealing with authentication.
In this page we will cover JWT's in soium and how to use them.

Creating a JWT service utility
==============================
To begin, lets start with creating a jwt system in the command line.
It should look something like this:

**Linux/Mac OS users**

.. code-block:: sh

   python3 -m libsodium create utility jwt

**Windows**

.. code-block:: sh

   python -m libsodium create utility jwt

This will launch the jwt service maker, and will promt you to use the key maker utility.

.. NOTE::
    When using ECDSA, please note that the ammount of bits means nothing and can be any positive integer

Using the JWT Factory
=====================
After you create a jwt service utility, we can start to use JWT's.
To create JWT's simply import the userJwtFactory class from 
src.utilities.{name of the service}JwtFactory
It should look something like this:

.. code-block:: python

   from src.utilities.userJwtFactory import userJwtFactory
   from libsodium import seconds
   myfactory = userJwtFactory()
   jwt = myfactory.generateJWT(
    {"this_is_optional":1234},
    scopes=["user.post", "user.logout", "user.delete_acc"],
    sub="12345",
    exp=seconds(60*60*24*30))

.. NOTE::
   makeJwt(payload={}, \**kwargs) => str 


Using the JWT Verifier
======================
So now that we have a safe way to create jwt's, lets verify some.
In sodium we can use the @useAuthorization(verifier) decorator to handle verification.

.. NOTE::
   The @useAuthorization decorator takes the entire verifier module, not the verify function.
   Provide the module that contains the function instead. It would look something like this.

By default the decorator will look for an Authorization: Bearer ... 
in the headers, but you can use cookies by adding cookie="MY COOKIE NAME" to the args.

.. code-block:: python

   from libsodium import Route, Response, useAuthorization
   from src.utilities.userJwtVerifier import userJwtVerifier

   def route():
       @useAuthorization(userJwtVerifier())
       class post:
           def onRequest(self, request):
               create_post(request.json["post"])
               rsp = Response(f'{"code":"success"}')
               rsp.headers['Content-Type'] = 'applicaiton/json'
               return rsp
       return Route('POST', '/post', signup)

.. NOTE::
   This example is not safe, as it uses things that may be nonexistent, refer to the `Blueprints <Blueprints.html>`_ page.
