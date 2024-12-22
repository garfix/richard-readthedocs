# Custom modules

Your application will likely have a custom module. It contains the relations your application adds. Each relation is linked to a database table, executes a command, or performs any other custom behaviour.

Here's an example that shows you the basics. The module can take a data source as a dependency if it needs to retrieve and store records. The constructor defines its relations. The rest of the class contains the implementations of each of the relations.

~~~python
class SIRModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("have", query_function=self.have))
        self.add_relation(Relation("part_of_n", query_function=self.part_of_n, write_function=self.common_write, arguments=['part', 'whole', 'number'])),


    def part_of_n(self, values: list, context: ExecutionContext) -> list[list]:
        part_variable = context.arguments[0]
        whole_variable = context.arguments[1]

        results = self.ds.select(context.relation.predicate, context.relation.arguments, values)

        return results


    # have(whole, part)
    # the verb have is always very abstract, but in this case it also handles with information on the class-level
    def have(self, values: list, context: ExecutionContext) -> list[list]:

        # solving based on class information

        whole_variable = context.arguments[0]
        part_variable = context.arguments[1]

        whole_type = None
        if isinstance(whole_variable, Variable):
            whole_type = self.get_name(context, whole_variable.name, values[0])

        part_type = None
        if isinstance(part_variable, Variable):
            part_type = self.get_name(context, part_variable.name, values[1])

        results = context.solver.solve([('part_of_number', part_type, whole_type, Variable('N'))])

        if len(results) == 0:
            raise ProcessingException(f"Don't know whether {part_type} is part of {whole_type}")

        number = results[0]['N']
        response = ResultIterator([None, None], number)

        return response

~~~

## ResultIterator

The example class above demonstrates the **ResultIterator**. This object is useful in the edge case where you need to return a set of instances, but these instances don't have an individual identity. It is used in combination with `count`, where a possibly very large set of instances is expected, but we're only interested in the number of them. The `ResultIterator` object ensures that the length of the object is returned directly, without iterating over all items. The the SIR demo for an example.

