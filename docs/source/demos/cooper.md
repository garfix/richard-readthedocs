# Cooper's system

This demo aims to replicate a dialog of William S. Cooper's system as described in "Fact Retrieval and Deductive Question-Answering Informatlon Retrieval Systems" - Cooper (1964)

The source code for the demo can be found [https://github.com/garfix/richard/blob/main/tests/integration/Cooper_test.py](here)

The main features of this model are:

* Use of three-valued logic (true, false, unknown); a open world assumption
* Learning names of things
* Learning simple rules about things

## Two grammars

Cooper's system has a learning phase and a query phase. In the learning phase the sentence "magnesium is a metal" aims to add factual knowledge to the system, while in the query phase, the same sentence aims to check a statement. I created separate grammars for both phases, because this is the easiest way to deal with this phenomenon.

## Three-valued logic

The main logic of Richard!, like Prolog, is based on treating the absense of a fact as treating it as false. This is called the __closed world assumption__: the assumption that all that is known about a subject is present in the database.

Cooper's system works differently. A fact can be available positively (`true`), or it can be available negatively (`false`). If neither is the case, the fact is `unknown`.

All predicates in this replication have an extra truth-value `truth` that can be `true` or `false`. This tuple, for example, expresses the fact that it not true that gasoline burns rapidly.

    burns_rapidly('gasoline', 'false')

The replication has logical operators that handle tree-valued logic:

    not_3v(T1, T2)

`T2` results in the negative of `T1`, where `T1` may be "unknown". The negative of "unknown" is "unknown".

    and_3v(T1, T2, T3)

`T3` results in the logical `and` of `T1` and `T2`. If either `T1` or `T2` is "unknown", the result `T3` is "unknown".

The result of evaluating a sentence in the second grammar is also a truth value. Whereas a regular grammar in our system passes entities around, this replication also passes truth values around. This is not a problem because truth values are entities as well.

