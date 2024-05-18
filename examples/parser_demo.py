from richard.Pipeline import Pipeline
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.processor.tokenizer.BasicTokenizer import BasicTokenizer
from richard.block.FindOne import FindOne

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
        FindOne(tokenizer),
        FindOne(parser)
    ])

    request = SentenceRequest("John loves Mary")
    pipeline.enter(request)

    tree = parser.get_tree(request)
    print(tree)


if __name__ == '__main__':
    parser_demo()
