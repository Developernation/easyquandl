from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION.txt'), encoding='utf-8') as f:
    version = f.readline()

setup(

    # How users can install this project:
    # $ pip install easyquandl
    # Where it will live on PyPI: https://pypi.org/project/easyquandl/
    name='easyquandl',  # Required

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,  # Required

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='Quandl real estate Python API wrapper',  # Optional

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/Developernation/easyquandl',

    # This should be your name or the name of the organization which owns the
    # project.
    author='Developernation',  # Optional

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email='easyquandl@googlegroups.com',  # Optional

    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',

        # TODO Pick your license as you wish
        # 'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.


        'Programming Language :: Python :: 3.6',

        'Programming Language :: Python :: 3.7',

    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.

    keywords='quandl realestate zillow',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #

    packages=find_packages(exclude=['tests']),  # Required

    install_requires=['interface',
                      'numpy',
                      'pandas',
                      'quandl',
                      'requests',
                      'tinydb',
                      'ujson',
                      ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install easyquandl[s]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional

        'tests': ['mypy',
              'unittest'],

    },

    # Often packages will need to depend on files which are not .py files: e.g. images, data tables, documentation,
    # etc. Those files need special treatment in order for setuptools to handle them correctly. The mechanism that
    # provides this is the MANIFEST.in file. This is relatively quite simple: MANIFEST.in is really just a list of
    # relative file paths specifying files or globs to include, e.g.:
    #   include README.rst
    #   include docs/*.txt
    #   include funniest/data.json
    # In order for these files to be copied at install time to the package’s folder inside site-packages, you’ll
    # need to supply include_package_data=True to the setup() function.
    #
    # https://python-packaging.readthedocs.io/en/latest/non-code-files.html
    include_package_data=True,

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },


    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional

        'Bug Reports': 'https://github.com/Developernation/easyquandl/issues',
        'Source': 'https://github.com/Developernation/easyquandl',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',

    },

)
