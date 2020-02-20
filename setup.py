import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PanaXea", # Replace with your own username
    version="0.9.0-dev0",
    author="Dario Panada",
    author_email="dario.panada@manchester.ac.uk",
    description="A minimalist framework for agent-based modelling in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/DarioPanada/panaxea",
    packages=setuptools.find_packages(exclude=("tests", "tests*",
                                               "tests/resources*",
                                               "examples", "examples*")),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
