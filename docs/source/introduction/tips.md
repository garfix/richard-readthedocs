# Tips for building a grammar

## Efficiency: less rules is better

A good rule-of-thumb when building a grammar is that less rules is better. This rule has two aspects.

When you start to build a grammar you can get the urge to make the grammar as flexible as you can by creating a big number of rewrite rules. Control this urge. Making a rule more flexible later is easy to do. Simplifying with a rule set that doesn't reflect the demands of the domain is much harder. It's no problem at all to start out with a grammar that contains just a single rule to parse a sentence.

    s -> 'what' 'rivers' 'are' 'there' '?'

This is the perfect implementation of the rule: less rules is better.

The other aspect is about efficiency, of course. After you created some grammar rules, and you start to notice the same structures reoccurring, create extra rules that capture this regularity. This will make your grammar grow and become more powerful. After each change, make your tests work again.

The essential point is that there are many ways to make a rule more abstract and flexible starting from one example. But not all of them are equally well. Wait until the patterns present themselves to you.

## Tests may pass by accident

When you add a new sentence to your test suite, the first thought is likely to be: let's first check if it just works. You run the test and find that it either works or that it fails. If you're like me and you see the test pass, you think: "Good! Up to the next one!". After you add some more tests you may find that these start to fail and you don't understand why, because the previous tests passed as well and they're about the same. You find that some tests have <b>passed by accident</b>. This is a common phenomenon, and it happens more in tests with simple anwers like "True", "False", or "OK".

You can deal with the phenomenon by following these rules:

* Plan what the system should do
* Add the rules to make that possible
* Check if the system follows your plan

