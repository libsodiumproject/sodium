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

Using the JWT Printer
=====================
After you create a jwt service utility, we can start to use JWT's.
To create JWT's simply import the makeJwt function from src.utilities.{name of the service}JwtPrinter
It should look something like this:

.. code-block:: python

   from src.utilities.userJwtPrinter import makeJwt

.. NOTE::
   makeJwt(header: Dict, body: Dict) => str 


Using the JWT Verifier
======================
You can verify jwt's sodium using the **@useAuthorization** decorator.
The decorator takes the verifier module, **not the verify function** the **module**.
This will automaticly filter all trafic with invalid/nonexistent JWT's on the route that
it's applied on.

.. NOTE::
   You can use this decorator with other decorators, though it's best practice to put this decorator at the bottom.
   
