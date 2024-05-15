# Database access

The library can use databases to store data. Currently it supports:

* PostgreSQL
* MemoryDb, a simple in-memory store

More databases will be added later.

## The Record and RecordSet

Natural language systems that create complicated SQL queries are either very complicated to build and maintain, or very restricted in their expressiveness. Furthermore, many sentences can't be expressed in a single query at all. This library opts for the other extreme: it supports only three simple operations on a database:

* assert a single record (insert a row into a table) 
* retract records (delete a selection of records from a table)
* select records (list a selection of records)

The terms __assert__ and __retract__ are taken from the domain of knowledge bases.

You will find that the library performs many simple queries, most of which are like this: "SELECT * FROM <table> WHERE <a> = <x> AND <b> = <y>"

A __record__ (class Record) is a combination of a table name and a dictionary of key/values. A record can be written to, deleted from and selected from any database. It's a named tuple.

A __record set__ is a set of records. A set is different from a list in that each item can only occur once.

Example:

    Record('has_child', {'parent': 'mary', 'child': 'lucy'})

This record is a tuple of the relation `has_child` with attributes `parent` and `child`. It can be stored in a database as a row in table "has_child" with the columns `parent` and `child`.

