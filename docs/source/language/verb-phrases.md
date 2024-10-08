# Verbs

A verb is the heart of a sentence. It is expressed logically as a predication over a fixed number of arguments. The verb "flow through" for example is logically represented by the atomic formula `flow_through(X, Y)`.

Syntactically, the subject is the first argument you see in a sentence, whether the sentence is active or passive. In "John was bitten by a snake", "John" is the subject.

In linguistic semantics however, the logical representation is key, and the arguments are named after the position in the predication: `predicate(subject, object, indirect object)`.

* __subject__ is the first argument
* __object__ is the second argument
* __indirect object__ is the third argument

"John" would be the object of the sentence, whether it was passive or active.

The word `through` in this example is called the `particle` of the verb. Typically it is located just after the verb, but in many cases another phrase is placed between the verb and the particle.

There are (mainly) three types of verbs:

* __intransitive__ verbs (iv) with a subject but no object ("sleep")
* __transitive__ verbs (tv) with a subject and an object ("pick up")
* __ditransitive__ verbs (dtv) with a subject (sub), object (obj), and an indirect object (iobj)  ("flow to", "the river flows from the highlands to the sea")

In applications where time plays a role, or application that make statements about events or even states, the `event` needs to be represented explicitly. This is done by adding an extra event argument `E`: `flow_through(E, X, Y)`. In the examples below we will not do that yet.

Once the event has been represented, it becomes possible to create separate relations for the subject and object: `flow_through(E), subject(E, X), object(E, Y)`. This has the advantage that the verb is more flexible. In database applications this flexibility is not needed, and the extra relations just add to the complexity and syntactic overhead of the application. Use it only if you have a clear use case for it.

A verb can be either active or passive. A passive sentence changes the order of the subject and the object, or indirect object. To change the syntactic order into the semantic order, the arguments must be __normalized__ (reordered).

In most cases a verb phrase does not contain all of the arguments of the predication. In the sentence "John was bitten by a snake", "was bitten by a snake" is the verb phrase, and it does not contain the object ("John").

## Verb phrase naming

You will find that there are many types of verb phrases, all missing one or two arguments. A transitive vp is different from a ditransitive vp. The order of the arguments may not be normalized. All these verb phrase variants require a different semantics, that composes the meaning in slightly different ways, and at the same time normalizes the argument order.

For this reason I've created specializations of the verb phrase (`vp`). The simplest form of an intransitive verb is `vp_sub`. It has one segment (`sub`), and it's the subject (abbreviated to `sub`). For a transitive verb it's `vp_sub_obj`, and for an intransitive verb it's `vp_sub_obj_iob`. Where `obj` is short for object and `iob` short for indirect object.

When a verb phrase does not span some argument of the predication, this unhandled argument is represented as `no`. For example, a ditransitive verb with an unhandled subject is named `vp_nosub_obj_iob`. It still expresses that this is a 3-place predicate, but one of the arguments, the subject, is not part of this vp, hence `nosub`.

The semantics of a passivized sentences is responsible for normalizing the argument order, and so there's a special case for each argument order. A basic example of a passive transitive verb is `vp_obj_sub`. Note the reversal of `sub` and `obj`. This rule is aware that the syntactic order of the arguments is different from the logical order.

Combinations of omission and reordering are common, as in `vp_noobj_sub`. This vp represents a passive sentence, and its object is handled outside of the vp.

## Transitive verb

In the phrase "Afghanistan borders China", "borders" is a transitive verb (`tv`): it has a `subject` ("Afghanistan") and an `object` ("China").

The meaning of the verb consists of a list with a single atom.

~~~python
{
  "syn": "tv(E1, E2) -> 'border'",
  "sem": lambda: [('borders', E1, E2)]
}
~~~

## Ditransitive verbs

~~~python
{
  "syn": "dtv(E1, E2, E3) -> 'flows' 'into'",
  "sem": lambda: [('flows_from_to', E1, E2, E3)]
}
~~~

## Active transitive verbs

"borders China" is an active vp missing the subject. This subject (`sub`) is passed to this semantic function as an argument, and the function passes it through to its child `tv`. The result is a function with one argument (`obj`) and can be used by `np` to establish membership.

~~~python
{
  "syn": "vp_nosub_obj(E1) -> tv(E1, E2) np(E2)",
  "sem": lambda tv, np: apply(np, tv)
}
~~~

With negation ("not"):

~~~python
{
  "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_obj(E1)",
  "sem": lambda vp_nosub_obj: [('not', vp_nosub_obj)]
}
~~~

## Passive transitive verbs

Note that the order of `obj` and `sub` is reversed and that the final call to `tv` is the same as in the active form.

~~~python
{
  "syn": "vp_noobj_sub(E1) -> tv(E2, E1) 'by' np(E2)",
  "sem": lambda tv, np: apply(np, tv)
}
~~~

Note the reversal of `E1` and `E2` as arguments to `tv`.

## Passive ditransitive verbs

The first rule receives an `obj` from its parent function and passes it to it's child function. The second rule receives an `obj` from the first rule, and adds an `sub` argument. Both are passed to its child function. The third rule receives both a `sub` and an `obj` from the second rule, and adds an `iob` argument.

Note that the first rule uses "from", which makes it not generic.

~~~python
{
  "syn": "vp_noobj_sub_iob(E1) -> 'from' 'which' np(E2) vp_noobj_nosub_iob(E1, E2)",
  "sem": lambda np, vp_noobj_nosub_iob: apply(np, vp_noobj_nosub_iob)
},
{
  "syn": "vp_noobj_nosub_iob(E1, E2) -> dtv(E2, E1, E3) np(E3)",
  "sem": lambda dtv, np: apply(np, dtv)
}
~~~
