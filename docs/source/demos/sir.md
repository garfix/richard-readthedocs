# SIR

Replicates a dialog of SIR (Semantic Information Retriever), by Bertram Rafael as described in "SIR: a computer program for semantic information retrieval" - Bertram Rafael (1964)

## Learning concepts

SIR has no built-in nouns. They're all taught by the user. The identifier of the concept is simply it's word in the sentence. The singular is taken, and therefore it's needed to split a word in its root morpheme and its plural suffix ("s").

## Teaching is-a relationships

SIR contains sentences like "Every boy is a person". These are added to the database in the form `isa('boy', 'person')`.

The page [is-a relationships](../language/is-a.md) has more on the topic.

## Teaching equality

SIR contains sentences like "John is Jack". These are added to the database in the form `equals('John', 'Jack')`.

The page [is (equals)](../language/is-equals.md) has more on the topic.

## Teaching concepts

SIR teaches the structure of concepts Notice these sentences:

    A finger is a part of a hand
    Every hand has 5 fingers

The first sentence just describes the relationship between finger and hand. The second sentence does the same, but adds the fact that there's number involved. In the demo these relationships are implemented by the predicates `part_of` and `part_of_n`.

## Clarification comments

SIR tells the user what knowledge is missing to make the proper inference. It can respond with "Don't know whether finger is part of John" and "How many finger per hand?". This is implemented in the predicates `have` and `part_of_n`. If they don't yield any results, the raise the exception that forms the response.

The implementation of this feature is very brittle. Simple changes to the inferences can break it.
