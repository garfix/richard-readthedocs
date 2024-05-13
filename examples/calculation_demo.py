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
        { "syn": "s -> 'what' 'is' term", "sem": lambda expr: lambda: expr() },
        { "syn": "s -> 'calculate' term", "sem": lambda expr: lambda: expr() },
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
