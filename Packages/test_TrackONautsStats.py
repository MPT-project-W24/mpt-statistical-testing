"""
Tests file for TrackONautsStats.py package.
"""
import unittest

import pandas as pd
import numpy as np
import scipy as sp

import TrackONautsStats

df_exp1 = pd.DataFrame([[-1,0,1],[1,0,-1],[0.5,0,0.5]], index=["A","B","C"])
df_exp2 = pd.DataFrame([[1,0,1],[-1,0,-1],[0,0,0]], index=["A","B","C"])
class TestCorrelation(unittest.TestCase):

    def test_corr_rowi_rowj_right_type(self):
        computed_correlation = df_utils.corr_rowi_rowj(df_exp1.iloc[0],df_exp1.iloc[2])
        assert isinstance(computed_correlation,float), "Computed correlation is neither int nor float, it is %s" % type(computed_correlation)

    def test_for_row_of_0(self):
        rowi = df_exp2.iloc[2]
        if rowi.all() == False:
            rowiPOP = rowi.pop(0)
            assert rowiPOP.all(), "Row is all 0, and .corr will not work"

    def test_corr_rowi_rowj_right_value(self):
        computed_correlation = df_utils.corr_rowi_rowj(df_exp2.iloc[1],df_exp2.iloc[0])
        assert 0 <= abs(computed_correlation) <= 1.00, "Something went wrong, and the correlation is outside [0,|1|]"

    def test_corr_rowi_vs_all_right_type(self):
        computed_correlation = df_utils.corr_rowi_vs_all(df_exp1.iloc[1],df_exp2)
        assert isinstance(computed_correlation, list), "Something went wrong, and the function did not return a list."

    def test_corr_rowi_vs_all_row_of_0(self):
        computed_correlation = df_utils.corr_rowi_vs_all(df_exp1.iloc[1],df_exp2)
        compPOP = computed_correlation.pop(0)
        assert compPOP.all == True, "There was a row of zeros that resulted in NaN correlation values"

    def test_corr_rowi_vs_all_work_across_df(self):
        corr1 = df_utils.corr_rowi_vs_all(df_exp1.iloc[1],df_exp2)
        corr2 = df_utils.corr_rowi_vs_all(df_exp1.iloc[1],df_exp1)
        assert type(corr1) == type(corr2), "Did not work across dataframes"

    def test_pairwise_correlation_right_type(self):
        computed_correlation = df_utils.pairwise_correlation(df_exp1)
        assert isinstance(computed_correlation, pd.DataFrame), "Something went wrong, and the function did not return a DataFrame."

    def test_pairwise_correlation_row_of_0_NA(self):
        computed_correlation = df_utils.pairwise_correlation(df_exp2)
        corrNoNA = computed_correlation.dropna()
        print(corrNoNA)
        assert corrNoNA.empty == False, "There was a row of 0, which .corr did not handle"

    def test_pairwise_correlation_right_shape(self):
        computed_correlation = df_utils.pairwise_correlation(df_exp1)
        assert computed_correlation.shape == df_exp1.shape, "Function resulted in different sized dataframe"

class TestStatistics(unittest.TestCase):

    def test_