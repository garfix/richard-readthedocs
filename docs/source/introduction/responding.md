# Responding

The list of bindings that are produced by the executor are the result of the sentence. But it is not yet a human-readable form. That's where the responder (`SimpleResponder`) comes in. It turns the list of bindings in string of words, or a table.

The responder reads the inferences made for the sentence to determine how to transform the bindings into the output. There are several formats possible. I will give an example for each of them.

## Y/N

~~~python
{
    "syn": "s(E1) -> 'is' 'there' np(E1) '?'",
    "sem": lambda np: apply(np, []),
    "inf": [("format", "y/n")],
}
~~~

The format inferred from processing this sentence is `("format", "y/n")`. I.e. this is a Yes/no question. The response should be "yes" or "no". The responder checks the list of bindings. If empty, it returns "no", otherwise "yes".

## List

~~~python
{
    "syn": "s(E1) -> 'what' nbar(E1) 'are' 'there' '?'",
    "sem": lambda nbar: nbar,
    "inf": [("format", "list"), ("format_list", e1)],
}
~~~

The format is `("format", "list")` and `("format_list", e1)` is a extension of it. This format collects all different values of `e1` and puts them in a single string, each value separated from the other by a comma.

## Number

~~~python
{
    "syn": "s(E2) -> 'how' 'large' 'is' np(E1) '?'",
    "sem": lambda np: apply(np, []) + [('size_of', E1, E2)],
    "inf": [("format", "number"), ("format_number", e2, "ksqmiles")],
}
~~~

The format is `("format", "number")` and `("format_number", e2, "ksqmiles")` is its extension. There can be only one value in the result, it is available from `e2` and the second argument is the unit, here `ksqmiles`. The output consists of the value plus the unit.

## Table

~~~python
{
    "syn": "s(E1, E3) -> 'what' 'is' 'the' 'average' 'area' 'of' np(E2) preposition(E2, E3) 'each' nbar(E3) '?'",
    "sem": lambda np, preposition, nbar: nbar + [('avg', E1, E4, apply(np, preposition) + [('size_of', E2, E4)])],
    "inf": [("format", "table"), ("format_table", [e3, e1], [None, 'ksqmiles'])],
}
~~~

The format is `("format", "table")` and `("format_table", [e3, e1], [None, 'ksqmiles'])` is its extension. The output here is not a string, but a list of lists (a table). The first row consists of the header: the second argument `[None, 'ksqmiles']`. For each of the bindings a row is created with the values of `e3` and `e1` in that order.

## Canned

~~~python
{
    "syn": "s(E1) -> 'bye' '.'",
    "sem": lambda: [],
    "inf": [("format", "canned"), ("format_canned", "Cheerio.")],
},
~~~

The so called "canned response" just returns a fixed line of text. In this example it returns "Cheerio." in response to the user's "bye.".
