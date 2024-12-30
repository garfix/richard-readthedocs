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
    "syn": "number(E1) -> /\d+/",
    "sem": lambda token: int(token)
}
~~~

Finally there are expressions like "10 million", which must resolve to a number in order to be useful.

~~~python
{
    "syn": "number(E1) -> number(E1) 'million'",
    "sem": lambda number: number * 1000000
}
~~~
