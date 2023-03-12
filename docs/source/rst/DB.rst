Database support using Sqlalchemy
=================================
If you have been in the API industry for more then 5 minutes you know that 
databases using raw sql querries can get messy and usualy lead to 
unnesesary complications that eventualy will bugs that would be near
imposible to track down. But there's an unavoidable solution, the ORM.

Worst Case Sinario
==================
Most people in the tech industry know that you can use code to execute SQL
to retrive data, like shown below:

.. code-block:: python3 

   querry = "SELECT * FROM PEOPLE WHERE ID=10"
   myquerry = mysql.execute(querry)
   print(f"The person with the ID of 10's name is: {myquerry[0]['first_name']}")

While for simple projects this will do, but when you start scaling up your
projects to enterprise levels. Suddenly you have 1000s of API routes and 
actions that are relied on by many and if those systems fail, the damage
would be extrodinary. Then one day you miss the memo and the database team
renames the "first_name" column to "firstName". Now suddenly all of your 
endpoints that rely on the first_name column start sending errors to your
clients. What seems like a simple problem, becomes an instant nightmare.
To fix a problem like this you would have to find all the failing 
endpoints, re-write the code to work in the new database which could mean
re-writing thousands of SQL querries taking lots of hours of potential
productivity.

A simple solution
=================
Lets say you built a time machine to tell yourself how to avoid this
madness, what would you say? If your read the title you know we're talking
about an ORM. Below is a code snippet for what an ORM does.


.. code-block:: python3

   #File: Owner.py
   from base import Base
   from libsodium.db import Column, Integer, String, relationship
   class Owner(Base):
       __tablename__ = 'owner'
       id = Column(Integer, primary_key=True)
       first_name = Column(String(50))
       last_name = Column(String(50))
       accs = relationship('Bank_Account', backref="owner")
       

.. code-block:: python3

   #File: Bank_Account.py
   from base import Base
   from libsodium.db import Column, Integer, ForeignKey

   class Bank_Account(Base):
       __tablename__ = 'bank_account'
       id = Column(Integer, primary_key=True)
       balance = Column(Integer)
       owner_id = Column(Integer, ForeignKey("owner.id"))


Now, while we had to define our database schema twice if the same sinario
happens to us again, we just make the first_name a mapping of the 
firstName column and on top of that we can find the places that the code 
have to be editied much easier thanks to OOP being a part of the language.
With an ORM we can first put in a temporary fix aswell as be able to fix
all affected areas much faster then re-writing complex SQL querries.

DB support in Sodium
====================
Under the hood sodium uses a varient of sqlalchemy with a simple wrapper
arround it allows us to organize our models across multiple files. So lets
get started.

To create a model in sodium use the following command:

For **Linux or Mac OS** users:

.. code-block:: sh

   python3 -m libsodium create model Human 

For **Windows** users:

.. code-block:: sh

   python -m libsodium create model Human 

Now if we open the Human.py file located in src/models we will see this
boilerplate:

.. code-block:: python3

   from base import Base
   from libsodium.db import Column, Integer

   class Human(Base):
       id = Column(Integer, primary_key=True)

As you can see it automaticly creates the id column for us and imports
the essentials to create a model. Lets start by adding a first_name and
a last_name field:

.. code-block:: python3

   from base import Base
   from libsodium.db import Column, Integer, String

   class Owner(Base):
       __tablename__ = 'owner'
       id = Column(Integer, primary_key=True)
       first_name = Column(String(10))
       last_name = Column(String(10))


As you can see, we had to import the string datatype and we can add a
number as an argument that serves as the maximum legnth. Now lets spice
this up by adding a sql relationship to our data. Below is the updated code:

.. code-block:: python3

   from base import Base
   from libsodium.db import Column, Integer, String

   class Owner(Base):
       __tablename__ = 'owner'
       id = Column(Integer, primary_key=True)
       first_name = Column(String(10))
       last_name = Column(String(10))
       accs = relationship('Bank_Account', backref="owner")

.. code-block:: python3

   from base import Base
   from libsodium.db import Column, Integer, ForeignKey

   class Bank_Account(Base):
       __tablename__ = 'bank_account'
       id = Column(Integer, primary_key=True)
       balance = Column(Integer)
       owner_id = Column(Integer, ForeignKey("owner.id"))
      
If you havent noticed by now, this is bacic SQLAlchemy. To
learn more about this database, I would strongly suggest
learning SQLAlchemy, and it should all fit in perfectly.
