# Major choices

This pages lists some "architectural decisions" best made before starting a project, as their impact is felt in every aspect of development.

## Events

An event is an identifier of a predication that makes the predicate time-dependent. When your application uses events, use an event variable for every predicate, even if you don't see the need for it right away. It's a lot of work to add events to a system later.

~~~python
("touch", E1, E2, E3)
~~~

Here `E1` is the event entity. It can be used to specify its date, for example:

~~~python
("date", E1, '2023-08-02')
~~~

## Open world assumption / closed world assumption

A system adhering the __closed world assumption__ assumes that the model contains all knowledge there is. It proves a fact by looking it up or deducing it. It disproves a fact by being unable to look it up or deducing it.

A system adhering the __open world assumption__ _does not_ assume that the model contains all knowledge there is. It admits that it has incomplete knowledge. It proves a fact by looking it up or deducing it. It disproves a fact by looking up the __negative fact__ or deducing it. When no fact can be deduced, the result is not "no", but "unknown".

The current library uses closed world by default, but is able to work with open world as well. Closed world is conceptually and syntactically easier to develop, but some domains may demand open world. The __Cooper's system__ demo experiments with open world.

## Semantic grammar

A semantic grammar is a grammar that contains the names of relations and entities in its syntactic rules. For example

    s -> 'what' 'is' aggregate element 'in' material

The categories `aggregate`, `element` and `material` are not syntactic, like `noun` and `verb`.

The current library allows you to create a semantic grammar, and there are some good use cases for it. But you must be aware that the grammar you build is very domain-specific and there's a low chance of being able to reuse it in other projects.

Adding some semantic grammar elements to any grammar is normal, however.

