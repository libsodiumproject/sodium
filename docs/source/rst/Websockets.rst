SocketIO And Websockets
=======================
As of libsodium v2.50 SocketIO has been integrated into the WSGI server that libsodium runs on.
This allows the developer to reap the benefits of websockets while having added support for
working multiple clients via the SocketIO library. 

Tutorial
========
If you go to src/websockets you will find a file called "app.py" this will contain the SocketIO
application.

file: app.py

.. code-block:: python

   from socketio import Server
   sio = Server()
   
This file is auto-imported by libsodium engine and is the SocketIO app that it connects to.
We can use this file to create event handlers for certain SocketIO events.

file: test.py

.. code-block:: python

   from src.websockets.app import sio

   @sio.on('echo')
   def echo(sid, message):
       sio.emit('echo', message)

This code will echo back a message sent by a client, lets say javascript.

.. code-block:: javascript

   import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js";
   var socket = io();

   socket.emit("echo", "Hello")

   socket.on('echo', function(msg) {
        console.log("Reply From Server:" + msg)
   })

For more complex topics refer to the 
`Python SocketIO Documentation. <https://python-socketio.readthedocs.io/en/latest/>`_
