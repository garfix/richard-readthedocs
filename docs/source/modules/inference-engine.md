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

## ('learn_rule', head, [body-atoms])

The `learn_rule` predicate lets you learn the system a new rule at runtime. For example:

~~~
{
    "sem": lambda noun, are, np: [('learn_rule', np[0], noun)],
}
~~~

Here `np[0]` holds the tuple that is the head of the rule, while `noun` holds the tuples that form the body.

Before storing the new rule, the head and body are bound to the activate variable values.

_Cooper's system_ has some examples.

## Grouping

Atoms may be grouped using parenthesis, like this: `( part_of(A, B), part_of_n(A, B, N) )` this allows a group of atoms to be used as a single argument.

## Disjunction

When multiple rules match an atom, they will all be executed. Sometimes this is not what you want. If you want the second and third rules to be only executed when the first fails, you may use Prolog disjunction operator.


An example can be found in the SIR demo. When asked "How many fingers has Tom?" SIR could find both "10" and "9" as the answer. However, it first tries to determine to look up the answer, and only if that fails, it tries to find the answer by reasoning.

~~~pl
part_of_number(A, B, N) :- (
    # direct, non inheriting
    part_of(A, B), part_of_n(A, B, N)
;   # direct, inheriting
    full_isa(AA, A), full_isa(B, BB), part_of(AA, BB), part_of_n(AA, BB, N)
;   # transitive, non inheriting
    part_of(C, B), part_of(A, C), part_of_n(C, B, N1), part_of_number(A, C, N2), multiply(N1, N2, N)
;   # transitive, inheriting
    full_isa(B, BB), part_of(C, BB), part_of(A, C), part_of_n(C, BB, N1), part_of_number(A, C, N2), multiply(N1, N2, N)
).
~~~

The Prolog `;` separates the possible solutions. The second disjunct is only executed when the first fails, the third only when the second fails, and so on.
