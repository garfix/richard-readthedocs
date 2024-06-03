# Prepositional phrases

An example prepositional phrase is "south of the Equator" in "The countries south of the Equator". The preposition is "south of". Usually it is just a single word like "in" or "after". Prepositions are relations between entities.

A prepositional phrases modifies a noun phrase, that is, it restricts the range of the instances of the np to a smaller set.

## Simple prepositional phrases

~~~python
{ 
    "syn": "np -> np pp", 
    "sem": lambda np, pp: 
                create_np(exists, lambda: np(pp)) 
},
{ 
    "syn": "pp -> preposition np", 
    "sem": lambda preposition, np: 
                lambda subject: np(preposition(subject)) 
},
{ 
    "syn": "preposition -> 'south' 'of'", 
    "sem": lambda: 
                lambda e1: lambda e2: model.find_relation_values('south-of', [e1, e2]) 
}
~~~

The first rule shows that a PP modified an NP. The second rule evaluates the rightmost argument of the PP relation. The third rule is the basic relation in the form of a nested function: one function for each argument.

## negation

Like "not south of the Equator"

~~~python
{ 
    "syn": "pp -> 'not' preposition np", 
    "sem": lambda preposition, np: 
                lambda subject: negate(np(preposition(subject))) 
}
~~~

## Relative clause with AND

The `&` set operator is used here to create the intersection of the two `np` sets.

~~~python
{ 
    "syn": "np -> np relative_clause 'and' relative_clause", 
    "sem": lambda np, rc1, rc2: 
                create_np(exists, lambda: np(rc1) & np(rc2)) 
}


