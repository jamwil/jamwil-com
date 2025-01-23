+++
title = "Notes from Stephen Wolfram's ChatGPT primer"
date = "2023-04-07T02:15:00Z"
[taxonomies]
tags = ["chat-gpt", "llm", "machine-learning", "transformers"]
categories = ["Technology"]
+++

**Source Material:**
[Stephen Wolfram, 2023-02-14](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/)

ChatGPT is a large-scale transformer-based language model that is designed to
predict the next word in a sentence given the context of what has been said. It
is a neural network with 175 billion parameters that has been trained on a vast
corpus of text, enabling it to form and apply a semantic structure to human
language.

The name ChatGPT stands for Generative Pre-trained Transformer. **Generative**
means that the model is capable of generating new text rather than just
recognizing patterns in existing text. **Pre-trained** means that the model has
been trained on a large corpus of text before being fine-tuned for a specific
task. **Transformer** refers to the specific type of neural network architecture
which is designed to better handle long-term dependencies between words in a
sentence.

To accomplish its task, ChatGPT uses a technique known as **unsupervised
learning**, which allows it to learn patterns in the data without being
explicitly taught. Instead of being trained on explicit examples of inputs and
their associated outputs like in **supervised learning**, the model is given a
large corpus of text and is trained to predict the next word in a sentence by
masking the latter part of the sentence and having it predict what should come
next. It then compares what it generated with the masked text, and iteratively
adjusts its parameters to minimize the error.

To evaluate how well the model performs on each iteration, a **loss function**
is used. The loss function calculates how far away the model's predictions are
from the desired outcome, and the neural net weights are adjusted in a way that
minimizes the result of the loss function.

Training the model both optimizes the neural net weights and produces
**embeddings**, which are a way of representing the meaning of words as arrays
of numbers (in the vague, undefinable sense of ‘meaning’). Nearby words are
represented by nearby numbers. ChatGPT takes this concept further by generating
embeddings not just for individual words, but for entire sequences of words.

These embeddings are then used to predict the probabilities of different words
that might come next in a sentence. This is accomplished using a **transformer**
architecture, which is designed to better handle dependencies between tokens in
the input and output even when they are far from each other in the input
sequence. One of the defining features of the transformer is its use of an
**attention mechanism**, which involves certain neurons focusing more on
relevant parts of the sequence than others. This allows ChatGPT to take into
account the context of the conversation that's taken place, which can inform the
next token that's generated. The attention mechanism also allows ChatGPT to
capture context from the prior conversation even when that context is not
adjacent to the token being generated. This is the main reason ChatGPT comes
across as a coherent entity.

Finally, ChatGPT uses a **temperature** setting to introduce a degree of
randomness into its predictions, which can make the output more diverse and
interesting.

---

What strikes me as the most profound point Stephen makes is the success of
ChatGPT as a scientific _discovery_ in that it shows that there may be simple
rules that describe how the semantics of human language can be arranged that we
ourselves don’t yet understand. Studying the pathways and structures ChatGPT
uses could help deepen our own understanding of human language.

<!-- more -->
