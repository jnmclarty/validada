# -*- coding: utf-8 -*-
"""
checks.py

Each function in here should

- Take a DataFrame as its first argument, maybe optional arguments
- Makes its assert on the result
- Return the original DataFrame
"""
import numpy as np
import pandas as pd
from copy import copy

from core import CheckSet

none_missing = CheckSet().none_missing
is_monotonic = CheckSet().is_monotonic
is_shape = CheckSet().is_shape
unique_index = CheckSet().unique_index
within_set = CheckSet().within_set



class ResetSlice(object):
    pass

Reset = ResetSlice()

def within_range(df, items=None):
    """
    Assert that a DataFrame is within a range.

    Parameters
    ==========
    df : DataFame
    items : dict
        mapping of columns (k) to a (low, high) tuple (v)
        that ``df[k]`` is expected to be between.
    """
    for k, (lower, upper) in items.items():
        if (lower > df[k]).any() or (upper < df[k]).any():
            raise AssertionError
    return df
        
class SlicedChecks(object):
    def __init__(self, sl=None, post_check_reset=False):
        self.pcr = post_check_reset
        self.sl = sl or slice(None)
    def __getitem__(self, sl):
        if isinstance(sl, ResetSlice):
            self.sl = slice(None)
        else:
            self.sl = sl
        return self 
    def within_range(self, df, items=None):        
        slc = copy(self.sl)
        if self.pcr:
            self.sl = slice(None)
        try:
            within_range(df.iloc[slc], items)
        except:
            raise AssertionError
        return df


sc = SlicedChecks()
scr = SlicedChecks(post_check_reset=True)

def within_n_std(df, sl=None, n=3):
    """
    TODO: Check broadcasting post-.iloc
    """
    slc = sl or slice(None)
    means = df.mean()
    stds = df.std()
    if not (np.abs(df.iloc[slc] - means) < n * stds).all().all():
        raise AssertionError
    return df

def has_dtypes(df, items):
    """
    Assert that a DataFrame has `dtypes`

    Parameters
    ==========
    df: DataFrame
    items: dict
        mapping of columns to dtype.
    """
    dtypes = df.dtypes
    for k, v in items.items():
        if not dtypes[k] == v:
            raise AssertionError
    return df

__all__ = [is_monotonic, is_shape, none_missing, unique_index, within_n_std,
           sc.within_range, within_set, has_dtypes]

