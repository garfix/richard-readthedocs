# Numbers

Some numbers can be listed in the lexicon, but not all of them. Let's start with the ones that should be listed in the lexicon:

~~~python
{ "syn": "number(E1) -> 'one'", "sem": lambda: 1 },
{ "syn": "number(E1) -> 'two'", "sem": lambda: 2 },
{ "syn": "number(E1) -> 'three'", "sem": lambda: 3 },
~~~

Then the ones that can't:

~~~python
{
    "syn": "number(E1) -> token(E1)",
    "sem": lambda token: int(token),
    "if": lambda token: re.match('^\d+$', token)
}
~~~

`E1` is bound to an integer that matches the token in the input. To start, `number` rewrites to `token`. The semantics of token is its literal form. So the meaning of the token "123" is "123". The sem of this rule simply converts the string to an integer. But there's a condition attached to it. The `if` says that this rule only applies if the token matches the regular expression. This is just a Python expression so the test could be implemented in any way you need.

Finally there are expressions like "10 million", which must resolve to a number in order to be useful.

~~~python
{
    "syn": "number(E1) -> number(E1) 'million'",
    "sem": lambda number: number * 1000000
}
~~~

## Other forms of annotation

The technique to parse numbers can be used for other entities as well, like dates, email addresses and amounts of money. For some forms it will be useful to change the tokenizer as well, to produce single tokens for each entity.

