
import pandas as pd

import datetime as dt

from slicers import ix
from functools import wraps
from copy import copy
from collections import Counter

from convenience import _pull_out_ret, _pull_out_raize_kwargs, \
                        _read_arg_or_kwarg, _read_required_arg_or_kwarg, \
                        _ret_proper_objects, _make_generic_raizer, \
                        _generic_check_maker, _lop_off_head_if_slice

def _has_in_index_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _ret, ret_specd = _pull_out_ret(kwargs, dforig)

    orig_obj_to_check = _read_required_arg_or_kwarg(args, 0, kwargs, 'obj')
    obj_to_check = orig_obj_to_check

    try_ix = _read_arg_or_kwarg(args, 1, kwargs, 'try_ix', False)
    try_strftime = _read_arg_or_kwarg(args, 2, kwargs, 'try_strftime', False)
    check_na = _read_arg_or_kwarg(args, 3, kwargs, 'check_na', False)
    
    
    
    ans = obj_to_check in dfcheck.index
    
    if try_strftime:
        try:
            obj_to_check = obj_to_check.strftime(try_strftime)
        except:
            pass
    
    # at this point, if it's in the index, ans will be True
        
    if try_ix:
        try:
            ans = ans or (len(dfcheck.ix[obj_to_check]) > 0)
        except:
            pass

    # at this point, if it's in the index, or if it's string representation
    # is in the index, ans will be True

    if check_na:
        try:
            isna = dfcheck.ix[obj_to_check].isnull()[0]
        except:
            isna = True
        ans = not ((not ans) or isna)
        
    results = {orig_obj_to_check : ans}
    ret_specd['obj'] = results
    ret_specd['ndframe'] = pd.Series(results)
    ret_specd['bool'] = not ans
    
    return _ret_proper_objects(_ret, ret_specd)
_has_in_index_raize = _make_generic_raizer(_has_in_index_ret)

def _equal_columns_sum_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _ret, ret_specd = _pull_out_ret(kwargs, dforig)

    cola = _read_arg_or_kwarg(args, 0, kwargs, 'cola', dfcheck.columns[0])
    colb = _read_arg_or_kwarg(args, 1, kwargs, 'colb', dfcheck.columns[1])
    
    results = {cola : dfcheck[cola].dropna().sum(),
               colb : dfcheck[colb].dropna().sum()}

    ret_specd['obj'] = results
    ret_specd['ndframe'] = pd.Series(results)
    ret_specd['bool'] = not results[cola] == results[colb]
    
    return _ret_proper_objects(_ret, ret_specd)
_equal_columns_sum_raize = _make_generic_raizer(_equal_columns_sum_ret)

def _none_missing_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _ret, ret_specd = _pull_out_ret(kwargs, dforig)

    columns = _read_arg_or_kwarg(args, 0, kwargs, 'columns', dfcheck.columns)
    
    ret_specd['obj'] = dfcheck[columns].isnull()
    ret_specd['ndframe'] = ret_specd['obj'].any()
    ret_specd['bool'] = ret_specd['ndframe'].any()
    
    return _ret_proper_objects(_ret, ret_specd)
_none_missing_raize = _make_generic_raizer(_none_missing_ret)

def _is_shape_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _ret, ret_specd = _pull_out_ret(kwargs, dforig)

    shape = _read_required_arg_or_kwarg(args, 0, kwargs, 'shape')
    
    ret_specd['obj'] = "is_shape has no output object"
    ret_specd['ndframe'] = "is_shape has no output ndframe"
    ret_specd['bool'] = not dfcheck.shape == shape
    
    return _ret_proper_objects(_ret, ret_specd)   
_is_shape_raize = _make_generic_raizer(_is_shape_ret)

def _unique_index_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _ret, ret_specd = _pull_out_ret(kwargs, dforig)

    ret_specd['obj'] = Counter(list(dfcheck.index))
    ret_specd['ndframe'] = pd.Series(ret_specd['obj'])
    ret_specd['bool'] = not dfcheck.index.is_unique
    
    return _ret_proper_objects(_ret, ret_specd)   
_unique_index_raize = _make_generic_raizer(_unique_index_ret)

