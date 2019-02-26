#!/usr/bin/env python3
import gc
import faulthandler

from rpy2.robjects import numpy2ri, baseenv, r


# SEGFAULT tracebacks are a godsend.
faulthandler.enable()

# Convert an R matrix to a numpy array
# without keeping a reference on the R side.
# It needs to be either big enough or data-backed(?)
exprs = numpy2ri.rpy2py(r('''
data(allen, package="scRNAseq")
SummarizedExperiment::assay(allen, 1L)
'''))

# Garbage collect in Python and R.
gc.collect()
baseenv['gc']()

# SEGFAULT when interacting with the numpy array.
print(exprs)
