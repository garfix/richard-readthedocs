# Relative clauses

An example relative clauses is "The countries that are bordering China". The explicit sign of a relative clause is the word "that", but it is often left out.

A relative clause modifies a noun phrase, that is, it restricts the range of the instances of the np to a smaller set.

## Simple relative clause

~~~python
{ 
    "syn": "np -> np relative_clause", 
    "sem": lambda np, relative_clause: 
                create_np(exists, lambda: np(relative_clause)) 
},
{ 
    "syn": "relative_clause -> 'that' vp_no_sub", 
    "sem": lambda vp_no_sub: 
                lambda subject: vp_no_sub(subject) 
},
{ 
    "syn": "relative_clause -> vp_no_sub", 
    "sem": lambda vp_no_sub: 
                lambda subject: vp_no_sub(subject) 
}
~~~

Each relative clause creates a new np function (by calling `create_np`) by applying the original np to the modifying function. The `exists` quantifier is necessary but doesn't add meaning.

## Relative clause with AND

The `&` set operator is used here to create the intersection of the two `np` sets.

~~~python
{ 
    "syn": "np -> np relative_clause 'and' relative_clause", 
    "sem": lambda np, rc1, rc2: 
                create_np(exists, lambda: np(rc1) & np(rc2)) 
}


