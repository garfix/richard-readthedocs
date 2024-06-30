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
        { "syn": "np(E1) -> det(D1) nbar(E1)", "sem": lambda det, nbar: [('quant', E1, det, nbar)] },
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
