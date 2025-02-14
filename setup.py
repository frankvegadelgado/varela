from pathlib import Path

import setuptools

VERSION = "0.0.8"

NAME = "varela"

INSTALL_REQUIRES = [
    "numpy>=2.2.1",
    "scipy>=1.15.0",
    "networkx[default]>=3.4.2"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Estimating the Minimum Vertex Cover with an approximation factor of ≤ 3/2 for an undirected graph encoded in DIMACS format.",
    url="https://github.com/frankvegadelgado/varela",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/varela",
        "Documentation Research": "https://www.researchgate.net/publication/388791285_The_Unique_Games_Conjecture",
    },
    author="Frank Vega",
    author_email="vega.frank@gmail.com",
    license="MIT License",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires=">=3.10",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["varela"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'approx = varela.app:main',
            'test_approx = varela.test:main',
            'batch_approx = varela.batch:main'
        ]
    }
)