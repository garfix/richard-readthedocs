# Noun phrases

## Nouns

A `noun` descibes an entity. The meaning of the word "rivers" is formed by the identifiers (ids) of all river entities in the model.

~~~python
{ 
    "syn": "noun -> 'rivers'", 
    "sem": lambda: 
            lambda: model.get_instances('river') 
}
~~~

## Simple N-bars

An `nbar` (originally an n with a bar above it, or n') represents the unqualified part of the `np`. When it rewrites to a `noun`, it's just the meaning of the noun.

~~~python
{ 
    "syn": "nbar -> noun", 
    "sem": lambda noun: lambda: noun() 
}
~~~

## Noun phrases with determiners

An `np` is a phrase that describes and entity, with an explicit or implicit determiner. Example are "every man", "the block", "at least 3 dogs", or just a name ("Afghanistan").

The meaning of the np is a function created by the `create_np`. It uses `nbar` to produce instances and `det` to check if the number of instances is correct, once applied to a verb.

~~~python
{ 
    "syn": "np -> det nbar", 
    "sem": lambda det, nbar:  
            lambda: create_np(det, nbar) 
}
~~~

The determiner `det` is explained in [Determiners](determiners.md)


## Attributes

In the sentence "What is the capital of Upper Volta?", "capital of" is an `attribute`. An attribute is not a syntactic category in the classic sense. "capital" would be a noun and "of" a preposition. However, the meaning of the sentence can only be understood if we combine these two to a single group. An attribute is a 2-place predicate where the second argument holds the `entity instance` and the first argument the `attribute value` of that entity.

For example: `capital_of(ouagadougou, upper_volta)`

~~~python
{ "syn": "nbar -> attr 'of' np", "sem": lambda attr, np: lambda: model.find_attribute_values(attr, np) },
{ "syn": "attr -> 'capital'", "sem": lambda: lambda: 'capital-of' },
~~~

## Superlatives

Words like "largest" are superlatives. They produce the entity that scores highest/lowest in some attribute. The algorithm is:

- for each identity, find some attribute value
- find the highest/lowest attribute value
- return the id of the entity with that attribute value

~~~python
{ 
    "syn": "nbar -> superlative nbar", 
    "sem": lambda superlative, nbar: lambda: superlative(nbar) 
},
{ 
    "syn": "superlative -> 'largest'", 
    "sem": lambda: lambda range: model.find_entity_with_highest_attribute_value(range, 'size-of') 
}
~~~

The result is a range with a single entity id.
