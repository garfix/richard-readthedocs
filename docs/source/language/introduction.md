# Introduction

There is no scientific consensus on linguistic semantics. Furthermore, semantics has mainly been studied as part of logic, where the meaning of a sentence is taken to be its truth value. In this library we're not just interested in a declarative logical representation of a sentence, we want to have it executed. Study on semantics has focused on quantification, which is just a fragment of language. Large parts are still terra incognita.

The easy approach I could take in this library would be to say: defining semantics attachment is up to you. Take whichever theoretical framework you like, and good luck! But this would leave you in the dark. Composing semantics is notoriously difficult and you need any help you can get.

As a consquence, the semantic constructs on the following pages are __experimental__. They are based partly on information from books on English grammar semantics, and partly on my own experience and ingenuity. The syntactic rules are loosely based on X-bar theory. The `find` construct was based on [Planner](https://en.wikipedia.org/wiki/Planner_(programming_language)), the procedural semantics engine of [SHRDLU](https://en.wikipedia.org/wiki/SHRDLU). The `dnp` is based on the `quant` construct of the Core Language Engine, etc.

I encourage you to come up with other approaches, and to experiment. The library was designed to make computational semantics as simple as possible, but that doesn't mean it is. It's a struggle, and I hope you're into it! :)

