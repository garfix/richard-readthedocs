from richard.core.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.semantic_composer.SemanticComposer import SemanticComposer
from richard.block.FindOne import FindOne
from richard.core.constants import E1, E2, Body, Range
from richard.processor.parser.helper.grammar_functions import apply
from richard.type.SemanticTemplate import SemanticTemplate

def composition_demo():
    grammar = [
        { "syn": "s(E1) -> np(E1) vp(E1)", "sem": lambda np, vp: apply(np, vp)},
        { "syn": "vp(E1) -> verb(E1, E2) np(E2)", "sem": lambda verb, np: apply(np, verb) },
        { "syn": "verb(E1, E2) -> 'flows' 'to'", "sem": lambda: [('flows', E1, E2)] },
        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar: SemanticTemplate([Body], apply(det, nbar, Body)) },
        { "syn": "det(E1) -> 'the'", "sem": lambda: SemanticTemplate([Range, Body], Range + Body) },
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
        { "syn": "noun(E1) -> 'river'", "sem": lambda: [('river', E1)] },
        { "syn": "noun(E1) -> 'sea'", "sem": lambda: [('sea', E1)] },
    ]

    parser = BasicParser(grammar)
    composer = SemanticComposer(parser)

    pipeline = Pipeline([
        FindOne(parser),
        FindOne(composer),
    ])

    request = SentenceRequest("The river flows to the sea")
    semantics = pipeline.enter(request)
    print(str(semantics))


if __name__ == '__main__':
    composition_demo()
