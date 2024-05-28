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

## Verbs, subjects and objects

All quantifiers treat verb predicates as if they have only a single `np` argument. 

In the following code example, `np` represents only the subject of the verb. `vp_no_sub` may produce a one-placed or a two-placed predicate, but at this level we don't know and don't care. At the sentence level every `np` is a `subject`.

~~~python
{ 
    "syn": "s -> 'does' np vp_no_sub '?'",  
    "sem": lambda np, vp_no_sub: lambda: model.filter_entities(np(), vp_no_sub) 
}
~~~

Only when the verb itself is deconstructed, in a `verb-composition-rule` the objects of the verb are added.

~~~python
{ 
    "syn": "vp_no_sub -> tv np", 
    "sem": lambda tv, np: lambda subject: model.filter_entities(np(), tv(subject)) 
}
~~~

This rule builds the verb from its parts, and the parts involve objects: the direct object and the indirect object.

This leads us to the following guideline: within a `verb-composition` rule an `np` arguments represents an `object`, but in all other rules, the `np` argument is a `subject`. 

## Events

An event is an identifier of a predication.

