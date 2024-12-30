# Is (Equality)

One can state that different names mean the same thing:

    John is Jack.
    The Evening Star is the Morning Star.

Possible ways to implement it are:

* Make the names share the same ID
* Use two ID's, but use `isa` to have the first entity inherit all properties from the second entity
* Just define equality

## Make the names share the same ID

The following example shows that this is problematic:

    John is a boy.
    Jack is a dope.
    John is Jack.

In the first two sentences both John and Jack have been defined, and have been given an ID. This makes it hard for the third sentence to unify these. It is possible, but hard.

## Use isa to inherit

You could say `isa(John, Jack)` and `isa(Jack, John)`, so that both persons inherit each other's properties. Apart from being semantically incorrect, the inferences quickly run into infinite recursion.

## Define equality

Just define `equals(John, Jack)` and have inference rules deal with the inheritance of properties.

The SIR demo uses this approach:

~~~prolog
instance_of(A, B) :- equals(A, C), instance_of_proper(C, B).
instance_of(A, B) :- equals(C, A), instance_of_proper(C, B).
~~~

The drawback here is that the inferences should be set up in a way that avoids code duplication. You don't want `equals` to pollute all of your code.

The advantage is that you leave it to the logic to determine what `equals` really means. It can be a problematic concept, and it doesn't mean the same thing in all cases. Compare:

    Salt is Natrium Chloride
    Clark Kent is Superman

The first equality is pure synonymy, While the second one means something like: Clark Kent and Superman have the same location, and share (a large part of) the same mind and body. Note that one can't just say "Clark Kent flies over Metropolis wearing a red cape."

