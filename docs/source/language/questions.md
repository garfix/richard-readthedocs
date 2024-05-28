# Questions

## Where

A where question requests the location of an entity.

~~~python
{ 
    "syn": "s -> 'where' copula np '?'", 
    "sem": lambda np: lambda: model.get_matching_attribute_range('location-of', np())
}
~~~

## Yes/no

Yes/no questions produce a range of entities. If the list contains any values, the answer is "yes", if not, it is "no".

~~~python
{ 
    "syn": "s -> aux_do np vp_no_sub '?'",  
    "sem": lambda np, vp_no_sub: lambda: filter(np(), vp_no_sub) 
}
~~~

