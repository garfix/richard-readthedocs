# Model and Database

You could tell the grammar to talk to a database directly, but this would put much of the complexity in the grammar, and it is of itself already a source of complexity. It would also make it impossible to reuse the grammar in other domains.

This library puts a layer between the application and the database: the model. The model contains the relations. It delegates the implementation of the relations through modules. Each model may talk to a data source (possibly more), which can take any form tabular data, most commonly a database. 

![Layers](../images/layers.drawio.png)

Each layer has its own language. The grammar has natural language (English, French). The model has the domain language of relations and entities, which are here expressed in English, but any other language is fine. The data sources each have their own naming conventions.

## Model: domain and interpretation

We won't use formal logic, but we will borrow its idea of a model. A __model__ represents part of reality. It has a __domain__, some entities, relations and attributes, and an __interpretation__. The domain contains a number of instances (things). Relations and attributes specify how the instances in the domain interact. The interpretation is a function that maps the entities and relations to the domain.

In this library, the domain is formed by the rows in a database, the files of a file system, or any other piece of data. The interpretation is formed by functions that map an entity or relation to the id's in a database, to filenames, or any other identifier.

The grammar uses the model as an abstraction to decouple it from the database.

__types__, or in linguistic literature: __sorts__, are the basic concepts of a model: users, customers, persons, products, orders, fields, groups, blocks, etc. Each entity is part of another entity, which is called its parent. For example: a town is a place; a customer is a person; a pyramid is a block. Thus, entities form a __hierarchy__. They are the meaning of nouns.

__relations__ are connections between entities: borders, is_behind, is_taller. Relations take 2 or more entity arguments. They provide the meaning of verbs and relational expressions.

It's good to make these concepts explicit at the start of a new application. Give them names that are used by the people that work with the application, rather than, say, the names used in the database, though there will be a large overlap.

## Sets and instances

Entities find their data in a database. When a record is retrieved from the database, an `Instance` object is created for it. This object looks like this:

~~~python
class Instance:
    entity: str
    id: str
~~~

It contains the name of the entity it belongs to, as well as the id it has in the database.

Other values that were retrieved from the database are used unchanged: a float will stay a float, an int an int, and a string a string.

The library deals with `ordered sets` of instances. In each grouping of instances, each instance occurs only once. Such a set is commonly called a `range`.

## Module

The model has a generic part and a domain-specific part. The latter is implemented by you in the form of a ModelAdapter. It is passed to the model in the constructor.

Here's a module definition for the Chat-80 demo, with its relations.

~~~python
class Chat80Module(SomeModule):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source


    def get_relations(self) -> list[str]:
        return [
            "river", 
            "country", 
            "capital", 
            "borders",
            "resolve_name",
            "of",
            "size-of",
            "where",
        ]


    def interpret_relation(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:

        db_values = self.dehydrate_values(values)
    
        if relation == "river":
            out_types = ["river"]
            out_values = self.ds.select("river", ["id"], db_values)
        elif relation == "country":
            out_types = ["country"]
            out_values = self.ds.select("country", ["id"], db_values)
        elif relation == "capital":
            out_types = ["city"]
            out_values = self.ds.select("country", ["capital"], db_values)
        elif relation == "borders":
            out_types = ["country", "country"]
            out_values = self.ds.select("borders", ["country_id1", "country_id2"], db_values)
        elif relation == "of":
            out_types = ["city", "country"]
            out_values = self.ds.select("country", ["capital", "id"], db_values)
        elif relation == "size-of":
            out_types = ["country", None]
            out_values = self.ds.select("country", ["id", "area"], db_values)
        elif relation == "where":
            out_types = ["country", "place"]
            out_values = self.ds.select("country", ["id", "region"], db_values)
            print(values, out_values)
        elif relation == "resolve_name":
            out_types = [None, "country"]
            out_values = resolve_name(self.ds, db_values)
        else:
            out_types = []
            out_values = []
      
        return self.hydrate_values(out_values, out_types)
    
~~~

The adapter also implements the interpretations that map the domain-names to the database-names (more general: data source names).

## Data sources

A data source provides access to any kind of tabular data. It takes the shape of an adapter that makes the underlaying data available via this standard interface:

~~~python
def select(self, table: str, columns: list[str], values: list[Simple]) -> list[list[Simple]]:
~~~

Read this interface like an SQL select query:

~~~sql
SELECT `columns` FROM `table` WHERE `columns`=`values`
~~~

Note that same columns are both used in the "select" and the "where"
Note that if a value is None, it must be omitted from the "where"

To add a new data source, copy an existing one that best looks like the one you need, and make changes to it. To give you an idea, here's the implementation of `PsycoPg2DataSource`:

~~~python
def select(self, table: str, columns: list[str], values: list[Simple]) -> list[list[Simple]]:

    import psycopg2

    where = "TRUE"
    variables = []
    for column, value in zip(columns, values):
        if value is not None:
            where += f" AND {column}=%s"
            variables.append(value)

    cursor = self.connection.cursor(cursor_factory=psycopg2.extensions.cursor)
    select = ','.join(columns)
    cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
    return [list(row) for row in (cursor.fetchall())]
~~~

## Model access in the grammar

With this database access from the model in place, we can access the model from the grammar:

~~~python
[
    { 
        "syn": "noun(E1) -> 'parent'", 
        "sem": lambda: ('parent', E1)
    },
]
~~~

The meaning of the word `parent` is formed by the range of instances of all parents in the domain.
