#!/usr/bin/env python3
from gc import collect as py_gc
from rpy2.robjects import baseenv

r_gc = baseenv['gc']
del baseenv


def gc():
	py_gc()
	r_gc()


def with_converter():
	import scanpy as sc
	from rpy2.robjects import r, globalenv, default_converter
	import anndata2ri
	from rpy2.robjects.conversion import localconverter

	with localconverter(default_converter + anndata2ri.converter):
		adata_paul = sc.datasets.paul15()
		globalenv['sce_paul'] = adata_paul
		r('print(sce_paul); NULL')

		adata_allen = r('''
		suppressPackageStartupMessages(library(SingleCellExperiment))
		data(allen, package="scRNAseq")
		as(allen, 'SingleCellExperiment')
		''')
		print(adata_allen)


def manual():
	import scanpy as sc
	from rpy2.robjects import r, globalenv
	import anndata2ri

	adata_paul = sc.datasets.paul15()
	globalenv['sce_paul'] = anndata2ri.py2rpy(adata_paul)
	r('print(sce_paul); NULL')

	sce_allen = r('''
	suppressPackageStartupMessages(library(SingleCellExperiment))
	data(allen, package="scRNAseq")
	as(allen, 'SingleCellExperiment')
	''')
	adata_allen = anndata2ri.rpy2py(sce_allen)
	print(adata_allen)


def reproduced():
	def paul():
		import scanpy as sc
		from rpy2.robjects import numpy2ri, pandas2ri, globalenv, r
		from rpy2.robjects.packages import importr
		from rpy2.robjects.vectors import ListVector

		s4v = importr("S4Vectors")
		sce = importr("SingleCellExperiment")

		adata_paul = sc.datasets.paul15()

		layers = {k: numpy2ri.py2rpy(v.T) for k, v in adata_paul.layers.items()}
		assays = ListVector({"X": numpy2ri.py2rpy(adata_paul.X.T), **layers})
		del layers; gc()

		row_args = {k: pandas2ri.py2rpy(v) for k, v in adata_paul.var.items()}
		row_args["row.names"] = pandas2ri.py2rpy(adata_paul.var_names)
		col_args = {k: pandas2ri.py2rpy(v) for k, v in adata_paul.obs.items()}
		col_args["row.names"] = pandas2ri.py2rpy(adata_paul.obs_names)

		row_data = s4v.DataFrame(**row_args)
		col_data = s4v.DataFrame(**col_args)
		del s4v, row_args, col_args; gc()
		metadata = ListVector({k: numpy2ri.py2rpy(v) for k, v in adata_paul.uns.items()})
		del adata_paul; gc()

		sce_paul = sce.SingleCellExperiment(assays=assays, rowData=row_data, colData=col_data, metadata=metadata)
		del sce, assays, row_data, col_data, metadata; gc()
		globalenv['sce_paul'] = sce_paul

		r('print(sce_paul); NULL')
		r('sce_paul')

	# dir 2

	def rpy2py_data_frame(obj):
		import pandas as pd
		from rpy2.rinterface import NULLType
		from rpy2.robjects.robject import RSlots

		slots = RSlots(obj)
		columns = dict(slots["listData"].items())
		rownames = slots["rownames"]
		if isinstance(rownames, NULLType):
			rownames = pd.RangeIndex(slots["nrows"][0])
		del slots; gc()

		df = pd.DataFrame(columns, index=rownames)
		del columns, rownames; gc()
		return df

	def allen():
		from anndata import AnnData
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

		obs = rpy2py_data_frame(se.colData(sce_allen))
		var = rpy2py_data_frame(se.rowData(sce_allen))
		del se, sce_allen; gc()

		print(exprs)
		adata_allen = AnnData(exprs, obs, var, layers=layers)
		del exprs, obs, var, layers; gc()
		print(adata_allen)

	paul()
	allen()


if __name__ == '__main__':
	import faulthandler
	faulthandler.enable()
	reproduced()
