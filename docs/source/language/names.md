# Names

A name, or proper noun, is a special noun because it is not listed in the lexicon. It is looked up in the model (in a database), but only when the syntactic structure expects a proper noun. __Named Entity Recognition__ does not take place before parsing, but during execution.

~~~python
{
    "syn": "noun(E1) -> proper_noun(E1)",
    "sem": lambda proper_noun: proper_noun
},
{
    "syn": "proper_noun(E1) -> token(E1)",
    "sem": lambda token: [('resolve_name', token, E1)]
}
{
    "syn": "proper_noun(E1) -> token(E1) token(E1)",
    "sem": lambda token1, token2: [('resolve_name', token1 + " " + token2, E1)]
}
~~~

The meaning of the proper noun is a call of `resolve_name`, a predicate that is treated specially by the query optimizer (atoms with this predicate are always performed first). Resolve name takes a `token` as an argument. `token` has the special property of producing the literal text in the sentence as its semantics.

`resolve_name` needs to be implemented in your module. Here's an example from the CHAT-80 replication:

~~~python
def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
    name = values[0].lower()

    for type in ["country", "city", "sea", "river", "ocean", "continent"]:
        out_values = self.ds.select(type, ["id", "id"], [name, None])
        if len(out_values) > 0:
            context.solver.write_atom(('isa', context.arguments[1].name, type))
            return out_values

    if name == 'equator':
        return [['equator', 'equator']]

    raise ProcessingException("Name not found: " + name)
~~~

Your implementation may either be simpler or more complex. Basically the function looks up the name in all tables where names are stored.

The `ProcessingException` will be the result of the process and the block, and will end up in the response to the user.

## Using inferences

This is a naive implementation as the same name may be available in multiple entity types. A better implementation makes use of inferences to induce the type of the entity. `resolve_name` can then just select the table associated with that entity.

Take the sentence: "Which countries border China?" As a human we know that China is a country. The system doesn't. So it could look up the word "China" in the persons table, the cities table, the countries table, etc.

Now if we add some inferences to the word "borders", like this:

~~~python
{
    "syn": "tv(E1, E2) -> 'borders'",
    "sem": lambda: [('borders', E1, E2)],
    "inf: [('isa', e1, 'country'), ('isa', e2, 'country')]
}
~~~

When the system composes this sentence, it creates the inferences `e1 isa country` and `e2 isa country` and places these facts in the dialog context.

Then when the sentences is executed, and `resolve_name` comes along, the code may use these inferences, like this:

~~~python
def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
    name = values[0].lower()
    term = context.arguments[0]

    type = ""
    if isinstance(term, Variable):
        isa = context.solver.solve1([('isa', term.name, Variable('Type'))])
        if isa is not None:
            type = isa["Type"]

    if type == "country":
        out_values = self.ds.select("country", ["id", "id"], [name, None])
    elif type == "person":
        out_values = self.ds.select("person", ["id", "id"], [name, None])
    else:
        raise ProcessingException("Name not found: " + name)

    return out_values
~~~

## Learning names

To make the system learn a new name when it first occurs, you could use the following code to implement `resolve_name` in a module. It is taken from _Cooper's demo_.

~~~python
def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
    name = values[0].lower()
    id = values[1]

    out_values = self.ds.select("name", ["name", "id"], [name, None])
    if len(out_values) > 0:
        return out_values
    else:
        # if id is given, a new name is linked to that id
        if id is None:
            # otherwise a new id is created for the name
            id = context.arguments[1].name
        self.ds.insert("name", ["name", "id", ], [name, id])
        return [
            [name, id]
        ]
~~~

The predicate takes an `name` and an `id`. The `id` may be `None`. First the function tries to look up the `id` from the `name` in the database. When found, it is returned. If it is not found, an `id` is created from the name of the dialog variable (which is different for each entity), and inserted into the database.

## Synonyms

To express the fact that one name refers to the same entity as another name, you can use this sem:

~~~python
{
    "syn": "s(E1) -> proper_noun(E1) 'is' proper_noun(E1)",
    "sem": lambda proper_noun1, proper_noun2: proper_noun1 + proper_noun2,
}
~~~

## Compound noun names

This section is about compound nouns like "sodium chloride", used as proper nouns, when the class of the entity is to be inferred from the name. In the case of "sodium chloride", that it is a cloride. You can infer this by using an inference ("dialog").

~~~python
# proper noun
# "magnesium"
{ "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: [('resolve_name', token, E1)] },
# "ferrous sulfide"
{ "syn": "proper_noun(E1) -> token(E1) token(E1)", "sem": lambda token1, token2: [('resolve_name', token1 + " " + token2, E1)] },
{ "syn": "proper_noun(E1) -> token(E1) main_noun(E1)", "sem": lambda token, main_noun: [('resolve_name', token + ' ' + main_noun, E1)] },

# the major part a compound noun
{ "syn": "main_noun(E1) -> 'oxide'", "sem": lambda: 'oxide', "dialog": [("oxide", e1)] },
{ "syn": "main_noun(E1) -> 'chloride'", "sem": lambda: 'chloride', "dialog": [("chloride", e1)] },
{ "syn": "main_noun(E1) -> 'sulfide'", "sem": lambda: 'sulfide', "dialog": [("sulfide", e1)] },
~~~
