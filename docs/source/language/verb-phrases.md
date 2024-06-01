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
