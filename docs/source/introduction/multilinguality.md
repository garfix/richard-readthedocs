# Multilinguality

If you need your application to support multiple languages without the user having to select one, use the approach describes here.

This example code will make the idea clear:

~~~python
language_selector = LanguageSelector(["en_US", "nl_NL"])
tokenizer = BasicTokenizer()

parsers = {
    "nl_NL": BasicParser([
        { "syn": "s(V) -> np(E1) vp(V, E1)" },
        { "syn": "vp(V, E1) -> verb(V) np(E1)" },
        { "syn": "np(E1) -> noun(E1)" },
        { "syn": "noun(E1) -> proper_noun(E1)" },
        { "syn": "proper_noun(E1) -> 'john'" },
        { "syn": "proper_noun(E1) -> 'mary'" },
        { "syn": "verb(V) -> 'loves'" },
    ], tokenizer),
    "en_US": BasicParser([
        { "syn": "s(V) -> np(E1) vp(V, E1)" },
        { "syn": "vp(V, E1) -> verb(V) np(E1)" },
        { "syn": "np(E1) -> noun(E1)" },
        { "syn": "noun(E1) -> proper_noun(E1)" },
        { "syn": "proper_noun(E1) -> 'jan'" },
        { "syn": "proper_noun(E1) -> 'marie'" },
        { "syn": "verb(V) -> 'houdt' 'van'" },
    ], tokenizer)
}

parser = Multilingual(parsers, language_selector)

pipeline = Pipeline([
    FindOne(language_selector),
    FindOne(tokenizer),
    FindOne(parser)
])
~~~

The first block in the pipeline contains a `language selector`. The language selector produces two or more locales. After the first locale is selected, the rest of the pipeline is attempted. If this fails because the sentence can't be parsed in one language, the pipeline backtracks and tries the next locale.

The parser is changed into a composite in the form of a `Multilingual` processor. It is passed two parsers, one for each locale. When the pipeline reaches the parser, the multilingual processor selects the parser that matches the active locale.
