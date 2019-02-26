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

	assay_names = se.assayNames(sce_allen)
	assays = [
		numpy2ri.rpy2py(assay).T
		for assay in (se.assay(sce_allen, str(n)) for n in assay_names)
	]
	exprs, layers = assays[0], dict(zip(assay_names[1:], assays[1:]))
	del assay_names, assays; gc()

	print(exprs)


if __name__ == '__main__':
	import faulthandler
	faulthandler.enable()
	reproduced()
