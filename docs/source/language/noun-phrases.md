# Noun phrases

## Nouns

A `noun` descibes an entity. The meaning of the word "rivers" is formed by the identifiers (ids) of all river entities in the model.

~~~python
{
    "syn": "noun(E1) -> 'river'",
    "sem": lambda: [('river', E1)]
}
~~~

## Simple N-bars

An `nbar` (originally an n with a bar above it, or n') represents the unqualified part of the `np`. When it rewrites to a `noun`, it's just the meaning of the noun.

~~~python
{
    "syn": "nbar -> noun",
    "sem": lambda noun: noun
}
~~~

## Noun phrases

An `np` is a phrase that describes an entity, with an explicit or implicit determiner. Example are "every man", "the block", "at least 3 dogs", or just a name ("Afghanistan"). It is the most common phrase structure and it is always used in conjunction with a verb phrase.

The meaning of the np is a __template__, which is a function (in the form of an object). This template is always used as the first parameter of an `apply` call, like this:

~~~python
{
    "syn": "vp_nosub_obj(E1) -> tv(E1, E2) np(E2)",
    "sem": lambda tv, np: apply(np, tv)
}
~~~

Here the meaning of `np` is the template, and it is applied to the `tv`, which means that the `tv` is passed as an argument to the template function to produce the new meaning.

There are a few noun phrases. Each produces a `SemanticTemplate` which takes a single argument: a verb phrase called `Body`. The result of the function uses the `Body` and its child semantics, for example `nbar`.

~~~python
{
    "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
            SemanticTemplate([Body], nbar + Body)
},
{
    "syn": "np(E1) -> det(E1) nbar(E1)",
    "sem": lambda det, nbar:
            SemanticTemplate([Body], apply(det, nbar, Body))
}
~~~

The reason for using an object (`SemanticTemplate`) where a Python function would have been preferable is purely technical. Variable unification requires the variables to be accessible, and they are not accessible from within a Python function.

The determiner `det` is explained in [Determiners](determiners.md)

## Attributes

In the sentence "What is the population of Upper Volta?", "population" is an `attribute`: a property of an entity.

For example: `has_population(upper_volta, E1)`

~~~python
{
    "syn": "attr(E1, E2) -> 'population'",
    "sem": lambda: [('has_population', E1, E2)]
}
~~~

## Superlatives

Words like "largest" are superlatives. They produce the entity that scores highest/lowest in some attribute. The algorithm is:

- for each entity, find some attribute value
- find the highest/lowest attribute value
- return the entity with that attribute value

~~~python
{
    "syn": "nbar(E1) -> superlative(E1) nbar(E1)",
    "sem": lambda superlative, nbar: apply(superlative, nbar)
},
{
    "syn": "superlative(E1) -> 'largest'", "sem": lambda:
            SemanticTemplate([Body], [('arg_max', E1, E2, Body + [('size_of', E1, E2)])])
}
~~~

Here `E1` in `superlative` will hold the entity with the largest value of `size_of`. This is made possible by treating `superlative` as a template that takes `nbar` as an argument.
