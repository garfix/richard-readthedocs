# Grammar module

This module enables you to extend a grammar.

## ('learn_grammar_rule', head, [body-atoms])

The `learn_grammar_rule` predicate lets you learn the system a new grammar rule at runtime. For example:

~~~python
{ "syn": "common_noun(E1) -> /\w+/", "sem": lambda token: [ (token, E1) ],
    "exec": lambda token: [
        ('learn_grammar_rule', { "syn": f"common_noun(E1) -> '{token}'", "sem": lambda: [(token, E1)] }),
        ('add_relation', token, ['id']),
    ]
}
~~~

This example shows how a new common noun syntax rule (`common_noun(E1) -> 'a_new_noun'`) can be added to the grammar. The `exec` causes the following atoms to be executed by the executor. `learn_grammar_rule` learns the rule, while `add_relation` adds a new relation (table) to the database.

This function has been considered for the SIR system, but has not actually been used.
