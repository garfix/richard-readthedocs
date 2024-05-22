# Introduction

The study of linguistic semantics has not yet reached maturity. Many studies have been done on the subject, but together they don't form a coherent body of knowledge ready to be used. Furthermore, semantics has mainly been studied as part of formal logic, where the meaning of a sentence is taken to be its truth value. In this library we're not just interested in a declarative representation of a sentence, we want to have it executed. This has a profound effect on the way semantics is represented. The world of executable semantics is still very much terra incognita.

The easy approach I could take in this library would be to say: defining semantics attachment is up to you. Take whichever theoretical framework you like, and good luck! But this would leave you in the dark. Composing semantics is notoriously difficult and you need any help you can get.

As a consequence, take the semantic constructs on the following pages as __a workable approach__. It is based partly on information from books on English grammar semantics, and partly on my own experience and ingenuity. The syntactic rules are loosely based on X-bar theory. The `find` construct was based on [Planner](https://en.wikipedia.org/wiki/Planner_(programming_language)), the procedural semantics engine of [SHRDLU](https://en.wikipedia.org/wiki/SHRDLU). The `dnp` is based on the `quant` construct of the Core Language Engine, etc.

I encourage you to come up with other approaches, and to experiment. The library was designed to make computational semantics as simple as possible, but that doesn't mean it is. It's a new world and we are all pioneers!

