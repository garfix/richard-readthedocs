# Is a

With language you can define new concepts using the construct "is a".

It may be a class, like this, where "dog" and "Brumby" are introduced:

    A dog is a mammal
    A Brumby is a horse

or a single instance, like this, where "Fido", "Magnesium" and "Blue" are new:

    Fido is a dog
    Magnesium is a metal
    Blue is a color

The examples below are part of the SIR demo.

## Class is-a

While is-a for classes can be implemented as a rule (`mammal(E1) :- dog(E1).`), these rules can only be applied to instances, it can't be used to reason about class inheritance. Using the relation `isa` allows reasoning about both instances and classes.

~~~python
{
    "syn": "s() -> a() common_noun_name(E1) 'is' a() common_noun_name(E2)",
    "sem": lambda common_noun_name1, a2, common_noun_name2: [('store', [('isa', common_noun_name1, common_noun_name2)])],
},
~~~

This rule uses a `common_noun_name` rule, that contains the relation as its meaning.

~~~python
{
    "syn": "common_noun_name(E1) -> /\w+/", "sem": lambda token: token
}
~~~

## Instance is-a

Similarly, is-a for instances can be implemented as a tuple (`dog('fido')`), but this makes it impossible to reason about class inheritance involving both instances and classes. If the latter is needed, use the relation `isa` here as well.

~~~python
{
    "syn": "s() -> proper_noun(E1) 'is' a() common_noun_name(E2)",
    "sem": lambda proper_noun, a, common_noun_name: proper_noun + [('store', [('isa', E1, common_noun_name)])]
},
~~~

The id of the class can be found or created like this:

~~~python
{ "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: [('resolve_name', token, E1)] },
~~~

## Deductions with is-a

If Jane is a girl, and a girl is a person, then Jane is a person. If a person has two hands, then Jane has two hands. Deductions like this can be implemented using inference rules.

But what about the other way around? Is a person a girl? Sometimes, you could say. This means that is-a questions are not only used from specific to generals, but from generals to specifics as well.

The same sentence ("Is X an Y?") might have both interpretations. Sentences with multiple interpretations can be handled with a `switch` format.

~~~python
{
    "syn": "s(E3) -> 'is' a() common_noun_name() a() common_noun_name()~'?'",
    "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('two_way_instance_of', common_noun_name1, common_noun_name2, E3)],
    "dialog": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
            ("format_switch_value", 'sometimes', 'Sometimes'),
            ("format_switch_value", 'yes', 'Yes')
        ],
}
~~~

## Further considerations

Some thoughts that might occur when dealing with the introduction of new concepts in a dialog:

* A concept has both an entity aspect ("blue is a color") and a relation aspect ("the box is blue")
* New concepts could be added to the grammar as nouns. Check if already exists. Adding rules to the grammar at runtime is otherwise quite rare.
* A new identifier could be created for the concept's entity (perhaps not just its name, because of possible homonimity)
* A new table could be created for the relation of a concept. Check if already exists.
* Classes are common nouns ("magnesium", "blue") while instances are proper nouns ("Fido")
* Some of the nouns should also be usable as adjectives ("blue coat"); this may require that adjectives are derived from nouns
* Homonimy (a word with multiple meanings, i.e. "bat", "bank") cannot be handled this way
