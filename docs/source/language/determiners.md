# Determiners

[Determiners](https://en.wikipedia.org/wiki/Determiner) are words that restrict the noun phrase.

"Examples in English include articles (the and a), demonstratives (this, that), possessives (my, their), and quantifiers (many, both). Not all languages have determiners, and not all systems of grammatical description recognize them as a distinct category." - [Wikipedia](https://en.wikipedia.org/wiki/Determiner)

## Generalized quantification

Formal logic posits the existential (i.e. at least one) and the universal (i.e. all) quantifiers. Natural language also has numeric quantifiers (like "two", "most", "at least five"). Both can be handled by the same technique of __generalized quantification__. The technique is mainly suitable for quantifiers, but for simplicity it is used here for all determiners.

Generalized quantification implements each quantifier as function that accepts two numbers and returns a boolean:

~~~Python
def determiner(result: int, range: int) -> bool:
~~~

`range` is the total number of instances of an entity (for example: all children). `result` is the number of children that results when applied to the `vp` (for example: are playing). The range may be restricted to a smaller set of instances when the `np` is in scope of another determiner.

For example, the universal quantifier looks like this:

~~~Python
def determiner(result: int, range: int) -> bool:
    return result == range
~~~

while the existential quantifier looks like this:

~~~Python
def determiner(result: int, range: int) -> bool:
    return result > 0
~~~

and the quantifier "at least 5":

~~~Python
def determiner(result: int, range: int) -> bool:
    return result >= 5
~~~

the latter is a simplification, and the `5` will be variable in reality, but this shows the point: a single function can handle a wide range of quantifiers.

## Find

The determiner's function is applied by the function `find`:

~~~Python
def find(dnp: dnp, vp: callable) -> list:
~~~

`find` takes a `dnp` (determined noun phrase, the value of an `np`), and a `vp`. The `dnp` contains a `determiner` function and a `nbar` function. First it runs `nbar` to collect _all_ id's of the `nbar` entity. Then it uses each of these ids as an argument to the `vp` function. If the function contains results, the id is added to the list of results. When done, `find` knows both the total number of ids (called `range`) and the number of ids that delivered results when passed through `vp`. This number is called `result`. Both `result` and `range` are then passed to the `determiner` function. If this function returns `true`, all ids that passed `vp` are returned. If not, it returns an empty list.

In short, `find` passes all entities of `nbar` to `vp` and returns the ones that passed, but only if the function `determiner` is satisfied.



## Quantifiers

A quantifier specifies the quantity (amount) of the np. It delivers a function that is 

~~~Python
{ 
    "syn": "det -> quantifier", 
    "sem": lambda quantifier: 
            lambda result, range: quantifier(result, range) 
}
~~~

So here is "every"

~~~Python
{ 
    "syn": "quantifier -> 'every'", 
    "sem": lambda: lambda result, range: result == range 
}
~~~

and here is the literal "three":

~~~Python
{ 
    "syn": "number -> 'three'", 
    "sem": lambda: lambda: 3 
}
~~~



