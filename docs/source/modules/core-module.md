# Core module

The core module is always added to a model and contains some common relations.

## ('equals', E1, E2)

If both `E1` and `E2` are bound, it checks if they are equal. If so, it returns a single result with both values in it. If not, it returns no results.

If only one argument is bound, it returns a single result where the unbound variable is given the value of the bound variable.

## ('greater_than', E1, E2)

Both `E1` and `E2` should be bound.

If `E1` is larger than `E2`, it returns a single result with both values in it. If not, it returns no results.

## ('less_than', E1, E2)

Both `E1` and `E2` should be bound.

If `E1` is smaller than `E2`, it returns a single result with both values in it. If not, it returns no results.

## ('count', E1, [body-atoms])

Executes `body-atoms` and binds `E1` to the number of results.

## ('sum', E1, E2, [body-atoms])

Executes `body-atoms` and collects the values of `E1` in each of them. These values are added up and placed in `E2`.

## ('arg_max', E1, E2, [body-atoms])

Executes `body-atoms` and collects the values of `E1` and `E2` from each of its results. It looks for the result with the largest `E2` and returns the `E1` and `E2` from that result.

Used for superlatives where the "tallest tree" is the tree with the largest height.

## ('arg_min', E1, E2, [body-atoms])

Executes `body-atoms` and collects the values of `E1` and `E2` from each of its results. It looks for the result with the smallest `E2` and returns the `E1` and `E2` from that result.

## ('avg', E1, E2, [body-atoms])

Executes `body-atoms`, collects the value of `E2` in the results, and puts their average `E1`.

## ('percentage', E1, [nominator-atoms], [denominator-atoms])

Executes both `nominator-atoms` and `denominator-atoms`. If `denominator-atoms` returns no results, it returns an empty list. If not, it returns the number of nominator results divided by the number of denominator results multiplied by 100 in `E1`. The result is a percentage [0..100].

## ('not', [body-atoms])

Executes `body-atoms`. If this gives any results, it returns an empty list. If there are no results, it returns a list with a single value: True

It implements the logical __not__ in a __closed world assumption__ where the absence of results implies the opposite.

## ('let', E1, C)

Assigns `C` to `E1`.

## ('det_equals', [body-atoms], E2)

Executes `body-atoms`. If the number of results equals `E2`, it returns all results. If not, it returns no results.

Implements the number determiner.

## ('det_greater_than', [body-atoms], E2)

Executes `body-atoms`. If the number of results is greater than `E2`, it returns all results. If not, it returns no results.

Implements the determiner "more than".

## ('det_less_than', [body-atoms], E2)

Executes `body-atoms`. If the number of results is less than `E2`, it returns all results. If not, it returns no results.

Implements the determiner "less than".

## ('all', E1, [range-atoms], [body-atoms])

First executes `range-atoms`. The number of results is called `range-count`. Then for each value of `E1` in the result, binds it to the variable of `E1` in `body-atoms` and executes body-atoms. If this gives any results, the value of `E1` is added to the results of the function. The number of results is called `body-count`. After that, if `range-count` equals `body-count`, all results are returned. If not, no results are returned.

Implements the all-quantor.

## ('none', [body-atoms])

Executes `body-atoms`. If this gives any results, it returns an empty list. If there are no results, it returns a list with a single value: True

## ('scoped', [body-atoms])

Executes `body-atoms` in a separate scope. All bindings that are produced in this function are discarded when the function completes. The function returns an empty set if `body-atoms` produces no results; it returns a set with the single tuple containing `None` if `body-atoms` does produce results.

It is used internally by the query optimizer, and can be used by the programmer to produce independent parts of the query.

## ('store', [body-atoms])

Binds `body-atoms` to the active variable values, and passes the atoms, one by one, to the solver, to be stored by an acceptepting module. This is a module that has a `write_function` for the predicate.

## ('destructure', <bound-atoms>, <free-atoms>...)

Performs destructuring, or unification 

For example:

    ('destructure', Atoms, just_left_of(A, B))

If the value of `Atoms` is, or contains, `just_left_of('pad', 'telephone')`, then A and B will be assigned `pad` and `telephone` respectively.

## ('findall', variable-name, body-atoms, result-variable)

Executes `body-atoms` and goes through the results, collecting the values of `variable-name`. The list of these values are stored in `result-variable`.

## ('find_all', [variable-name, variable-name...], body-atoms, result-variable)

Executes `body-atoms` and goes through the results, collecting the combination of values of `variable-name, ...` into rows. The list of these rows (lists) are stored in `result-variable`.

## ('find_one', variable-name, body-atoms, result-variable)

Executes `body-atoms` and collects the first (presumed only) value of `variable-name`. This value is stored in `result-variable`.

## ('fine_one', [variable-name, variable-name...], body-atoms, result-variable)

Executes `body-atoms` and goes collecting the first (presumed only) values of `variable-name, ...` into a row. This row is stored in `result-variable`.

