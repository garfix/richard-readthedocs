# Domain

-- To be implemented --

Applications that interact with a single database talk the language of the database. If the database table is called "customer", then this is the table used in the `Record` used in the application. In a Sparql store, the name of the relation may be "http://dbpedia.org/ontology/country" and this will be the table of the record.

The consequence is that the grammar is now tied to the structure and naming of the database.

    { "syn": "noun -> 'parent'", "sem": lambda: lambda: db1.select(Record('person')).field('parent_id') },
    { "syn": "noun -> 'country'", "sem": lambda: lambda: db2.select(Record('http://dbpedia.org/ontology/country')) },   

In applications that use multiple databases, and applications that wish to decouple the domain language from the different table names in the databases, there is the possibility to create a Domain.

## What is the Domain?

The domain language is the language that is used in the company to talk about things. One talks about orders, customers, users, fields, parts, etc. These are the names one would also like to use in the application, and these are the ones that one would to use in the grammar, to make it independent of a specific database. 

Using a domain to hide the details of the databases, looks like this:

    $domain = Domain([
        my_postgres_db,
        my_mem_db,
        my_sparql_db
    ])

    { "syn": "noun -> 'parent'", "sem": lambda: lambda: domain.select(Record('parent')) },
    { "syn": "noun -> 'country'", "sem": lambda: lambda: domain.select(Record('country')) },   

This grammar more reusable.
