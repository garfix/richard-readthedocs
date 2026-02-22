The **solver** processes a series of atoms and returns a list of different variable bindings.

For example, this list of atoms

~~~python
[('river', E1), ('contains', 'india', E1)]
~~~

may result in the following bindings:

~~~python
[
    {'E1': 'Ganges'},
    {'E1': 'Indus'},
]
~~~

Those are the basics. Now let's dig a bit deeper.

## Atoms: predicates and formal parameters

An atom consists of a **predicate** and some **formal parameters**. In this example

~~~
('father_of', E1, E2)
~~~

`father_of` is the predicate and `E1` and `E2` are formal parameters. The scope of the formal parameters is the rule in which they occur. Different rules may reuse the same parameters and the meaning of the variable is different in each rule.

The **semantic composer** turns these rule-scoped variables into dialog-scoped variables. When these atoms are executed by the **semantic executor** the look like this:

~~~
('father_of', $7, $8)
~~~

## Unbound, bound, and dereferenced arguments

**unbound arguments** are the variables and constants passed to an atom at runtime, either directly or via sub-goaling. When the unbound arguments' variables are replaced by the values found in a binding, this results in **bound arguments**. These bound arguments may still hold variables. When all variables are followed down their **variable chain** and the unbound arguments' variables are replaced by their dereferenced values, this results in **dereferenced arguments**.

An example of dereferencing: if `E3` has value `E5` (another variable), and `E5` has value `E2` and `E2` has value "Sue", then "Sue" is the dereferenced value of `E3` (and `E5` and `E2`).

Let's say `('father_of', A, B)` is called with the arguments: `E1` and `E2` and the binding: `{E1: "John", E2: E3, E3: "Sam", E4: "Susan"}`. 

In this example

* `A`, and `B` are the formal parameters of the atoms. They appear literally in the rule definition, and are not used by the application
* `E1` and `E2` are the unbound arguments passed to the function, filling the slots of the formal parameters
* `John` and `E3` (the variable) are the bound arguments of the function
* `John` and `Sam` are the dereferenced arguments: `Sam` is the value of `E3`

Another example: in `('think', E1, A)` and `A` = `('like, E1, E2)`, `E1` = 'john' and `E2` = 'jane', the atom is first bound to `('think', E1, ('like, E1, E2))` and then to `('think', 'john', ('like, 'jane', 'john))`

## Atom execution

When the solver solves an atom, it passes an `ExecutionContext` to the atom, an object that contains all the data and services the atom may need to do it's job.

~~~python
class ExecutionContext:
    relation: Relation
    solver: SomeSolver
    sentence: SemanticSentence
    model: SomeModel
~~~

All atom execution functions have the following signatue:

~~~python
def some_predicate_name(self, arguments: list, context: ExecutionContext) -> list[list]
~~~    

The different arguments are available a follows:

* formal paramaters are available via `context.relation.formal_parameters`
* bound and dereferenced arguments via `arguments`

