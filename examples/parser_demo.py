from richard.core.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
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

    parser = BasicParser(grammar)

    pipeline = Pipeline([
        FindOne(parser)
    ])

    request = SentenceRequest("John loves Mary")
    parse_tree = pipeline.enter(request)
    print(parse_tree)


if __name__ == '__main__':
    parser_demo()
