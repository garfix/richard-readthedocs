# Prepositional phrases

An example prepositional phrase is "south of the Equator" in "The countries south of the Equator". The preposition is "south of". Usually it is just a single word like "in" or "after". Prepositions are relations between entities.

A prepositional phrases modifies a noun phrase, that is, it restricts the range of the instances of the np to a smaller set.

## Simple prepositional phrases

~~~python
{
    "syn": "pp(E1) -> preposition(E1, E2) np(E2)",
    "sem": lambda preposition, np: apply(np, preposition)
},
{
    "syn": "preposition(E1, E2) -> 'in'",
    "sem": lambda: [("in", E1, E2)]
},
{
    "syn": "preposition(E1, E2) -> 'of'",
    "sem": lambda: [("of", E1, E2)]
}
~~~

## Idioms

~~~python
{
    "syn": "pp(E1) -> 'south' 'of' np(E2)",
    "sem": lambda np: apply(np, [('south_of', E1, E2)])
}
~~~

## negation

Like "not south of the Equator"

~~~python
{
    "syn": "pp(E1) -> 'not' pp(E1)",
    "sem": lambda pp: [('not', pp)]
}
~~~

## Prepositional phrases with AND

~~~python
{
    "syn": "pp(E1) -> pp(E1) 'and' pp(E1)",
    "sem": lambda pp1, pp2: pp1 + pp2
}
~~~
