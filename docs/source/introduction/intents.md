# Intents

The core meaning of any sentence is its **intent**. An intent is the predicate that defines how the system deals witj the sentence.

While the meaning of a sentence is directly executable code, it's good to send this meaning to an `intent` handler to process it. This level of indirection provides you with the flexibility to format the output in any way you like, and to handle subtle differences in meaning in different ways.

## An example

Here's an example from the read grammar of the CHAT-80 replication demo:

~~~python
{
    "syn": "s(E1) -> 'what' 'are' np(E1) vp_noobj_sub_iob(E1) + '?'",
    "sem": lambda np, vp_noobj_sub_iob: [('intent_list', e1, apply(np, vp_noobj_sub_iob))],
}
~~~

The top-level semantics of the rule is the atom `intent_list()`. It has two arguments: `e1` and the actual semantics body of the sentence: `apply(np, vp_noobj_sub_iob)`. Both arguments are passed to the intent. This intent looks like this:

~~~pl
intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    store(output_type('list'), output_list(Elements)).
~~~

This intent executes the semantic body `Sem` using `find_all`. This results in a list of values called `Elements`.

This list is now prepared to output by storing it in the sentence context: `store(output_type('list'), output_list(Elements))`.
This says: store the output type `list` using as argument the list `Elements`.

This output is picked up by the generator. This is described in [Generation](output-generation).

## One sentence can have multiple intents

A single surface form often has multiple possible meanings. They can be completely different, but often they are subtle. Yet they mave to be handled in a different way. These meanings can all be handled by a single intent inference, in the form of a disjunction.

Each disjunct starts with a check, is followed by the execution, and ends with output.

Here's an example from SIR:

~~~pl
intent_isa(A, B) :- (
    # is a girl a person?
    full_isa(A, B), store(output_type('yes'))
    # is a person a girl?
;   proper_isa(B, A), store(output_type('sometimes'))
    # is a person a person?
;   equals(A, B), store(output_type('yes'))
    # otherwise
;   store(output_type('unknown'))
).
~~~
