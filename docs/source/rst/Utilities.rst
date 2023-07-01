Helper Utilities:

.. note:: 

   .. code-block:: python3
      def libsodium.utils.render(templatename, **kwargs):
      
   
   Wrapper for the jinja2 templating engine

   Usage: libsodium.utils.render("test.html", param1="world")


.. note:: 

   .. code-block:: python3
      def libsodium.utils.seconds(time):
   Adds the ammount of seconds too the current time to create an
   expiration date.

   Usage: libsodium.utils.seconds(60*60*24*30) 