def _is_monotonic_ret(dforig, dfcheck, dfderive, *args, **kwargs):

    _ret, ret_specd = _pull_out_ret(kwargs, dforig)
    
    increasing = _read_arg_or_kwarg(args, 0, kwargs, 'increasing', None)
    strict = _read_arg_or_kwarg(args, 1, kwargs, 'strict', False)
    items = _read_arg_or_kwarg(args, 2, kwargs, 'items', {k: (increasing, strict) for k in dfcheck})
    
    results = {}
    for col, (increasing, strict) in items.items():
        s = pd.Index(dfcheck[col])
        if increasing:
            good = getattr(s, 'is_monotonic_increasing')
        elif increasing is None:
            good = getattr(s, 'is_monotonic') | getattr(s, 'is_monotonic_decreasing')
        else:
            good = getattr(s, 'is_monotonic_decreasing')
        if strict:
            if increasing:
                good = good & (s.to_series().diff().dropna() > 0).all()
            elif increasing is None:
                good = good & ((s.to_series().diff().dropna() > 0).all() |
                               (s.to_series().diff().dropna() < 0).all())
            else:
                good = good & (s.to_series().diff().dropna() < 0).all()
        results[col] = not good
            
    ret_specd['obj'] = results
    ret_specd['ndframe'] = pd.Series(results)
    ret_specd['bool'] = any(list(results.values()))
    
    return _ret_proper_objects(_ret, ret_specd)
_is_monotonic_raize = _make_generic_raizer(_is_monotonic_ret)

def _within_set_ret(dforig, dfcheck, dfderive, *args, **kwargs):

    _ret, ret_specd = _pull_out_ret(kwargs, dforig)
    
    items = _read_required_arg_or_kwarg(args, 0, kwargs, 'items')
    
    results = {}
    for k, v in items.items():
        results[k] = not dfcheck[k].isin(v).all()
            
    ret_specd['obj'] = results
    ret_specd['ndframe'] = pd.Series(results)
    ret_specd['bool'] = any(list(results.values()))
    
    return _ret_proper_objects(_ret, ret_specd)
_within_set_raize = _make_generic_raizer(_within_set_ret)

def _within_range_ret(dforig, dfcheck, dfderive, *args, **kwargs):

    _ret, ret_specd = _pull_out_ret(kwargs, dforig)
    
    items = _read_required_arg_or_kwarg(args, 0, kwargs, 'items')
    
    results = {}
    for k, (lower, upper) in items.items():
        results[k] = (lower > dfcheck[k]).any() or (upper < dfcheck[k]).any()

    ret_specd['obj'] = results
    ret_specd['ndframe'] = pd.Series(results)
    ret_specd['bool'] = any(list(results.values()))
    
    return _ret_proper_objects(_ret, ret_specd)
_within_range_raize = _make_generic_raizer(_within_range_ret)

def _within_n_std_ret(dforig, dfcheck, dfderive, *args, **kwargs):

    _ret, ret_specd = _pull_out_ret(kwargs, dforig)
    
    n = _read_arg_or_kwarg(args, 0, kwargs, 'n', 3)

    means = dfderive.mean()
    stds = dfderive.std()
    
    results = (pd.np.abs(dfcheck - means) < n * stds)
    
    ret_specd['obj'] = results
    ret_specd['ndframe'] = results
    ret_specd['bool'] = not results.all().all()
    
    return _ret_proper_objects(_ret, ret_specd)
_within_n_std_raize = _make_generic_raizer(_within_n_std_ret)


def _has_dtypes_ret(dforig, dfcheck, dfderive, *args, **kwargs):

    _ret, ret_specd = _pull_out_ret(kwargs, dforig)
    
    items = _read_required_arg_or_kwarg(args, 0, kwargs, 'items')
    
    results = {}    
    dtypes = dfcheck.dtypes
    for k, v in items.items():
        results[k] = not dtypes[k] == v

    ret_specd['obj'] = results
    ret_specd['ndframe'] = pd.Series(results)
    ret_specd['bool'] = any(list(results.values()))
    return _ret_proper_objects(_ret, ret_specd)
    
_has_dtypes_raize = _make_generic_raizer(_has_dtypes_ret)
    
