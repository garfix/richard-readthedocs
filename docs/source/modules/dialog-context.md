# Dialog context

The dialog context is a simple memory module that contains the inferences that are made during the processing of the sentence and that are stored during the remainder of the dialog.

## Inferences

Here's an example of an inference that is stored in the dialog context:

~~~python
{
    "syn": "noun(E1) -> 'river'",
    "sem": lambda: [('river', E1)],
    "inf": [('dialog_isa', e1, 'river')]
}
~~~

The inferences are in the `inf` field. The inference here, `('dialog_isa', e1, 'river')` says: "e1 is a river". When this sentence is composed by the Composer, it stores this fact in the dialog context. From that point it is available by all modules like any other tuple in a database.

Why would you create both a `sem` and an `inf` for the same information, that E1 is a river? The `sem` is used to filter out the `E1`s that are not a river. The `inf` is used to provide information to predicates elsewhere in the sentence, or even in sentences further up in the dialog. For example, here is the predicate `has_population`:

~~~python
    def has_population(self, values: list, context: ExecutionContext) -> list[list]:
        term = context.arguments[0]
        type = ""
        if isinstance(term, Variable):
            isa = context.solver.solve1([('isa', term.name, Variable('Type'))])
            if isa is not None:
                type = isa["Type"]

        if type == 'city':
            out_values = self.ds.select("city", ["id", "population"], values)
            out_values = [[row[0], row[1] * 1000] for row in out_values]
        else:
            out_values = self.ds.select("country", ["id", "population"], values)
            out_values = [[row[0], row[1] * 1000000] for row in out_values]
        return out_values
~~~

If `E1` is a city, `has_population` needs to retrieve its size form the `city` table. If it's a country, it comes from the `country` table.

## Dialog variables

The variables `E1`, `E2`, `E3` etc are limited in scope to the rule itself. When the sentence is composed, these variables unified and turned into dialog variables `$1`, `$2`, `$3` etc. Each new entity gets its own dialog variable. Numbering doesn't restart at a new sentence, it just continues with `$4`, `$5`, `$6`.

## Reified variables

The facts inferred from the sentence are stored in the dialog context. However, it is not possible to store `('isa', E1, 'river')` in the database, since `E1` is a variable! Still, we want to store information __about the variable__, rather than one of its bindings, in the database. To do that the variable is turned into a string with the same name. This is making an abstract entity concrete, or __reification__. The result is `('isa', e1, 'river')`. Note the lower cased `e1`.
