Database support using Sqlalchemy
=================================
If you have been in the API industry for more than 5 minutes you know that 
databases using raw SQL queries can get messy and usually lead to 
unnecessary complications that eventually will cause bugs that would be nearly
impossible to track down. But there's an unavoidable solution, the ORM.

Worst Case Scenario
==================
Most people in the tech industry know that you can use code to execute SQL
to retrieve data, as shown below:

.. code-block:: python3 

   querry = "SELECT * FROM PEOPLE WHERE ID=10"
   myquerry = mysql.execute(querry)
   print(f"The person with the ID of 10's name is: {myquerry[0]['first_name']}")

While for simple projects this will do, but when you start scaling up your
projects to enterprise levels. Suddenly you have 1000s of API routes and 
actions that are relied on by many and if those systems fail, the damage
would be extraordinary. Then one day you miss the memo and the database team
renames the "first_name" column to "firstName". Now suddenly all of your 
endpoints that rely on the first_name column start sending errors to your
clients. What seems like a simple problem, becomes an instant nightmare.
To fix a problem like this you would have to find all the failing 
endpoints, and re-write the code to work in the new database which could mean
re-writing thousands of SQL queries taking lots of hours of potential
productivity.

A simple solution
=================
Let's say you built a time machine to tell yourself how to avoid this
madness, what would you say? Below is a simple example of an ORM.


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


We practically reconstruct the schema of the database but,
when something like a rename happens we would only have to
change 1 line of code.

DB support in Sodium
====================
Under the hood, sodium uses a variant of sqlalchemy with a simple wrapper
around it. This allows us to organize our models across multiple files. So let's
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

As you can see it automatically creates the id column for us and imports
the essentials to create a model. Let's start by adding a first_name and
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
number as an argument that serves as the maximum length. Now let's spice
this up by adding a SQL relationship to our data. Below is the updated code:

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
      
If you haven't noticed by now, this is basic SQLAlchemy. For more information on how SQLAlchemy works
refer to the SQLAlchemy docs.
