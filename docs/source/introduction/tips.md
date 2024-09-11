# Tips for building a grammar

## Efficiency: less rules is better

A good rule-of-thumb when building a grammar is that less rules is better. This rule has two aspects.

When you start to build a grammar you can get the urge to make the grammar as flexible as you can by creating a big number of rewrite rules. Control this urge. Making a rule more flexible later is easy to do. Simplifying with a rule set that doesn't reflect the demands of the domain is much harder. It's no problem at all to start out with a grammar that contains just a single rule to parse a sentence.

    s -> 'what' 'rivers' 'are' 'there' '?'

This is the perfect implementation of the rule: less rules is better.

The other aspect is about efficiency, of course. After you created some grammar rules, and you start to notice the same structures reoccurring, create extra rules that capture this regularity. This will make your grammar grow and become more powerful. After each change, make your tests work again.

The essential point is that there are many ways to make a rule more abstract and flexible starting from one example. But not all of them are equally well. Wait until the patterns present themselves to you.

## Semantic grammar

A semantic grammar is a grammar that contains the names of relations and entities in its syntactic rules. For example

    s -> 'what' 'is' aggregate element 'in' material

The categories `aggregate`, `element` and `material` are not syntactic, like `noun` and `verb`.

This library allows you to create a semantic grammar, and there are good use cases for it. But you must be aware that the grammar you build is very domain-specific and there's a low chance of being able to reuse it in other projects.

Adding some semantic grammar elements to any grammar is normal, however.

## preposition or part of verb?

How should we model "the river that flows from the Rwanda into the ocean"? Is this a single ditransitive verb "flow-from-into", or is the verb simply "flow" and are "from" and "into" to be modelled as prepositions?

## Events

An event is an identifier of a predication that makes the predicate time-dependent. When your application uses events, use them for every predicate, even if you don't see the need for it right away. It's hard to add an event to a predicate later.


