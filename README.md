# PanaXea

## Introduction

Welcome to **PanaXea**!

A minimalist framework to easily and quickly develop agent-based models in Python. PanaXea aims to provide a set of tools and utilities to rapidly achieve common tasks in agent-based model development such as schedule and environment management, agent behaviour setup, etc. 

It provides:

* Easy configuration model properties and keep track of parameter values and outputs;
* A scheduling system that implements model progression as a set of epochs, and makes sure all agents are executed within a single epoch;
* Classes for 2D and 3D environments, and helper methods for these;
* Generic classes for agents and other steppables providing commonly used functionalities.

## Table of Contents

* [Contributing](CONTRIBUTING.md) - PanaXea welcomes contributors, see the guidelines for an overview of how to participate in the project;
* [Getting started](#getting-started) - A quick description of how to get started designing your own models;
* [Installation](#installation) - A description of how to install the project;
* [License](LICENSE.md) - PanaXea is distributed under MIT license;

## Getting started

See examples in `./examples` for a few simple models to get you started.

The documentation is available on [readthedocs](https://panaxea.readthedocs.io/en/latest/).

PanaXea will work with both Python 2 and Python 3.

The `core` and `toolkit` modules do not require any additional packages to be used.

It might be useful to have [Nox](https://nox.thea.codes/) installed to run the end-to-end linting/testing/documenting pipeline. This will also require you to have [pytest](https://docs.pytest.org/en/latest/), [sphinx](https://www.sphinx-doc.org/) and [flake8](https://flake8.pycqa.org/en/latest/) installed.

Running some of the examples requires [NumPy](https://numpy.org/) and [Matplotlib](https://matplotlib.org/).

Overall, you might be more comfortable using an [Anaconda](https://www.anaconda.com/distribution/) distribution of Python.

## Installation

As a first possibility you may clone/download the project and make sure the `core` module (and the `toolkit` module if you plan on using it) are added to your `PYTHONPATH`.

You may also install using pip:

`pip install PanaXea`

## Contact

The project is maintained by Dario Panada, PhD student at The University of Manchester (UK). - _dario.panada at manchester dot ac dot uk_
