# Tokenization and parsing

Before we get into semantics, we need to learn about tokens and parse trees.

A __tokenizer__ breaks a sentence up into smaller parts, __tokens__, that form the input to the parser. As example sentence let's take "John loves Mary". Our basic tokenizer cuts up the sentence into the tokens `John`, `loves`, and `Mary`. It does this by collecting all letter-groups of the sentence, using a regular expression.

A __parse tree__ is a tree-representation of a sentence. This __syntactic__ representation is based on the hierarchical nature of language: a sentence is a compound of phrases, and these phrases are themselves composed of other phrases. A __parser__ parses a sentence to form such a tree. It uses __rewrite rules__ to transform the root node "s" into the branches "np" and "vp". These branches are then themselves rewritten into new branches. It's a recursive process that ends in the words of the sentence.

To see this in action, copy this sample script and run it.

~~~python
from richard.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.block.FindOne import FindOne

def parser_demo():

    grammar = [
        { "syn": "s(V) -> np(E1) vp(V, E1)" },
        { "syn": "vp(V, E1) -> verb(V) np(E1)" },
        { "syn": "np(E1) -> noun(E1)" },
        { "syn": "noun(E1) -> proper_noun(E1)" },
        { "syn": "proper_noun(E1) -> 'john'" },
        { "syn": "proper_noun(E1) -> 'mary'" },
        { "syn": "verb(V) -> 'loves'" },
    ]

    tokenizer = BasicTokenizer()
    parser = BasicParser(grammar, tokenizer)

    pipeline = Pipeline([
        FindOne(tokenizer),
        FindOne(parser)
    ])

    request = SentenceRequest("John loves Mary")
    pipeline.enter(request)

    tree = parser.get_tree(request)
    print(tree)


if __name__ == '__main__':
    parser_demo()

~~~

The variables `E1` and `V` that you see after each category within brackets, help to integrate the semantics of child nodes with their parent. In this syntax example they are not important.

Something about the choice of the rewrite rules that form the grammar: these rules, like `vp -> verb np`, are not the only ones possible. Linguistic frameworks have multiple ways of decomposing a sentence. Read [Wikipedia on Grammar](https://en.wikipedia.org/wiki/Grammar) for more information. We'll be using a variant of [X-bar theory](https://en.wikipedia.org/wiki/X-bar_theory) as it suits the composition of semantics well. But other types of grammar may be used as well.

You may be missing a lexicon in this example. A __lexicon__ is a collection of all the individual words of a language, together with their meanings. This library integrates the lexicon in the grammar to simplify the definition of idioms.

When you run the script, you should see the following parse tree representation.

~~~
s
+- np
|  +- noun
|     +- proper_noun
|        +- john 'John'
+- vp
   +- verb
   |  +- loves 'loves'
   +- np
      +- noun
         +- proper_noun
            +- mary 'Mary'
~~~

This library uses [Earley's parser](https://en.wikipedia.org/wiki/Earley_parser), which is fast and efficient, and doesn't fall into infinite recursion with left-recursive rules (i.e. `a -> a b`).
