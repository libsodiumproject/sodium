gRPC with Sonora
================
In libsodium v2.50 the gRPC API was added. This works by connecting the WSGI
application with a gRPC server using the sonora package. This allows for
having a gRPC application running underneath a http service on the same 
socket. 

Generating code for protobufs
=============================
If you go to src/gRPC you will see a folder named "protobufs". This folder
contains all the protobufs in the project. Lets create one inside the folder.

file: hello.proto

.. code-block:: protobuf

   // The greeting service definition.
   service Greeter {
     // Sends a greeting
     rpc SayHello (HelloRequest) returns (HelloReply) {}
   }

   // The request message containing the user's name.
   message HelloRequest {
     string name = 1;
   }

   // The response message containing the greetings
   message HelloReply {
      string message = 1;
   }


Now to create the files for the protobuf instead of using the grpc toolchain
directly we can use the libsodium wrapper.

.. code-block:: zsh

   python3 -m libsodium create gRPC hello.proto

If you look in the src/gRPC directory now you will see that there is a new
folder named after our protofile(hello). This folder will contain the
classic gRPC files but with one extra file named hello.py. This file will
be our service. 

.. code-block:: python3

   import src.gRPC.hello.hello_pb2_grpc as hello_pb2_grpc 

   def serve(server):
       hello_pb2_grpc.add_ExampleServicer_to_server(
           AppServicerHere(), server
       )

As you can see we get a template for implementing a servicer from
our proto file. Here is the fully completed version of the file.

.. code-block:: python3

   import src.gRPC.hello.hello_pb2_grpc as hello_pb2_grpc
   from src.gRPC.hello.hello_pb2 import (
       HelloReply
   ) 

   class GreeterService(hello_pb2_grpc.GreeterServicer):
       
       def SayHello(self, request, context):
           return HelloReply(message=f"Hi, {request.name}")        


   def serve(server):
       hello_pb2_grpc.add_GreeterServicer_to_server(
           GreeterService(), server
       )

.. note:: 

   The sonora library only supports HTTP 1.1 as of libsodium version 2.50.

