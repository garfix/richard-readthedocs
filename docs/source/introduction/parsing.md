# Tokenization and parsing

Before we get into semantics, we need to learn about tokens and parse trees.

A __tokenizer__ breaks a sentence up into smaller parts, __tokens__, which form the input to the parser. As an example sentence let's take "John loves Mary". Our basic tokenizer cuts up the sentence into the tokens `John`, `loves`, and `Mary`. It does this by collecting all letter-groups of the sentence, using a regular expression.

The __BasicTokenizer__ splits a string up in words (combinations of letters, digits and underscores) and other non-space characters. Each non-space character is turned into a separate token. If you need a different a different way of tokenization, create a sublass of the BasicTokenizer, have it tokenize a string in the way you want, and use this in stead.

A tokenizer, like any processor, can even produce multiple products. A tokenization process that yields multiple tokenizations implements a form of ambiguity, but I don't know of any use cases.

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
    product: BasicParserProduct = pipeline.enter(request)
    tree = product.parse_tree
    print(tree)


if __name__ == '__main__':
    parser_demo()

~~~

The variables `E1` and `V` that you see after each category within brackets, help to integrate the semantics of child nodes with their parent. You will see how they are important when we get to semantics.

Something about the choice of the rewrite rules that form the grammar: these rules, like `vp -> verb np`, are not the only ones possible. Linguistic frameworks have many ways of decomposing a sentence. Read [Wikipedia on Grammar](https://en.wikipedia.org/wiki/Grammar) for more information. I have not yet found a grammar that fits all purposes, and I will be using slightly different grammar rules throughout this documentation. You may look at [X-bar theory](https://en.wikipedia.org/wiki/X-bar_theory) as matches my approach best. But other types of grammar may be used as well.

An important characteristic of a grammar for a semantic parser is that there are many rewrite rules at the sentence level. The results that a sentence produces largely depend on the top-level construct of a sentence.

This library uses [Earley's parser](https://en.wikipedia.org/wiki/Earley_parser), which is fast and efficient, and doesn't fall into infinite recursion with left-recursive rules (i.e. `a -> a b`).

You may be missing a lexicon in this example. A __lexicon__ is a collection of all the individual words of a language, together with their meanings. This library integrates the lexicon in the grammar to simplify the definition of idioms. An __idiom__ is a group of words that does not form a phrase but contains a specific meaning. For example: "How many countries have population above 100 million?"

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

