# Inference engine

Some relations are best implemented as a goal that requires a number of sub-goals to succeed. This is the basis of the Prolog programming language, and this library implemented some of its most basic functionality, which includes some of the syntax.

For example, the CHAT-80 demo contains a file `inferences.pl` with this content:

~~~prolog
in(A, B) :- contains(B, A).
in(A, B) :- contains(C, A), in(C, B).
~~~

Whenever a relation `in` is executed, the inference engine attempts both of these rules and combines their results. The first rule says, for `in` to succeed, `contains` must succeed, and the bindings of `contains` will be returned for the `in` relation. The second rule says that both `contains` and `in` should succeed for `in` to succeed.

Notice that `in` is recursive, and this possibility is a big advantage of these rules.

Don't expect full Prolog here. The engine is limited to variable resolution.

## InferenceModule

To add such rules to the model, create an `InferenceModule` and show the pat to the rules file.

~~~python
inferences = InferenceModule()
inferences.import_rules(path + "inferences.pl")

model = Model([
    facts,
    inferences,
    sentence_context,
    dialog_context
])
~~~

## Facts

Except for rules, the file can contain facts as well. Facts are just like tuples in a database. Sometimes it's easier to have them near the rules. For example:

~~~prolog
parent('robert', 'martha').
parent('martha', 'william').
parent('william', 'beatrice').
parent('william', 'antonio').
grand_parent(X, Y) :- parent(X, Z), parent(Z, Y).
~~~

The `parent` rules are facts. They have no conditions.
