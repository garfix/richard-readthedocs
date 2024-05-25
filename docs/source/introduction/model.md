# Model and Database

A grammar could talk to a database directly, but this would put much of the complexity in the grammar, and it is of itself already a source of complexity. It would also make it impossible to reuse the grammar in other domains.

This library puts a layer between the application and the database: the model. The model contains the domain-entities and relations. It's given an application-specific adapter: the Model adapter. The adapter talks to one or more data sources, which can take any form tabular data, most commonly a database. 

![Layers](../images/layers.drawio.png)

Each layer has its own language. The grammar has natural language (English, French). The model has the domain language of relations and entities, which are here expressed in English, but any other language is fine. The data sources each have their own naming conventions.

## Model: domain and interpretation

We won't use formal logic, but we will borrow its idea of a model. A __model__ represents part of reality. It has a __domain__, some entities, relations and attributes, and an __interpretation__. The domain contains a number of instances (things). Relations and attributes specify how the instances in the domain interact. The interpretation is a function that maps the entities and relations to the domain.

In this library, the domain is formed by the rows in a database, the files of a file system, or any other piece of data. The interpretation is formed by functions that map an entity or relation to the id's in a database, to filenames, or any other identifier.

The grammar uses the model as an abstraction to decouple it from the database.

__entities__, or in linguistic literature: __sorts__, are the basic concepts of a model: users, customers, persons, products, orders, fields, groups, blocks, etc. Each entity is part of another entity, which is called its parent. For example: a town is a place; a customer is a person; a pyramid is a block. Thus, entities form a __hierarchy__. They are the meaning of nouns.

__relations__ are connections between entities: borders, is_behind, is_taller. Relations take 2 or more entity arguments. They provide the meaning of verbs and relational expressions.

__attributes__ express the special has-a relationship that exists between an entity and some characteristic: parent-of, capital-of, size-of, location-of. It take exactly two arguments. The first is the attribute value, the second the entity instance. They provide the meaning of propositional phrases.

__modifiers__ restrict the range of entities: red, european, big. They are the meaning of adjectives.

It's good to make these concepts explicit at the start of a new application. Give them names that are used by the people that work with the application, rather than, say, the names used in the database, though there will be a large overlap.

## Model adapter

The model has a generic part and a domain-specific part. The latter is implemented by you in the form of a ModelAdapter. It is passed to the model in the constructor.

Here's a model definition for the Chat-80 demo, with its entities and relations.

~~~python
class Chat80Adapter(ModelAdapter):
    def __init__(self) -> None:
        super().__init__(
            attributes=[
                Attribute("size"),
                Attribute("capital"),
                Attribute("location")
            ],
            entities=[
                Entity("river", []),
                Entity("country", ["size", "capital", "location"]),
                Entity("city", ["size"]),
            ], 
            relations=[
                Relation("borders", ['country', 'country']),
            ], 
        )

model = Model(Chat80Adapter())
~~~


The adapter also implements the interpretations that map the domain-relations to the database (data source) names.

This is the interpretation function for relations:

~~~python
def interpret_relation(self, relation_name: str, values: list[Simple]) -> list[list[Simple]]:
~~~

It is passed a relation name and the argument values, and it expects a list of records (`list[Simple]`) that match the arguments.

Here's an sample implementation:

~~~python
def interpret_relation(self, relation_name: str, values: list[Simple]) -> list[list[Simple]]:
    columns = []
    if relation_name == "borders":
        table = "borders"
        columns = ["country_id1", "country_id2"]

    return ds.select(table, columns, values)
~~~

As you can see, it maps model names to data source names and passes the request on to the data source.

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

To add a new data source, copy an existing one that best looks like the one you need, and make changes to it.

## Model access in the grammar

With this database access from the model in place, we can access the model from the grammar:

~~~python
[
    { 
        "syn": "noun -> 'parent'", 
        "sem": lambda: lambda: model.get_entity_range('parent') 
    },
]
~~~

The meaning of the word `parent` is formed by the range of identities (ids) of all parents in the domain.
