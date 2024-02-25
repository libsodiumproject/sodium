Blueprints
==========
Imagine you have a route, let's say /signup. That route requires 3 things username, email, and password.
Now we assume you can save the user to the database by running the create_user(username, email, password).
This may seem simple, but this is where complications arise. The problem is that you need to get their user input.
Now, without any special tools, you would have to check if the user provided a username, email, and password.
It's common knowledge among developers to follow the Don't Repeat Yourself(DRY) design pattern and all of these checks
violate these rules.

What The Heck Is A Blueprint?
=============================
A blueprint will allow you always to get the request in the format **you** define, and handle all the checks for
you.

How to create Blueprints
========================
Below are the simple instructions to use the CLI wizard to make the template for a blueprint.

For **Linux or Mac OS** users:

.. code-block:: sh

   python3 -m libsodium create blueprint signup 

For **Windows** users:

.. code-block:: sh

   python -m libsodium create blueprint signup

.. note::
   The name of the blueprint doesn't have to be the name of the route, though it's **best practice**.


Now that we have created our blueprint, let's take a peek inside:

**file: /src/blueprints/signupBlueprint.py:**

.. code-block:: python3

   from libsodium import Rule 

   class signupBlueprint:
       name = Rule(str, "<regex>")

.. note:: 
   Alternative syntax(**Not Recommended**):

   .. code-block:: python3

      from libsodium import Blueprint

      signupBlueprint = Blueprint([
      ('example', str, "<regex>")
      ])

Long story short, the Rule object contains the datatype and the regex which we can put into class variables.

Example of using regex's

.. code-block:: python3

   from libsodium import Rule 

   class signupBlueprint:
        username = Rule(str)
        email = Rule(str, r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"+'"'+"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*"+'"'+")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
        password = Rule(str)  


.. note:: 
   Alternative syntax(**Not Recommended**):

   .. code-block:: python3

      from libsodium import Blueprint

      signupBlueprint = Blueprint([
      ('username', str)
      ('email', str, r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"+'"'+"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*"+'"'+")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
      ('password', str)  
      ]) 

.. note::
   The regex used for the email can be found `here <https://www.emailregex.com/>`_

Using The Blueprint
===================
Now let's add the blueprint to our route. We can do this by using the useBlueprint decorator.

.. NOTE::
   **libsodium.classes.useBlueprint(Blueprint blueprint, List[str,..] mimetypes)**

Code:

.. code-block:: python

   from libsodium import Route, Response, useBlueprint
   from src.blueprints.postBlueprint import postBlueprint

   def route():
       @useBlueprint(postBlueprint, ["applicaiton/json"])
       class signup:
           def onRequest(self, request):
               create_user(request.json["username"], request.json["email"], request.json["password"])
               rsp = Response(f'{"code":"success"}')
               rsp.headers['Content-Type'] = 'applicaiton/json'
               return rsp
       return Route('POST', '/signup', signup)

And just like that, we have blueprints installed.
