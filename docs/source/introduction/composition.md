# Semantic attachments and composition

The meaning of a sentence or phrase can be composed of the meaning of its constituent phrases. Known as [Frege's principle](https://en.wikipedia.org/wiki/Principle_of_compositionality), this is the basis of deriving the meaning of a sentence.

It was Richard Montague who first showed that lambda calculus can be used to compose the meaning of a phrase by applying a function on the meanings of its child phrases. This __Montague grammar__ is often used to compose compound predicate logic expressions which are declarative in nature. This library, on the other hand, uses the same principle to create and run executable code.

A grammar rule can be extended with a __semantic attachment__, expressed by the "sem" key, which expresses the meaning of the phrase covered by the rule. In this library the attachments take the form of a Python function.

Here's an example rule that demonstrates a typical 2-part structure of a semantic attachment ("sem"):

    { 
        "syn": "s -> np vp_no_sub", 
        "sem": lambda np, vp_no_sub: 
                    lambda: find(np(), vp_no_sub) 
    },

Notice that "sem" is formed by a nested lambda function. It consists of an _outer function_ that returns an _inner function_. This is a general principle.

The outer function `lambda np, vp_no_sub: ...` is just needed to import the semantic functions of the child nodes. Each child is appointed a parameter with the same name as the syntactic category it belongs to. In the example above, `np` is the first consequent of the rule, and `np` is therefore the name of the first parameter of the outer function. In the same way, `vp_no_sub` is the second consequent, and therefore the second parameter. Only categories need parameters. Words (like `'times'` or `'two'` have no need for a parameter, as they have no semantic attachment).

The parameter names are not required to be the same as the syntactic categories, but it is good practice to keep them that way. An exception occurs when the rule has two of the same syntactic categories, as in `term -> term operator term`. In this case append a follow-up number, like `lambda term1, operator, term2`.

The inner function `lambda: find(np(), vp_no_sub)` forms the real meaning of the rule. It uses the meanings of its child nodes that were made available through the parameters of the outer function.

This example script takes a simple grammar to show how the meaning of the sentence: the result of the calculation, is formed by applying functions. The most basic meaning is formed by functions like `lambda: 1` that yield constants. These functions are passed as parameter to an operator functions like `lambda a, b: a() + b()`. They in turn are passed to term functions, which are recursive (`term -> term operator term`).

The semantic composition itself is performed by the __semantic composer__. It composes the meaning of the sentence into a single function. The __semantic executor__ simply executes this function.

~~~python
from richard.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.processor.semantic_executor.SemanticExecutor import SemanticExecutor
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer


def calculation_demo():
    """
    The example was taken from https://github.com/percyliang/sempre/blob/master/TUTORIAL.md
    """

    grammar = [
        { "syn": "s -> 'what' 'is' term", "sem": lambda term: lambda: term() },
        { "syn": "s -> 'calculate' term", "sem": lambda term: lambda: term() },
        { 
          "syn": "term -> term operator term", 
          "sem": lambda term1, operator, term2: 
                    lambda: operator(term1, term2) 
        },
        { "syn": "operator -> 'plus'",  "sem": lambda:  lambda a, b: a() + b() },
        { "syn": "operator -> 'minus'", "sem": lambda:  lambda a, b: a() - b() },
        { "syn": "operator -> 'times'",  "sem": lambda:  lambda a, b: a() * b() },
        { "syn": "operator -> 'divided' 'by'", "sem": lambda:  lambda a, b: a() / b() },
        { "syn": "term -> 'one'", "sem": lambda: lambda: 1 },
        { "syn": "term -> 'two'", "sem": lambda: lambda: 2 },
        { "syn": "term -> 'three'", "sem": lambda: lambda: 3 },
        { "syn": "term -> 'four'", "sem": lambda: lambda: 4 },
    ]

    tokenizer = BasicTokenizer()
    parser = BasicParser(grammar, tokenizer)
    composer = SemanticComposer(parser)
    executor = SemanticExecutor(composer)

    pipeline = Pipeline([
        tokenizer,
        parser,
        composer,
        executor
    ])

    request = SentenceRequest("What is three plus four")
    pipeline.enter(request)
    print(executor.get_results(request))
    
    request = SentenceRequest("Calculate three plus four times two", find_all=True)
    pipeline.enter(request)
    print(request.get_alternative_products(executor))
    
if __name__ == '__main__':
    calculation_demo()
~~~

By default, the pipeline just returns the first successful alternative. In the second example we tell the request that we want to find all alternatives.