class CheckSet(object):
    def __init__(self, ret=None, raize=None, msg=""):
        
        self.check_slc = copy(ix)
        self.derive_slc = copy(ix)
        
        self.ret = ret or ('ndframe', 'bool', 'obj')
        self.raize = raize or AssertionError
        self.raize_msg = msg

    none_missing = _generic_check_maker(_none_missing_ret, _none_missing_raize)
    none_missing.__doc__ = """
        Asserts that there are no missing values (NaNs) in the DataFrame.
        Parameters
        ==========
        df : Series or DataFrame    
        columns : list of column names
        """
    
    is_monotonic = _generic_check_maker(_is_monotonic_ret, _is_monotonic_raize)
    is_monotonic.__doc__ =     """
        Asserts that the DataFrame is monotonic
    
        Parameters
        ==========
        df : Series or DataFrame
        items : dict
            mapping columns to conditions (increasing, strict)
        increasing : None or bool
            None is either increasing or decreasing.
        strict: whether the comparison should be strict
        """

    is_shape = _generic_check_maker(_is_shape_ret, _is_shape_raize)
    is_shape.__doc__ = """
    Asserts that the DataFrame is of a known shape.

    Parameters
    ==========

    df: DataFrame
    shape : tuple (n_rows, n_columns)
    """
    
    unique_index = _generic_check_maker(_unique_index_ret, _unique_index_raize)
    unique_index.__doc__ = """Assert that the index is unique"""
    
    within_set = _generic_check_maker(_within_set_ret, _within_set_raize)
    within_set.__doc__ = """
    Assert that df is a subset of items

    Parameters
    ==========

    df : DataFrame
    items : dict
        mapping of columns (k) to array-like of values (v) that
        ``df[k]`` is expected to be a subset of
    """
    
    within_range = _generic_check_maker(_within_range_ret, _within_range_raize)
    within_range.__doc__ = """
    Assert that a DataFrame is within a range.

    Parameters
    ==========
    df : DataFame
    items : dict
        mapping of columns (k) to a (low, high) tuple (v)
        that ``df[k]`` is expected to be between.
    """
    
    within_n_std = _generic_check_maker(_within_n_std_ret, _within_n_std_raize)
    within_n_std.__doc__ = """
    Assert that a DataFrame is within a range.

    Parameters
    ==========
    df : DataFame
    n : float
        Number of standard deviations the columns should be within.
    """
    
    has_dtypes = _generic_check_maker(_has_dtypes_ret, _has_dtypes_raize)
    has_dtypes.__doc__ = """
    Assert that a DataFrame has `dtypes`

    Parameters
    ==========
    df: DataFrame
    items: dict
        mapping of columns to dtype.
    """
    
    equal_columns_sum = _generic_check_maker(_equal_columns_sum_ret, 
                                             _equal_columns_sum_raize)
    equal_columns_sum.__doc__ = """
    Assert that the sume of two columns are equal

    Parameters
    ==========
    df: DataFrame
    cola: str
        column one
    colb: str
        column two
    """
    
    has_in_index = _generic_check_maker(_has_in_index_ret, 
                                        _has_in_index_raize)
    has_in_index.__doc__ = """
    Assert that the sume of two columns are equal

    Parameters
    ==========
    df: DataFrame
    obj: obj
        Any hashable object that would be in an index
    try_ix: boolean, default to False
        will apply an additional check to see if the object can be converted
        using ix's logic.
    try_strftime: str or boolean, defaults to False
        If set to a string, it will be used to attempt obj.strftime(try_strftime)
        If set to True, it will be used to attempt obj.strftime('%Y-%m-%d')
        Does nothing if try_ix is False
    """
    
    def decorator_maker(self, name, *args, **kwargs):
        def adecorator(*args, **kwargs):
            def decorate(func):
                @wraps(func)
                def wrapper(*wargs, **wkwargs):
                    result = func(*wargs, **wkwargs)
                    ans = getattr(self, name)(result, *args, **kwargs)
                    result = (result, ans)
                    return result
                return wrapper
            return decorate
        return adecorator
        
class ReturnSet(CheckSet):
    def __init__(self, ret=None):
        
        self.check_slc = copy(ix)
        self.derive_slc = copy(ix)
        
        self.ret = ret or ('orig','bool','ndframe','obj')
        self.raize = None
        self.raize_msg = None


class RaiseSet(CheckSet):
    def __init__(self, raize=None, msg=""):
        
        self.check_slc = copy(ix)
        self.derive_slc = copy(ix)
        
        self.ret = ('orig',)
        self.raize = raize or AssertionError
        self.raize_msg = msg
        
if __name__ == '__main__':

    df = pd.DataFrame(data={'A' : [1,2,3,4], 'B' : [1,2,3,5]})
    
    rs = ReturnSet(('bool','obj'))
    eqs = rs.equal_columns_sum
    print eqs(df)
    
    print "*" * 10

    eqs_dec = rs.decorator_maker('equal_columns_sum')
#    
    @eqs_dec()
    def myfunc(adf):
        return adf + 1.0
    
    print myfunc(df)
