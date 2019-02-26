#!/usr/bin/env python3
import faulthandler
from gc import collect as py_gc

from rpy2.robjects import numpy2ri, baseenv, r

faulthandler.enable()
r_gc = baseenv['gc']


def gc():
	py_gc()
	r_gc()


exprs = numpy2ri.rpy2py(r('''
data(allen, package="scRNAseq")
SummarizedExperiment::assay(allen, 1L)
''')).T
gc()
print(exprs)

