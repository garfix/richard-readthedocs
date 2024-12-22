# Entity Unification Grammar

The grammar formalism of this library was developed by me in order to make semantic composition easier than was possible with the existing techniques.

Articles about natural language interfaces rarely contain information on the details of turning a syntactic structure into a semantic structure. For the older systems we can only guess how they are implemented. Winograds's SHRDLU was a good exception, it explained how  "semantic specialists" worked together during syntactic analysis to form a Planner program. However, Winograd himself found the procedural approach not suited for large scale applications.

Richard Montague created the first formalism to compose semantics using lambda calculus: [Montague grammar](https://en.wikipedia.org/wiki/Montague_grammar). It's interesting to see how semantic composition can be done by function application, but a commonly heard complaint is that becomes complicated rather quickly.

Computational linguists turned to __feature structure unification__. For an example, see [here](https://cs.union.edu/~striegnk/courses/nlp-with-prolog/html/node83.html). It has the advantage that it can handle both person/number/tense agreement and long-distance dependencies. But working with these structures is still the work of a specialist. "Gap threading" comes to mind as a particularly complex part of this approach.

The formalism I developed aimed to be so simple that I could work with it myself. It focuses on the entities involved in a sentence and performs __entity unification__. It handles long-distance dependencies through entity unification and agreement by creating inferences that are checked for agreement in a separate step (not yet implemented here yet, but implemented before in NLI-GO). I found syntactic agreement to be largely superfluous when it comes to semantic composition, and the CHAT-80 replication shown here doesn't use it at all.

## Syntax and semantics

Syntax is based on phrase structure grammar, but extended with variables that represent the entities involved.

Here's a sample rule. The `syn` part is based on the rewite rule `vp -> tv np` and has two variables `E1` and `E2` that represent the subject and the object of the verb.

~~~python
{
    "syn": "vp(E1) -> tv(E1, E2) np(E2)",
    "sem": lambda tv, np: np + tv
}
~~~

It says: rewrite the verb phrase `vp` (verb phrase) to a `tv` (transitive verb) and an `np` (noun phrase). Each constituent is followed by at least one variable, but `tv` has two: `E1` and `E2`.

`sem` forms the semantics, or meaning, of the phrase. It is implemented as a function that has an argument for each constituent of the syntax rule, here: `tv` and `np`. When this function is called, by the Semantic Composer, to compose the semantics of the sentence, it passes the __semantics__ of the children `tv` and `np`. Only after the semantics of the child constituents has been computed can the semantics of their parent be calculated. The child semantics are passed to the parent as arguments to the function.

Just as an example, `tv` could be `[('flows', E1, E2)]` and `np` could be `[('country, E1)]`. Semantics here takes the form of lists of atoms. The lambda function then performs Python code on these child semantics to create the parent semantics. Here it just adds the lists (`+`).

## Variable unification

In the above exaple, `tv` will be rewritten by another rule. Here's an example:

~~~python
{
    "syn": "tv(E1, E2) -> 'flows' 'to'",
    "sem": lambda: [('flows', E1, E2)]
}
~~~

`E1` and `E2` are sentence variables. There scope is the rule they are in. The composer will create __dialog variables__ for these variables, and these have dialog scope. They happen to be the same here, but that's because the rules use the same small set of variables. If the rule would have been written like this:

~~~python
{
    "syn": "verb(A3, A4) -> 'flows' 'to'",
    "sem": lambda: [('flows', A3, A4)]
},
~~~

The composer would create a new __dialog variable__, let's say `$5` that replaces both `E1` and `A3`, and a dialog variable `$6` to replace both `E2` and `A4`.

The result:

~~~
tv($5) -> verb($5, $6) np($6)
verb($5, $6) -> 'flows' 'to'
~~~

The formalism, together with the variable unification procedure by the Composer, solves the problem of long-distance dependencies in an effortless way.

## inferences about dialog variables

Some phrases imply information about dialog variables that is useful to following sentences in the dialog. In the following example, the `inf` (inference) tells the dialog that the dialog variable `E1` is a city. In the rest of the dialog, whenever `E1` is used again, the system knows that this is a city.

~~~python
{
    "syn": "noun(E1) -> 'city'",
    "sem": lambda: [('city', E1)],
    "inf": [('isa', e1, 'city')]
}
~~~

The information should be stored in the dialog context. The dialog variables, like `E1` are stored as strings. Note that `E1` has only local scope and is given dialog scope by turning it into the form `$7192` or similar.

The value of `inf` may be a list of atoms, but it can also be a function that returns a list of atoms, and is given the same child semantics as `sem`:

~~~python
{
    "syn": "common_noun(E1) -> /\w+/",
    "sem": lambda token: [(token, E1)],
    "inf": lambda token: [('isa', e1, token)]
}
~~~

## automaticly executed code

In some cases you don't want information be stored, but code to be executed, immediately. In this case, use `exec`:

~~~python
{ "syn": "common_noun(E1) -> /\w+/",
  "sem": lambda token: [ (token, E1) ],
  "exec": lambda token: [
        ('learn_grammar_rule', { "syn": f"common_noun(E1) -> '{token}'", "sem": lambda: [(token, E1)] }),
        ('add_relation', token, ['id']),
    ]
}
~~~

In this example the `learn_grammar_rule` and `add_relation` atoms are executed by the semantic executor after the sentence is parsed and composed.

