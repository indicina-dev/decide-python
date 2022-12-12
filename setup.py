from setuptools import setup, find_packages

__version__ = "0.3.2"


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="indicina-decide",
    version=__version__,
    description="",
    packages=find_packages(),
    install_requires=["requests==2.28.1"],
    extras_require={
        'dev': [
            'pre-commit==2.20.0',
        ]
    },
    author="Indicina Engineering",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
