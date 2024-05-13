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


def parser_demo():

    grammar = [
        { "syn": "s -> np vp" },
        { "syn": "vp -> verb np" },
        { "syn": "np -> noun" },
        { "syn": "noun -> proper_noun" },
        { "syn": "proper_noun -> 'john'" },
        { "syn": "proper_noun -> 'mary'" },
        { "syn": "verb -> 'loves'" },
    ]

    tokenizer = BasicTokenizer()
    parser = BasicParser(grammar, tokenizer)

    pipeline = Pipeline([
        tokenizer,
        parser
    ])

    request = SentenceRequest("John loves Mary")
    pipeline.enter(request)

    tree = parser.get_tree(request)
    print(tree)


if __name__ == '__main__':
    parser_demo()
~~~

Something about the choice of the rewrite rules that form the grammar: these rules, like `vp -> verb np`, are not the only ones possible. Linguistic frameworks have multiple ways of decomposing a sentence. Read [Wikipedia on Grammar](https://en.wikipedia.org/wiki/Grammar) for more information. We'll be using a variant of [X-bar theory](https://en.wikipedia.org/wiki/X-bar_theory) as it suits the composition of semantics well. But other types of grammar may be used as well.

You should see the following parse tree representation.

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


