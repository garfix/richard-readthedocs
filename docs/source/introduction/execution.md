# Execution

Once the composer has composed the semantic representation in the forms of a list of logical atoms, like this

~~~prolog

    ('ocean', $1)
    ('borders', $1, $2)
    ('african', $2)
    ('country', $2)
    ('borders', $1, $3)
    ('asian', $3)
    ('country', $3)

~~~

the executor (`AtomExecutor`) is able to execute it. Execution is similar to the logic programming language [Prolog](https://en.wikipedia.org/wiki/Prolog). It starts out with an empty variable binding. Then processes the list of atoms, one by one. Each free variable is bound to one or more values. If the atom has a variable that is already bound, this variable value is used as a restriction to the atom.

In the above example the first atom is `('ocean', $1)`. It contains the new variable `$1`. The __predicate__ `ocean` is sent to one of the available modules that is able to process it (there may even be multiple modules that can process it). The module returns a list of values for the variable. `$1` is then bound to `arctic_ocean`, `indian_ocean`, `pacific` etc. In the next atom, `('borders', $1, $2)`, `$1` is already bound, and the module that handles the predicate `borders` is given a bound value of `$1`. It then finds the values of `$2`, given the bound value of `$1`. When no values are found for an atom, the process stops and the result is an empty list of bindings. If the list completes, the executor returns a list of distinct bindings. Each binding has a value for `$1`, `$2` and `$3`.

Some predicates handle lists of atoms for an argument. For example

~~~prolog
('count', $4, [
    ('ocean', $1)
    ('borders', $1, $2)
])
~~~

performs the body `('ocean', $1) ('borders', $1, $2)` and counts the number of results and returns this as `$4`.
