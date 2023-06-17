==========
Quickstart
==========
After `Installation <Installation.html>`_ you can initialize a project by running some code in the command line.

Creating a project
==================

For **Linux/Mac OS** Users

.. code-block:: sh

   python3 -m libsodium init


For **Windows** Users

.. code-block:: sh

   python -m libsodium init


Writing the code
================
So lets start writing code, cd into the project you just created(the directory is the project name).
To make sure everything is working, lets start the development server:

For **Linux/Mac OS** Users

.. code-block:: sh

   python3 -m libsodium start

   
For **Windows** Users

.. code-block:: sh

   python -m libsodium start


If you followed the steps correctly you should see something like this:

.. image:: /images/sodiumstartup.png

Lets begin by creating a simple **route** named "helloworld" at /

For **Linux/Mac OS** Users

.. code-block:: sh

   python3 -m libsodium create GETRoute helloworld /

   
For **Windows** Users

.. code-block:: sh

   python -m libsodium create GETRoute helloworld /

Lets look in what our **route** looks like, the **route** will be located at src/routes/<routename>/

.. code-block:: python3

   from libsodium import Route, Response

   def route():
       class helloworld:
           def onRequest(self, request):
               rsp = Response(f'<h1>Hello World!</h1>')
               rsp.headers['Content-Type'] = 'text/html'
               return rsp
       return Route('GET', '/', helloworld)


Lets leave the code to the default and run our project:

For **Linux/Mac OS** Users

.. code-block:: sh

   python3 -m libsodium start

   
For **Windows** Users

.. code-block:: sh

   python -m libsodium start


Now if go over to `http://localhost:5000 <http://localhost:5000>`_ it should look something like this:

.. image:: /images/default-web.png

HTTP METHODS
============
If you have been following the guide we have only covered GET requests and any of the other **HTTP methods**.
We create other types of http routes by simply using the create command with one of these parameters.

* GETRoute
* POSTRoute
* HEADRoute
* PUTRoute
* DELETERoute
* OPTIONSRoute
* CONNECTRoute
* TRACERoute

So lets make a simple **Post Route**. We can make a post route by simply running the same command for creating a
get route, just with post instead. It should look something like this:

For **Linux/Mac OS** Users

.. code-block:: sh

   python3 -m libsodium create POSTRoute ping /ping

   
For **Windows** Users

.. code-block:: sh

   python -m libsodium create POSTRoute ping /ping

Now that we have a post route, lets see what it looks like:

.. code-block:: python

   from libsodium import Route, Response

   def route():
       class ping:
           def onRequest(self, request):
               rsp = Response(f'<h1>Hello World!</h1>')
               rsp.headers['Content-Type'] = 'text/html'
               return rsp
       return Route('POST', '/ping', ping)

As you can see, we get the same output for the helloworld route we
created earilier, just with the last line changed to fit the 
parameters we gave to the function.

The "Request/Response" objects
==============================
If you don't know, sodium uses werkzeug under the hood for it's
development server and **Request**/**Response** wrapers. So the
request is just a werkzeug request object. For further info about this
object, go to the `werkzeug <https://werkzeug.palletsprojects.com/en/2.2.x/wrappers/>`_ wrapper documentation.

For now lets go over some basic functionality:

**Request.form**: An immutable dictionary containing form data rasing an error if not provided

**Request.json**: An immutable dictionary containing json data rasing an error if not provided

**Response.headers**:  A dictionary containing the headers

**Response.status_code**: A integer for the status code of the response

POST Route Example
==================
Lets see what we can do with our POST route. Lets start by making the /ping route return the info you sent it.
We can do this easily with the following code:

.. code-block:: python

   from libsodium import Route, Response

   def route():
       class ping:
           def onRequest(self, request):
               try:
                   form = request.form
               except:
                   rsp = Response(f'<h1>form not provided<h1>')
                   rsp.headers['Content-Type'] = 'text/html'
                   return rsp
               rsp = Response(f'<h1>Hello World!</h1><p>{str(form)}</p>')
               rsp.headers['Content-Type'] = 'text/html'
               return rsp
       return Route('POST', '/ping', ping)


.. NOTE::
   The code above is not the recomended way to handle user input. Refer to the `Blueprints <Blueprints.html>`_ page for more info.

Deploying to a WSGI server
==========================
To deploy to a WSGI server, go into your project directory and then open the start.py file.
The varible "MainDeamon" is the WSGI app that you can use. Normaly this is ran by the 
eventlet server but can be ported over to any WSGI server

.. note:: 
   Be varry that if you use the `SocketIO API <Websockets.html>`_ you must use a server 
   that is compatible, check out the 
   `Python SocketIO Documentation <https://python-socketio.readthedocs.io/en/latest/intro.html#server-features>`_
   for more info
