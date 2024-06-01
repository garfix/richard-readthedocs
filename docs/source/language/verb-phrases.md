# Verbs

## Transitive verb

In the phrase "Afghanistan borders China", "borders" is a transitive verb (`tv`): it has a `subject` ("Afghanistan") and an `object` ("China").

The meaning of the verb needs to consist of a subject-function within an object function, as below:

~~~python
{ "syn": "tv -> 'border'", 
  "sem": lambda: 
            lambda object: 
                lambda subject: 
                    model.find_relation_values('borders', [subject, object]) },
~~~

It can't be a single function with two parameters, because the functions are used in different places.

## Verb phrases without subject

In many cases it is useful or necessary to separate the subject from the verb phrase. In this case the subject will be passed to the semantics of the verb phrase as an argument.

~~~python
{ 
  "syn": "vp_no_sub -> tv np", 
  "sem": lambda tv, np: lambda subject: np(tv(subject)) 
}
~~~

This verb phrase without subject (`vp_no_sub`) first creates a predicate function by passing the `subject` it gets from the parent node to the `tv` (transitive verb) and then executes the `np` (noun phrase) with the new predicate as an argument. This results in a new range of instances.
