# Declaratives

A declarative, or statement, enables the user to teach the system new information.

The predicate `store` is available to store a record of information into a table.

~~~python
{
    "syn": "s() -> a() common_noun_name(E1) 'is' a() common_noun_name(E2)",
    "sem": lambda common_noun_name1, a2, common_noun_name2: [('store', [('isa', common_noun_name1, common_noun_name2)])],
},
~~~

## Being critical

The system can be critical in what it accepts as new knowledge. It can check if the new information is not inconsistent with existing information.

An implementation is available in the SIR demo.

Notice that the sem of the sentence doesn't just `store` the preposition, it says that the user "claims" the information.

~~~python
{
    "syn": "s(E3) -> proper_noun(E1) 'is' preposition(E1, E2) proper_noun(E2)",
    "sem": lambda proper_noun1, preposition, proper_noun2: proper_noun1 + proper_noun2 + [('sentence_claim', preposition, E3)],
    "dialog": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
            ("format_switch_value", 'impossible', 'The above statement is impossible'),
            ("format_switch_value", 'ok', 'I understand')
        ],
}
~~~

Only after checking the validity of the information is it actually stored.

~~~prolog
sentence_claim(Atom, "impossible") :- not(check_claim(Atom)).
sentence_claim(Atom, "ok") :- check_claim(Atom), store(Atom).
~~~

