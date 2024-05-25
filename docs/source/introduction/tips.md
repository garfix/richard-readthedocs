# Tips

## About building a grammar

Don't try to be perfect. Don't try to be extensible and complete from the start. In fact, start by making a few lines of grammar that exactly fits the need of the sentence your working on. If the sentence is "What rivers are there?", start with a rule that just says:

    s -> 'what' nbar 'are' 'there' '?'

Note that I replaced "rivers" by `nbar` because that's just a no-brainer. The rest of the words are implemented as literal strings.

Create request/response tests in the form:

- input: "What rivers are there?"
- expected output: ["amazon", "brahmaputra"]

After you created some grammar rules, and you start to notice the same structures reoccurring, create extra rules that capture this regularity. This will make your grammar grow and become more powerful. After each change, make your tests work again.

Once you start abstracting, take a look at the guidelines we made for building a grammar.

## Semantic grammars

A semantic grammar is a grammar that contains the names of relations and entities in its syntactic rules. For example

    s -> 'what' 'is' aggregate element 'in' material

The categories `aggregate`, `element` and `material` are not syntactic, like `noun` and `verb`. 

This library allows you to create a semantic grammar, and there are good use cases for it. But you must be aware that the grammar you build is very domain-specific and there's a low chance of being able to reuse it in other projects.

Adding some semantic grammar elements to any grammar is normal, however.

## Events

If you need events, use them everywhere, and start using them from the start.
