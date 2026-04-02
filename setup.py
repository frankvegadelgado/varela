from pathlib import Path

import setuptools

VERSION = "0.3.3"

NAME = "varela"

INSTALL_REQUIRES = [
    "hvala>=0.0.7"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Compute the Approximate Vertex Cover for undirected graph encoded in DIMACS format.",
    url="https://github.com/frankvegadelgado/varela",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/varela",
        "Documentation Research": "https://dev.to/frank_vega_987689489099bf/the-varela-algorithm-3nbm",
    },
    author="Frank Vega",
    author_email="vega.frank@gmail.com",
    license="MIT License",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires=">=3.12",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["varela"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'cover = varela.app:main',
            'test_cover = varela.test:main',
            'batch_cover = varela.batch:main'
        ]
    }
)