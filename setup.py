#!/usr/bin/env python

import setuptools

# VERSION MUST be defined on line 6
VERSION = '0.1'

test_deps = [
    'black',
    'pylint',
    'pytest',
    'pytest-cov',
    'tox',
]
extras = {
    'test': test_deps,
}

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='milliluk-tools',
    version=VERSION,

    description='TRS-80 Color Computer Tools',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/milliluk/milliluk-tools',

    # Author details
    author='Erik Gavriluk',

    # Choose your license
    license='CC BY-NC-ND 4.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    install_requires=[
        'pypng',
    ],
    tests_require=test_deps,
    extras_require=extras,
    python_requires='>=3.3',

    # What does your project relate to?
    keywords='coco image conversion trs-80 tandy',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=setuptools.find_packages(where='src'),
    package_dir={
        '': 'src',
    },

    entry_points={
        'console_scripts': [
            'max2png=milliluk.max2png.max2png:main',
            'cgp220=milliluk.cgp220.cgp220:main',
        ],
    },
)
