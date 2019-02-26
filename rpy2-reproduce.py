#!/usr/bin/env python3
from gc import collect as py_gc
from rpy2.robjects import baseenv

r_gc = baseenv['gc']
del baseenv


def gc():
	py_gc()
	r_gc()


def reproduced():
	from rpy2.robjects import numpy2ri, r
	from rpy2.robjects.packages import importr

	se = importr("SummarizedExperiment")

	sce_allen = r('''
	suppressPackageStartupMessages(library(SingleCellExperiment))
	data(allen, package="scRNAseq")
	as(allen, 'SingleCellExperiment')
	''')

	exprs = numpy2ri.rpy2py(se.assay(sce_allen, 1)).T
	gc()
	print(exprs)


if __name__ == '__main__':
	import faulthandler
	faulthandler.enable()
	reproduced()
