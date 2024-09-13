# Questions

There are many variants on questions. Here are the major groups, with just one example for each group. The reason that there are so many types of questions is that all variables that take part in the response need to be accessible from this top level.

The sentence-level rules in a semantic parser differ most from a pure syntax based analysis. The word "what" for example is tradionally just a pronoun, a sort of noun that forms an argument to a verb. In a semantic parser it's a __signal word__, a word that indicates the type of question.

## Yes/no

Yes/no questions start with "is", "are", "does", "do".

They produce a range of entities. If the list contains any values, the answer would be "yes", if not, it is "no". It comes in different forms. Here's an example:

~~~python
{
    "syn": "s(E1) -> 'is' 'there' np(E1) '?'",
    "sem": lambda np: apply(np, []),
    "inf": [("format", "y/n")],
}
~~~

## List

List questions start with "what", "which", "where".

List question produce one or more answers, based on a single variable, that can be output as a comma-separated string: "Amazon, Brahmaputra, Colorado"

~~~python
{
    "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' '?'",
    "sem": lambda nbar: nbar,
    "inf": [("format", "list"), ("format_list", e1)],
}
~~~

Note the lower case `e1` that reifies (from variable to string) the main variable `E1`. This reification is needed to store the variable in a table.

Here's a quite different sentence, that still behaves just like a list:

~~~python
{
    "syn": "s(E2) -> 'where' 'is' np(E1) '?'",
    "sem": lambda np: apply(np, []) + [('where', E1, E2)],
    "inf": [("format", "list"), ("format_list", e2)],
}
~~~

The answer to the question is a location. The location is produced by the predicate `where`.

## Number

Number questions start with "how many", "how large", or "what is" with an aggregation.

The `sem` of a rule that results in a number is often an aggregation, like `sum`, but it can also be a list of atoms that normally results in a single value. You can specify a unit of measurement, which makes the result something like "14 ksqmiles".

~~~python
{
    "syn": "s(E1) -> 'what' 'is' 'the' 'total' 'area' 'of' np(E2) '?'",
    "sem": lambda np: [("sum", E1, E3, apply(np, []) + [('size_of', E2, E3)])],
    "inf": [("format", "number"), ("format_number", e1, "ksqmiles")],
}
~~~

## Table

Table questions start with "what" and produce multiple sentence-level variables.

Some questions require multiple values per answer, and are normally displayed as a table.

~~~python
{
    "syn": "s(E1, E3) -> 'what' 'is' 'the' 'average' 'area' 'of' np(E2) preposition(E2, E3) 'each' nbar(E3) '?'",
    "sem": lambda np, preposition, nbar: nbar + [('avg', E1, E4, apply(np, preposition) + [('size_of', E2, E4)])],
    "inf": [("format", "table"), ("format_table", [e3, e1], [None, 'ksqmiles'])],
}
~~~

Notice that this rule has two sentence variables: `s(E1, E3)`. These can be formatted as list of lists (a table). `format` table has two arguments: the result-variables and the column headers.

