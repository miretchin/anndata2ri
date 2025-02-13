"""
Converter between Python’s AnnData and R’s SingleCellExperiment.
"""
__all__ = ["activate", "deactivate", "py2rpy", "rpy2py", "converter"]


from typing import Any

from get_version import get_version
from rpy2.rinterface import Sexp


__author__ = "Philipp Angerer"
__version__ = get_version(__file__)

del get_version


from .conv import converter, activate, deactivate
from . import py2r, r2py

def py2rpy(obj: Any) -> Sexp:
    """
    Convert Python objects to R interface objects. Supports:

    - :class:`~anndata.AnnData` → :rcls:`SingleCellExperiment::SingleCellExperiment`
    """
    return converter.py2rpy(obj)

def rpy2py(obj: Any) -> Sexp:
    """
    Convert R interface objects to Python objects. Supports:

    - :rcls:`SingleCellExperiment::SingleCellExperiment` → :class:`~anndata.AnnData`
    - :rcls:`S4Vectors::DataFrame` → :class:`~pandas.DataFrame`
    """
    return converter.rpy2py(obj)
