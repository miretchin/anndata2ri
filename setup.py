from setuptools import setup

setup(
    name = 'anndata2ri',
    author = 'Philipp A.',
    author_email = 'flying-sheep@web.de',
    
    classifiers = [
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3',
    'Programming Language :: R',
    'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    
    packages=find_packages();
    
    install_requires=[
        "rpy2 >= 3.0.0.dev", # 3.0.1 fixes crashes!
        "tzlocal", # for pandas2ri
        "numpy",
        "pandas",
        "anndata",
        "pytest",
        "get_version",
        "scipy",
        "future-fstrings",
    ],
    
    python_requires = '>=3.6',
    
    project_urls={
        'home-page': 'https://github.com/flying-sheep/anndata2ri'
    },
    
    extras_require = {
        'test': ['pytest', 'pytest-faulthandler']
    },
)
