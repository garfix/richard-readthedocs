# Output generation

When the system needs to produce output, this output is not sent directly to the client. It is not printed to the screen. It is not even sent to a callback function to be processed in any other way. Rather, it is stored as a data structure in the sentence context.

The write grammar handles this output type like this:

~~~python
{
    "syn": "s() -> format(E1)",
    "if": [('output_type', 'list'), ('output_list', E1)],
    "format": lambda elements: format_list(elements),
}

def format_list(elements):
    elements.sort()
    return ", ".join(elements)

~~~

The output generator looks for the `s` node, and checks if the `if` clause of the rule matches. Here is matches the output type `list` and binds the variable `E1` to the element list. `s` then rewrites to `format`, which means that the `format` function of the rule is called, passing the list. This calls the function `format_list` which sorts the elements and concatenates them using a comma. This forms the actual output.

## The order of the rules

Whereas one should not depend on the order of the rules in the read grammar, the order in the write grammar matters. The first rule that matches is applied, further rules are skipped.

## Output types

The following output types are available from the BasicOutputBuffer:

* `output_value(value)`
* `output_value_with_unit(value, unit)`
* `output_table(results, units)`
* `output_list(elements)`

Examples of all types can be found in the CHAT-80 demo.

## Optional output

Adding a `?` to a category will make it optional. If it fails, it is simply skipped from the output, but the rule still holds.

~~~python
{
    "syn": "custom() -> just_left_of(E1)? just_right_of(E1)? left_of(E1)? right_of(E1)?",
    "if": [('output_type', 'location'), ('output_location', E1)],
}
~~~
