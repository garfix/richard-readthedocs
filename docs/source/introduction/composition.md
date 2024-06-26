# Semantic attachments and composition

The meaning of a sentence or phrase can be composed of the meaning of its constituent phrases. Known as [Frege's principle](https://en.wikipedia.org/wiki/Principle_of_compositionality), this is the basis of deriving the meaning of a sentence.

A grammar rule can be extended with a __semantic attachment__, expressed by the "sem" key, which expresses the meaning of the phrase covered by the rule. In this library the attachments take the form of lists of atoms. The atom is implemented as a Python tuple.

An atom is a combination of a predicate with some arguments. Examples are `('river', E1)`, `('give', E1, E2, E3)`. The arguments may be variables (as in the example) or values.

Most sems are lists of atoms. This allows us to combine sems by simply adding the lists. Sems that don't need to be combinable can just be single atoms, or even simple values.

## Code structure

Here's an example rule that demonstrates a typical 2-part structure of a semantic attachment ("sem"):

~~~python
{ 
    "syn": "noun(E1) -> 'rivers'", 
    "sem": lambda: [('river', E1)] 
},
{ 
    "syn": "s(E1) -> np(E1) vp_no_sub(E1)", 
    "sem": lambda np, vp_no_sub: [('check', E1, np, vp_nosub_obj)]
}
~~~

Notice that "sem" is formed by a lambda function that returns a list of atoms.

The function `lambda np, vp_no_sub: ...` is just needed to import the semantic values of the child nodes. Each child is appointed a parameter with the same name as the syntactic category it belongs to. In the example above, `np` is the first consequent of the rule, and `np` is therefore the name of the first parameter of the outer function. In the same way, `vp_no_sub` is the second consequent, and therefore the second parameter. Only categories need parameters. Words (like `'river'` or `'two'` have no need for a parameter, as they have no child nodes).

The parameter names are not required to be the same as the syntactic categories, but it is good practice to keep them that way. An exception occurs when the rule has two of the same syntactic categories, as in `term -> term operator term`. In this case append a follow-up number, like `lambda term1, operator, term2`.

The returned value `[('check', E1, np, vp_nosub_obj)]` forms the real meaning of the rule. It uses the meanings of its child nodes that were made available through the parameters of the outer function.

## Example script

The example script below takes a simple grammar to show how the composition of the meaning of the sentence.

The semantic composition itself is performed by the __semantic composer__. It composes the meaning of the sentence into a single function. 

~~~python
from richard.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.block.FindOne import FindOne
from richard.constants import E1, E2, EXISTS

def composition_demo():
    grammar = [
        { "syn": "s(E1) -> np(E1) vp(E1)", "sem": lambda np, vp: [('check', E1, np, vp)]},
        { "syn": "vp(E1) -> verb(E1, E2), np(E2)", "sem": lambda verb, np: [('check', E2, np, verb)] },
        { "syn": "verb(E1, E2) -> 'flows' 'to'", "sem": lambda: [('flow', E1, E2)] },
        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: [('quant', E1, det, nbar)] },
        { "syn": "det(E1) -> 'the'", "sem": lambda: EXISTS },
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
        { "syn": "noun(E1) -> 'river'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> 'sea'", "sem": lambda: [('sea', E1)] },
    ]

    tokenizer = BasicTokenizer()
    parser = BasicParser(grammar, tokenizer)
    composer = SemanticComposer(parser)

    pipeline = Pipeline([
        FindOne(tokenizer),
        FindOne(parser),
        FindOne(composer),
    ])

    request = SentenceRequest("The river flows to the sea")
    pipeline.enter(request)
    print(composer.format_tuples(request))


if __name__ == '__main__':
    composition_demo()
~~~

The script composes and prints out the resulting meaning of the sentence. It is a tree-structure composed of atoms:

~~~python
[
    ('check', S1, [
        ('quant', S1, 'exists', [
            ('river', S1)])], [
        ('check', S2, [
            ('quant', S2, 'exists', [
                ('sea', S2)])], [
            ('flow', S1, S2)])])]

~~~

Note how the individual atoms have been composed to a tree of nested atoms. Note also that local variables `E1` and `E2` that reoccur in the rules have been replaced by sentence-wide variables `S1`, `S2` and so on. These variables express the fact that the child variables and the parent variables refer to the same values.

When the composer combines the child sems with the parent sems, it introduces a new sentence variable for each new variable it encounters. When such a variable is used in a child node, the variable is passed on to the child. This mapping is defined by the variables next to the syntactic categories. 

There are many other forms of semantic composition. The one presented here is both relatively easy to learn and yet very expressive. This will become more clear from the examples given in the rest of the documentation.

## Check and quant

Most sems just consist of lists of atoms that can be added together, resulting in bigger lists of atoms. But whenever a new entity is introduced, it needs to be quantified. This adds nesting to the structure. And as it is common for most sentence to be about multiple entities, each of these entities adds a new level of nesting. 

A `check` has a `quant` and a `body`. The `quant` itself consists of a `determiner` and a `range`. In the first `check` of the example above, the determiner is `exists`, and the range `[('river', S1)]`. The body consists of the second check.

In the example above we just see two entities, `S1` and `S2`. Each of them is quantified (by a `quant`) and "checked". Note that the verb of the sentence ("flow") appears only deeply nested inside the structure. The first `check` iterates over the values of `S1`, and passes each of them to the second check. The second `check` iterates over the values of `S2`, and passes both the values of `S1` and `S2` to the body of the check.

In the atom `('check', E1, np, vp)`, the predicate `check` iterates over all entities of the range and passes each of them as argument to the body. If this results in one or more bindings, the entity is added to the result. When this is done, the  determiner checks if the number of entities in the result agrees with the expected amount. If so, all results are returned. If not, no results are returned.

