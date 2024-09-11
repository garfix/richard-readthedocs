# Sentence context

The sentence context is a simple memory module whose contents is cleared whenever the composer starts processing a new parse tree. It contains inferences about the sentence that don't need to be stored outside the scope of processing this one sentence.

Here are two inferences of a rewrite rule that will be stored in the sentence context:

~~~python
("format", "list"), ("format_list", e2)
~~~

This information is used to process the sentence. When the sentence is comletely processed, these facts become useless. They are discarded when the next sentence is composed. The sentence context is cleared by the Composer. This is the only reason it has this dependency.


