# Domain and Database

This library puts a layer between the application and the database: the domain. 

## Domain

Every application has its own domain, with its own concepts and names. In natural language processing, we are particularly interested in the entities and relations of the domain. 

A grammar uses the concepts defined in a domain.

__entities__, or more traditionally: sorts, are the basic things of a domain: users, customers, persons, products, orders, fields, groups, blocks, etc. Each entity is part of another entity, which is called its parent. For example: a town is a place; a customer is a person; a pyramid is a block. Entities form a __hierarchy__.

__relations__ are connections between entities: has_parent, has_color, is_behind, is_taller.

It's good to make these concepts explicit at the start of a new application. Give them names that are used by the people that work with the application, rather than, say, the names used in the database, though there will be a large overlap.

Here's a simple domain definition with its entities and relations.

~~~python
domain = Domain([
    Entity("customer"),
    Entity("order"),
    Entity("product"),
], [
    Relation("has_order", ['customer', 'order']),
    Relation("contains_product", ['order', 'product']),
])
~~~

## Database access

To make a grammar reusable we don't want it to use a database directly. In stead, we want it to depend on the domain which represents the concepts used by the application.

The library supports any kind of database access, but has no specific support for any particular database. In the entities and relations of the domain you can simply specify what needs to be done to retrieve instances of the entities, and check whether the relations exist.

The following example uses PostgreSQL as example database. 

~~~python
import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(database='richard', host='127.0.0.1', user='patrick', password='test123', cursor_factory=RealDictCursor)

def get_all_ids(table: str):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM " + table)
    return [row['id'] for row in cursor.fetchall()]

domain = Domain([
    Entity('customer', lambda: get_all_ids('customer')),
    Entity('product', lambda: get_all_ids('inventory_item'))
], [])
~~~

Note that `Entity` contains a function to retrieve the id's of all customers. How you implement it is up to you. In the example we're using a Postgres database to select the id's from a table directly. But the library by no means depends on Postgres, and you can replace the query code to select data from a MySQL database, a Sparql triple store, a csv file, a NumPy array, or whatever suits your needs.

The query to retrieve the ids of all entities is very simple in this example, but you may find you need to join two tables, add a where clause, or even aggregate, to get the result from the database that is expected by the domain. We call this __domain-database mapping__.

In most examples here we'll use the simple in-memory database because it's easiest for us. Remember that the database in these examples can be replaced by any other data source.

## Domain access in the grammar

With this database access from the domain in place, we can access the domain from the grammar:

~~~python
[
    { 
        "syn": "noun -> 'parent'", 
        "sem": lambda: lambda: domain.get_entity_ids('parent') 
    },
]
~~~

The meaning of the word `parent` is formed by the set of identities (ids) of all parents in the domain (or database).
