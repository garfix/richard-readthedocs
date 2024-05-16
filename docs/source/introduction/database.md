# Database access

Natural language access to a database is a common use case. This includes mainly Question-Answering where a user asks for some information, but the database can also be used as a knowledge base to store and retrieve any information.

Currently the library supports:

* PostgreSQL
* MemoryDb, a simple in-memory store

To use PostgreSQL, you'll need to install the psycopg package. More databases will be added later.

## The Record and RecordSet

Natural language systems that create complicated SQL queries are either very complicated to build and maintain, or very restricted in their expressiveness. Furthermore, many sentences can't be expressed in a single query at all. This library chooses the other extreme: it requires only three simple operations on a database:

* insert a single record (insert a row into a table) 
* delete records (delete a selection of records from a table)
* select records (retrieve a selection of records)

You will find that the library performs many simple queries, most of which are like this: "SELECT * FROM a_table WHERE a = x AND b = y". The following classes play an important part in database access:

A __record__ (class Record) is a combination of a table name and a dictionary of key/values. A record can be written to, deleted from and selected from any database. It's a named tuple.

Example:

    Record('has_child', {'parent': 'mary', 'child': 'lucy'})

This record is a tuple of the relation `has_child` with attributes `parent` and `child`. It can be stored in a database as a row in table "has_child" with the columns `parent` and `child`.

A __record set__ is a set of records. A set is different from a list in that each item can only occur once.
