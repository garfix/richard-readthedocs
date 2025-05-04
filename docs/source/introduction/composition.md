# Semantic attachments and composition

The meaning of a sentence or phrase can be composed of the meaning of its constituent phrases. Known as [Frege's principle](https://en.wikipedia.org/wiki/Principle_of_compositionality), this is the basis of deriving the meaning of a sentence.

A grammar rule can be extended with a __semantic attachment__, expressed by the "sem" key, which expresses the meaning of the phrase covered by the rule. In this library the attachments take the form of lists of atoms. The atom is implemented as a Python tuple.

An atom is a combination of a predicate with some arguments. Examples are `('river', E1)`, `('give', E1, E2, E3)`. The arguments may be variables (as in the example) or values.

Most sems are lists of atoms. This allows us to combine sems by simply adding the lists. Sems that don't need to be combinable can just be single atoms, or even simple values.

## Adding semantics to the syntax rule

Here are example rules that demonstrate the typical 2-part structure of a semantic attachment ("sem"):

~~~python
{
    "syn": "noun(E1) -> 'rivers'",
    "sem": lambda: [('river', E1)]
},
{
    "syn": "vp_nosub_obj(E1) -> tv(E1, E2) np(E2)",
    "sem": lambda tv, np: apply(np, tv)
},
~~~

Notice that "sem" is formed by a lambda function that returns a list of atoms.

The function `lambda tv, np: ...` is used to import the semantic values of the child nodes. Each child value is appointed a parameter with the same name as the syntactic category it belongs to. In the example above, `tv` is the first consequent of the rule, and `tv` is therefore the name of the first parameter of the function. In the same way, `np` is the second consequent, and therefore the second parameter. Only categories need parameters. Words (like `'river'` or `'two'` have no need for a parameter, as they have no child nodes).

The parameter names are not required to be the same as the syntactic categories, but it is good practice to keep them that way. An exception occurs when the rule has two of the same syntactic categories, as in `term -> term operator term`. In this case append a follow-up number, like `lambda term1, operator, term2`.

The returned value, a list of atoms like `[('river', E1)]`, forms the real meaning of the rule. It uses the meanings of its child nodes that were made available through the parameters of the function.

## Three composition operations

Calculating the semantics of a phrase is done by three operations: __add__, __fill__, and __apply__.

__add__ simply concatenates two lists. In the following example the sem of `nbar` is calculated from that of `adj` and `nbar` by adding their sems:

~~~python
{
    "syn": "nbar(E1) -> adj(E1) nbar(E1)",
    "sem": lambda adj, nbar: adj + nbar
}
~~~

__fill__ fills in an argument of a tuple with the sem of a child. In this example the sem of a child phrase is used as an argument of the sem.

~~~python
{
    "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_obj(E1)",
    "sem": lambda vp_nosub_obj: [('not', vp_nosub_obj)]
}
~~~

__apply__ is a bit more complex. The sem of one child is a __function__ (a `SemanticFunction` object) which is then applied to the sems of other child nodes. The Python function `apply` performs this operation. The first argument of `apply` is thus a the SemanticFunction, the latter arguments are the sems of the other children.

In the first rule of the following example `vp_nosub_obj` says: I will use my child `np` as a function to calculate my sem. I will pass it the child `tv` as an argument. Two further `np` rules are added as example of how the actual function depends on the inner structure of the `np`.

~~~python
{
    "syn": "vp_nosub_obj(E1) -> tv(E1, E2) np(E2)",
    "sem": lambda tv, np: apply(np, tv)
},
{
    "syn": "np(E1) -> nbar(E1)",
    "sem": lambda nbar: SemanticFunction([Body], nbar + Body)
},
{
    "syn": "np(E1) -> det(E1) nbar(E1)",
    "sem": lambda det, nbar: SemanticFunction([Body], apply(det, nbar, Body))
}
~~~

A `SemanticFunction` is like a function, but in the form of an object. It has two arguments: parameters and function body. Its first argument is a list of parameters. These parameters will be bound to the second (and further) arguments of the apply-call. SemanticFunction's second argument is an expression that calculates the sem. It may use both the child sems (i.e. `nbar`) and the parameters of the SemanticFunction (i.e. `Body`) to calculate the meaning.

`SemanticFunctions` should be used sparingly. They are mainly used for `np`, `det`, and `superlative`: syntactic structures that need sibing structures to determine their full meaning.

Apply is used a lot, because each np needs to be used as argument of apply. The number of SemanticFunctions, however is relatively large for a small grammar, but their use is rather limited to np's, determiners, and superlatives. In a large grammar their use will be relatively small.

## Example script

The semantic composition itself is performed by the __semantic composer__. It composes the meaning of the sentence into a single function.

A script composes and prints out the resulting meaning of the sentence. It is a tree-structure composed of atoms:

~~~python
[
    ('river', $1),
    ('sea', $2),
    ('flows', $1, $2)
]
~~~

Note how the individual atoms have been composed to a tree of nested atoms. Note also that local variables `E1` and `E2` that reoccur in the rules have been replaced by dialog-wide variables `$1`, `$2` and so on. These variables express the fact that the child variables and the parent variables refer to the same values.

When the composer combines the child sems with the parent sems, it introduces a new dialog variable for each new variable it encounters. When such a variable is used in a child node, the variable is passed on to the child. This mapping is defined by the variables next to the syntactic categories.

There are many other forms of semantic composition. The one presented here is both relatively easy to learn and yet very expressive. This will become more clear from the examples given in the rest of the documentation.

## Query optimization

The composition phase results in a list of atoms. Some of these contain a list of atoms as their arguments themselves. These atoms are about to be executed in order to process the sentence. The atoms form the meaning of the sentence and when executed they perform the function of the sentence. But is this an _efficient_ implementation of the function? Is it fast?

This system, like Prolog, processes atoms (called "goals" in Prolog) one by one. Each atom can either increase or decrease the number of variable bindings. Each of these bindings is then used as input to the subsequent atoms.

David Warren, one of the pioneer of the Prolog language, and together with Fernando Pereira designer of the famous Chat-80 system, recognized that the inference rules of Prolog are logically sound, but suffer from two performance problems. In the article "Efficient processing of interactive relational database queries expressed in logic" he worked out two ways to overcome them. Both of them have been implemented in the current system, as `BasicQueryOptimizer` which can be added to the composer as `query_optimizer`.

### Place resolve_name atoms up front

But let's start with an optimization I added myself. I added `FrontResolveName`, an optimizer that puts all `resolve_name` atoms in the list up front. In most cases a name resolver yields only one or just a few results. Best to place these atoms up front.

### Sort by cost

Warren's first optimization is named "ordering goals in a conjunction" and implemented here by `SortByCost`. The basic idea is that an atom that creates less variable alternatives should be placed before an atom that creates more alternatives. The first one "costs less". Cost is determined by the number of tuples in the relation denoted by the predicate of the atom: the __size__ of the relation. Larger relations cost more. But that is not all. Once an argument of the atom is bound, the situation changes as the number of values produced changes quite a bit. How much this number changes depends on the number of different values of the argument: its __cardinality__.

In Warren's example a relation "borders" has a size of 900 tuples. Each of its arguments has cardinality 180. (There are 180 countries which are bordering in 900 different ways) When none of its arguments are bound, the cost of the atom is simply 900. When one argument is bound, the cost reduces to 900/180 and when both arguments are bound the cost reduces even further, to 900/180/180.

While the outcome of any ordering is the same, the performance of an query sorted by cost can increase dramatically.

Atoms that represent database relations are the main candidates for sorting by cost. Other atoms often depend on other atoms. For example `('>', E1, E2)` should not move to a front position. It should only be used if both E1 and E2 are bound.

### Isolating subqueries

The second optimization is named "isolating independent parts of a query" and implemented here by "IsolateIndependentParts". The problem is best described by Warren himself: "The problem is essentially that resolution treats all goals in a conjunction as being dependent. This is fine so long as the goals share uninstantiated variables. However when two parts of a conjunction no longer share variables, they should be solved independently."

The best illustration of the problem is in this sentence: "Which is the ocean that borders african countries and that borders asian countries?" which translates to

~~~prolog
answer(X) :- ocean(X), borders(X, C1), african(C1), country(C1), borders(X, C2), asian(C2), country(C2).
~~~

You can see the similar structures for african and asian countries. The crux is in the fact that C2 is evaluated not once, but for each separate binding of C1. This is inefficient and unnecessary.

Warren didn't give an algorithm for this optimization. It is available in the Prolog code of Chat-80, for the enthusiast. I attempted an implementation based on the numerous examples he gave and I will try to give a bit of an explanation. First I create a dependency graph that links each atom to all other atoms that use the same variable(s). The order of the atoms is retained, and this is important because it the result of earlier optimizations. From this first graph I create a second graph. All atoms are processed anew. If an atom is "global" (it is needed for the response of the sentence), it's made to be independent on other atoms. If the atom has a dependency on a succeeding atom, it is also made to be independent. Otherwise, it is made to be dependent on the first atom it depends on. From this second graph the new query is generated, where each isolated subquery is placed in the body of an `isolated` atom. This kind of predicate executes all atoms in its body, but returns only a single value.
