# Pipeline

In the examples before we have used the pipeline without introducing it. It needed some examples to get the idea.

A __pipeline__ is a sequence of steps that process the sentence from tokenization to response. It was popularized by the [Core Language Engine](https://mitpress.mit.edu/9780262512091/the-core-language-engine/) in 1992. The alternative to a processing pipeline is to perform several steps (parsing, semantic analysis, pragmatics) at the same time. A pipeline is more modular, simpler to build and easier to understand.

![Pipeline](../images/pipeline.drawio.png)

The pipeline in this library consists of __processors__, and these can be organized by the programmer. It's even possible to create your own processor and add it to your pipeline.

## Sentence request

Each new input sentence is placed in an object, a `SentenceRequest`, and passed through all processors. Each processor takes the products of one or more previous processors, which are stored in this request, and stores its own product in the request as well.

![Pipeline](../images/pipeline-request.drawio.png)

## Ambiguity resolution

The library also makes the pipeline responsible for ambiguity resolution. __Ambiguity__, the phenomenon that a sentence may have more than one possible meaning, appears at different levels of processing. It allows each processor to produce multiple alternative readings to the same input. Each of these alternatives will then be tried with the rest of the pipeline, until the first one succeeds. It's a form of depth-first tree traversal.

## Dependencies

Most processors depend on other processors. This dependency is expressed by passing references to these dependent processors to the constructor of the processor. By making the dependencies explicit you will be less inclined to put the processors in the wrong order.
