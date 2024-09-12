# Determiners

[Determiners](https://en.wikipedia.org/wiki/Determiner) are words that restrict the noun phrase.

"Examples in English include articles (the and a), demonstratives (this, that), possessives (my, their), and quantifiers (many, both). Not all languages have determiners, and not all systems of grammatical description recognize them as a distinct category." - [Wikipedia](https://en.wikipedia.org/wiki/Determiner)

## Generalized quantification

Formal logic posits the existential (i.e. at least one) and the universal (i.e. all) quantifiers. Natural language also has numeric quantifiers (like "two", "most", "at least five"). Both can be handled by the same technique of __generalized quantification__. The technique is mainly suitable for quantifiers, but for simplicity it is used here for all determiners.

Generalized quantification is implemented as a SemanticTemplate that takes a `Range` and a `Body`.

~~~Python
SemanticTemplate([Range, Body], <determiner-function>)
~~~

`Range` is bound to an `nbar` that is the part of the `np` without the determiner (for example: children). `Body` is bound to a `vp` (for example: are playing).

A determiner is always used by an `np`, as the first parameter in an `apply` call:

~~~python
{
    "syn": "np(E1) -> det(E1) nbar(E1)",
    "sem": lambda det, nbar:
            SemanticTemplate([Body], apply(det, nbar, Body))
}
~~~

The universal quantifier looks like this:

~~~Python
{
    "syn": "det(E1) -> 'all'",
    "sem": lambda:
        SemanticTemplate([Range, Body], [('all', E1, Range, Body)])
}
~~~

while the existential quantifier looks like this:

~~~Python
{
    "syn": "det(E1) -> 'some'",
    "sem": lambda:
            SemanticTemplate([Range, Body], Range + Body)
}
~~~

Note that the all-quantifier produces an extra atom, whereas the existential quantifier just returns the input. This is important, because it allows the semantic representation to stay shallow, and thus optimizable.

The quantifier "more than":

~~~Python
{
    "syn": "det(E1) -> 'more' 'than' number(E1)",
    "sem": lambda number:
            SemanticTemplate([Range, Body], [('det_greater_than', Range + Body, number)])
}
~~~

In the same vein, there are predicates `det_less_than` and `det_equals`.


