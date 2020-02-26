# Flower - The Friendly Federated Learning Framework

[![GitHub license](https://img.shields.io/github/license/adap/flower)](https://github.com/adap/flower/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/adap/flower/blob/master/CONTRIBUTING.md)
![Build](https://github.com/adap/flower/workflows/Python%20CI/badge.svg)

Flower is a framework for building federated learning systems. The design of Flower is based on a few guiding principles:

- **Customizable**: Federated learning systems vary wildly from one use case to another. Flower allows for a wide range of different configurations depending on the needs of each individual use case.
- **Extendable**: Flower originated from a research project at the Univerity of Oxford, so it was build with AI research in mind. Many components can be extended and overridden to build new state-of-the-art systems. 
- **Framework-independent**: Different machine learning frameworks have different strengths. Flower can be used with any machine learning framework, for example, [PyTorch](https://pytorch.org), [TensorFlow](https://tensorflow.org), or even raw [NumPy](https://numpy.org/) if you enjoy computing gradients by hand :)
- **Understandable**: Flower is written with maintainability in mind. The community is encouraged to both read and contribute to the codebase.

> Note: This is pre-release software. Incompatible API changes are likely.

## Installation

Flower can be installed directly from our GitHub repository using `pip`:

```bash
$ pip install git+https://github.com/adap/flower.git
```

Official [PyPI](https://pypi.org/) releases will follow once the API matures.

## Documentation

Documentation is still WIP and will be stored stored in `doc`.

## Contributing to Flower

We welcome contributions. Please see [CONTRIBUTING.md](CONTRIBUTING.md) to get started!
