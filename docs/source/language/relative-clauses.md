# Relative clauses

An example relative clauses is "The countries that are bordering China". The explicit sign of a relative clause is the word "that", but it is often left out.

A relative clause modifies a noun phrase, that is, it restricts the range of the instances of the np to a smaller set.

## Simple relative clause

~~~python
{
    "syn": "relative_clause(E1) -> 'that' vp_nosub_obj(E1)",
    "sem": lambda vp_nosub_obj: vp_nosub_obj
},
{
    "syn": "relative_clause(E1) -> 'that' vp_noobj_sub(E1)",
    "sem": lambda vp_noobj_sub: vp_noobj_sub
}
~~~

## Relative clause with AND

~~~python
{
    "syn": "relative_clause(E1) -> relative_clause(E1) 'and' relative_clause(E1)",
    "sem": lambda relative_clause1, relative_clause2: relative_clause1 + relative_clause2
}
~~~

