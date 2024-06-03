# Verbs

A verb is the heart of a sentence, or of a relative clause. It is expressed logically as a predication over a fixed number of arguments. The verb "flow through" for example is in essence `flow_through(X, Y)`. The first argument is called the `subject`, the second `object`, a possible third `indirect object`.

The word `through` in this example is called the `particle` of the verb. Typically it is located just after the verb, but in many cases another phrase is placed between the verb and the particle.

In applications where time plays a role, or application that make statements about events or even states, the `event` needs to be represented explicitly. This is done by adding an extra event argument `E`: `flow_through(E, X, Y)`. In the examples below we will not do that yet.

Once the event has been represented, it becomes possible to create separate relations for the subject and object: `flow_through(E), subject(E, X), object(E, Y)`. This has the advantage that the verb is more flexible. In most cases however, this flexibility is not needed, and the extra relations just add to the complexity and syntactic overhead of the application. Use it only if you have a clear use case for it.

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

## Transitive verb phrases without subject

In many cases it is useful or necessary to separate the subject from the verb phrase. In this case the subject will be passed to the semantics of the verb phrase as an argument.

~~~python
{ 
  "syn": "tv_no_sub -> tv np", 
  "sem": lambda tv, np: lambda subject: np(tv(subject)) 
}
~~~

This verb phrase without subject (`tv_no_sub`) first creates a predicate function by passing the `subject` it gets from the parent node to the `tv` (transitive verb) and then executes the `np` (noun phrase) with the new predicate as an argument. This results in a new range of instances.

## Passive transitive verb phrases

A passive sentence reverses the order of subject and object: "John picked up the block" becomes "The block was picked up by John". Whereas usually the subject is the focus of the sentence, in a passive sentence the focus is the object, and in questions, the object provides the answer. 

This is the basic syntactic form of a passive sentence:

~~~python
{ 
  "syn": "tv_no_obj -> tv_passive 'by' np", 
  "sem": lambda tv_passive, np: 
            lambda object: np(tv_passive(object)) 
}
~~~

Note the use of `tv_passive` in stead of `tv`. The passive form is problematic for the transitive verb definitions, like this one, that specify that the subject comes first. For passive sentences the order of subject and object would have to be reversed.

~~~python
{ 
  "syn": "tv -> 'flow' 'through'", 
  "sem": lambda: 
            lambda subject: lambda object: model.find_relation_values('flows-through', [subject, object]) 
}
~~~

To avoid having both passive and an active form for each transitive verb, we have introduced a `transformation` that wraps the active tv-function and makes it passive.

~~~python
{ 
  "syn": "tv_passive -> tv", 
  "sem": lambda tv: 
            lambda object: lambda subject: tv(subject)(object) 
}
~~~

