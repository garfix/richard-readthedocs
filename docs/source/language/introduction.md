# Introduction

The study of linguistic semantics comes in many shapes and sizes. Many studies have been done on the subject, but together they don't form a coherent body of knowledge ready to be used. Semantics has mainly been studied in the context of formal logic, where the meaning of a sentence is taken to be its truth value, and provability was the aim.

In this library we're not interested in a formal logical representation of a sentence, we want to __execute__ the sentence. Most historical systems produce declarative structures, like first order predicate logic formulas, or Horn clauses (as in Prolog). These need an engine to be executed. This library proceduces Python code, that can be executed directly. This has the advantage that the full power of Python can be used to produce actions. It also means that the library can be ported to any other modern language. The disadvantage, at the moment, is that we somewhat have to invent the wheel.

Thinking of semantics in terms of code in stead of logic means we have to think about the __performance__ of the implementation. This has a profound effect on the way semantics is represented. The world of executable semantics is still very much terra incognita.

The easy approach I could take in this library would be to say: defining semantics attachment is up to you. Take whichever theoretical framework you like, and good luck! But this would leave you in the dark. Composing semantics is notoriously difficult and you need any help you can get.

As a consequence, take the semantic constructs on the following pages as __a workable approach__. It is based partly on information from books on English grammar semantics, and partly on my own experience and ingenuity.

I encourage you to come up with other approaches, and to experiment. The library was designed to make executional semantics as simple as possible, but that doesn't mean it is. It's (still!) a new world and we are all pioneers!

## Choice of grammar

There are many kinds of [grammar](https://en.wikipedia.org/wiki/Grammar). Many grammars are suitable to computational linguistics in some way. Which one is best I don't know. Historically most natural language systems use some form of [Phrase Structure Grammar](https://en.wikipedia.org/wiki/Phrase_structure_grammar), probably because it's easier to write a parser for them. In the examples here you will find terms used in [X-bar theory](https://en.wikipedia.org/wiki/X-bar_theory), like "nbar", but the grammars don't adhere to this theory other than that.

## The meaning of a sentence

In first order predicate logic the intension of a sentence is its formula, and its extension a truth value. How is this different in this library?

The intension here is a list of logical atoms, implemented by Python code, and the extension is determined by the top level sentence. Typically the result of a sentence consists of the bindings of a single variable. The result is a __list__. But there are exceptions.

A __yes/no__ question is just interested in the fact if there are any results at all. If

Some sentences return a __single value__, like "How many countries does the Danube flow through?"

Exceptionally, a sentence could ask for a combination of instance and attribute. As in "What are the capitals of the countries bordering the Baltic?" in this case the __table__ of entities (country) and their attributes (capital) would be considered the value of the sentence.
