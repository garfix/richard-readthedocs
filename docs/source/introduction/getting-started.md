# Getting started

Welcome to Richard!, a Python library that translates human language into Python code. It allows you to query a database, create commands to make your computer do things, and learn the computer new words and rules.

Richard! adheres to the principle of progressive disclosure of complexity: simple systems can be built using little code, complex systems can be built as well, but require a lot more code.

The system is still very much in development, so don't expect it to work flawlessly, and the code you develop will probably not work with the next release of the library. But you will be able to experiment with natural language understanding.

## Demos

You're probably interested to see some demos of the system. See [the introduction to the demos](../demos/introduction.md) for how to find them and how to run them.

## Start your own project

After that, pick a demo that looks like the system you intend to design. Copy it and adapt it to suit your needs.

In your project you build a processing pipeline. It consists of control blocks with processors, like this:

~~~python
pipeline = Pipeline([
    FindOne(tokenizer),
    FindOne(parser),
    TryFirst(composer),
    TryFirst(executor),
    TryFirst(responder)
])
~~~

When you have a pipeline, it can process a sentence that is entered by the user, like this:

~~~python
question = "How many children has Madonna?"
result = pipeline.enter(SentenceRequest(question))
~~~

The result you get is the product of the last processor in the pipeline. This result can be used by you to show it to the user.

## Grow your project by extending a dialog

When looking at the demos you'll notice that they all use a demo dialog to test all interactions. Such a dialog serves as a means to automatically test your system, to make sure that previous constructions still work after you change your modules.

Start with a single, simple test, make it work, then add another one. From simple to complex.

The library comes with a testing framework that shows you the intermediate results of your request, to help debugging. To use it, run your test through this code:

~~~python
logger = Logger()
logger.log_all_tests()
logger.log_products()
logger.log_stats()

tester = DialogTester(self, tests, pipeline, logger)
tester.run()

print(logger)
~~~

The `logger` class has several options. Turn them all on at first. When you're completely done with the system, change the settings to `logger.log_no_tests()` to skip the logs and just perform the tests.

Test your code in the command line, like this:

~~~bash
python3 -m unittest tests/integration/Chat80_test.py
~~~

If you're using Bash, the intermediate results show up with colored headings.

## Documentation

Now you know how to get started, read the documentation to find out more about the system:

* __Introduction__ teaches you the basics
* __Language__ shows you how to turn language constructs into semantic constructs
* __Modules__ provide information about the available modules

