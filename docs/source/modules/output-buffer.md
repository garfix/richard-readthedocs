# Output buffer

Whenever a system want to output information to the user it just places facts in the output buffer. The client picks up these facts, generates a sentence from them and clear the output buffer.

The following output types are available from the BasicOutputBuffer:

* `output_value(value)`
* `output_value_with_unit(value, unit)`
* `output_table(results, units)`
* `output_list(elements)`
