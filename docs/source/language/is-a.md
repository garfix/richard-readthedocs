# Is a

With language you can define new concepts using the construct "is a".

It may be a class, like this, where "dog" and "Brumby" are introduced:

    A dog is a mammal
    A Brumby is a horse

or a single instance, like this, where "Fido", "Magnesium" and "Blue" are new:

    Fido is a dog
    Magnesium is a metal
    Blue is a color

Implementing these relations is more complex than it would appear because:

* A concept has both an entity aspect ("blue is a color") and a relation aspect ("the box is blue")
* New concepts should be added to the grammar as nouns. Check if already exists. Adding rules to the grammar at runtime is otherwise quite rare.
* A new identifier must be created for the concept's entity (perhaps not just its name, because of possible homonimity)
* A new table needs to be created for the relation of a concept. Check if already exists.
* Some instances are common nouns ("magnesium", "blue") while other instances are proper nouns ("Fido")
* Some of the nouns should also be usable as adjectives ("blue coat"); this may require that adjectives are derived from nouns
* Homonimy (a word with multiple meanings, i.e. "bat", "bank") cannot be handled this way

The concept should be learned in a way that makes it usable for following interactions.

Learning a class should allow

* using it as a noun ("A dog is a mammal" => "small dogs"): add a relation (table), add a grammar rule (noun)

Learning an instance should allow

* using it as a noun ("Blue is a color" => "the sky is blue"): add a relation (table), add a grammar rule (noun)

## Class is-a

While is-a for classes can be implemented as a rule (`mammal(E1) :- dog(E1).`), these rules can only be applied to instances, it can't be used to reason about class inheritance. Using the relation `isa` allows reasoning about both instances and classes.

~~~python
{
    "syn": "s() -> a() common_noun(E1) 'is' a() common_noun(E2)",
    "sem": lambda common_noun1, a2, common_noun2: [('store', [('isa', common_noun2[0], common_noun1)])],
    "inf": [("format", "canned"), ("format_canned", "I understand")],
},
~~~

This rule uses a `common_noun` rule, that contains the relation as its meaning, learns a new lexical entry (in the form of a grammar rule), and creates a relation (table).

~~~python
{ "syn": "common_noun(E1) -> token(E1)", "sem": lambda token: [ (token, E1) ],
    "exec": lambda token: [
    ('learn_grammar_rule', { "syn": f"common_noun(E1) -> '{token}'", "sem": lambda: [(token, E1)] }),
    ('add_relation', token, ['id']),
] },

~~~

## Instance is-a

Similarly, is-a for instances can be implemented as a tuple (`dog('fido')`), but this makes it impossible to reason about class inheritance involving both instances and classes. If the latter is needed, use the relation `isa` here as well.

~~~python
{
    "syn": "s() -> proper_noun(E1) 'is' a() common_noun(E2)",
    "sem": lambda proper_noun, a, common_noun: [('store', [('isa', proper_noun[0], common_noun)])],
    "inf": [("format", "canned"), ("format_canned", "I understand")],
},
~~~

The id of the class can be found or created like this:

~~~python
{ "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: [('resolve_name', token, E1)] },
~~~
