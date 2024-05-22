# Model and Database

This library puts a layer between the application and the database: the model. 

## Model: domain and interpretation

We won't use formal logic, but we will borrow its idea of a model. A __model__ represents part of reality. It has a __domain__, some entities, relations and attributes, and an __interpretation__. The domain contains a number of instances (things). Relations and attributes specify how the instances in the domain interact. The interpretation is a function that maps the entities and relations to the domain.

In this library, the domain is formed by the rows in a database, the files of a file system, or any other piece of data. The interpretation is formed by functions that map an entity or relation to the id's in a database, to filenames, or any other identifier.

The grammar uses the model as an abstraction to decouple it from the database.

__entities__, or in linguistic literature: __sorts__, are the basic concepts of a model: users, customers, persons, products, orders, fields, groups, blocks, etc. Each entity is part of another entity, which is called its parent. For example: a town is a place; a customer is a person; a pyramid is a block. Thus, entities form a __hierarchy__.

__relations__ are connections between entities: borders, has_parent, has_color, is_behind, is_taller.

It's good to make the concepts explicit at the start of a new application. Give them names that are used by the people that work with the application, rather than, say, the names used in the database, though there will be a large overlap.

Here's a simple model definition with its entities and relations.

~~~python
model = Model([
    Entity("customer"),
    Entity("order"),
    Entity("product"),
], [
    Relation("has_order", ['customer', 'order']),
    Relation("contains_product", ['order', 'product']),
])
~~~

## Database access

To make a grammar reusable we don't want it to use a database directly. In stead, we want it to depend on the model which represents the concepts of the application.

The library supports any kind of database access, but has no specific support for any particular database. In the entities and relations of the model you can simply specify what needs to be done to retrieve instances of the entities, and check whether the relations exist.

The following example uses PostgreSQL as example database. 

~~~python
import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(database='richard', host='127.0.0.1', user='patrick', password='test123', cursor_factory=RealDictCursor)

def get_all_ids(table: str):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM " + table)
    return [row['id'] for row in cursor.fetchall()]

model = Model([
    Entity('customer', lambda: get_all_ids('customer')),
    Entity('product', lambda: get_all_ids('inventory_item'))
], [])
~~~

Note that `Entity` contains a function to retrieve the id's of all customers. How you implement it is up to you. In the example we're using a Postgres database to select the id's from a table directly. But the library by no means depends on Postgres, and you can replace the query code to select data from a MySQL database, a Sparql triple store, a csv file, a NumPy array, or whatever suits your needs.

The query to retrieve the ids of all entities is very simple in this example, but you may find you need to join two tables, add a where clause, or even aggregate, to get the result from the database that is expected by the model. We call this __model-database mapping__.

In most examples here we'll use the simple in-memory database because it's easiest for us. Remember that the database in these examples can be replaced by any other data source.

## Model access in the grammar

With this database access from the model in place, we can access the model from the grammar:

~~~python
[
    { 
        "syn": "noun -> 'parent'", 
        "sem": lambda: lambda: model.get_entity_ids('parent') 
    },
]
~~~

The meaning of the word `parent` is formed by the set of identities (ids) of all parents in the model (or database).
