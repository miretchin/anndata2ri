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

	exprs = numpy2ri.rpy2py(r('''
	data(allen, package="scRNAseq")
	SummarizedExperiment::assay(allen, 1L)
	''')).T
	gc()
	print(exprs)


if __name__ == '__main__':
	import faulthandler
	faulthandler.enable()
	reproduced()
