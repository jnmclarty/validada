
from slicers import ix, SliceStore
from functools import wraps
from copy import copy

def _pull_out_ret(kwargs, dforig):
    try:
        _ret = kwargs['_ret']
    except KeyError:
        raise KeyError("_ret must be defined")
    
    if not isinstance(_ret, (list, tuple)):
        _ret = (_ret,)
    ret_specd = {'orig' : dforig, 'bool' : None, 'ndframe' : None, 'obj' : None}
    return _ret, ret_specd

def _pull_out_raize_kwargs(kwargs):
    try:
        _raize = kwargs['_raize']
        _raize_msg = kwargs['_raize_msg']
    except KeyError:
        raise KeyError("_raize and _raize_msg must be defined")
        
    kwargs = {key : value for key, value in kwargs.iteritems() if key not in ('_raize', '_raize_kwargs')}
    
    return _raize, _raize_msg, kwargs


def _read_opt_kwarg(kwargs, arg, ifnone):
    if arg in kwargs:
        val = kwargs[arg]
        if val is None:
            val = ifnone
    else:
        val = ifnone
    return val

def _ret_proper_objects(_ret, ret_specd):
    ret = [ret_specd[t] for t in _ret]
    
    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)    
def _none_missing_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _ret, ret_specd = _pull_out_ret(kwargs, dforig)

    columns = _read_opt_kwarg(kwargs, 'columns', dfcheck.columns)
    
    ret_specd['obj'] = dfcheck[columns].isnull()
    ret_specd['ndframe'] = ret_specd['obj'].any()
    ret_specd['bool'] = ret_specd['ndframe'].any()
    
    return _ret_proper_objects(_ret, ret_specd)

def _none_missing_raize(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _raize, _raize_msg, kwargs = _pull_out_raize_kwargs(kwargs)
    
    _ret = ('bool',)
    result = _none_missing_ret(dforig, dfcheck, dfderive, _ret=_ret, *args, **kwargs)
    
    if not result:
        return dforig
    else:
        raise _raize(_raize_msg)  


def _is_monotonic_ret(dforig, dfcheck, dfderive, *args, **kwargs):

    _ret, ret_specd = _pull_out_ret(kwargs, dforig)
    
    increasing = _read_opt_kwarg(kwargs, 'increasing', None)
    strict = _read_opt_kwarg(kwargs, 'strict', False)
    items = _read_opt_kwarg(kwargs, 'items', {k: (increasing, strict) for k in dfcheck})
    
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
    ret_specd['bool'] = list(results.values()).any()
    
    return _ret_proper_objects(_ret, ret_specd)

def _is_monotonic_raize(dforig, dfcheck, dfderive, *args, **kwargs):
    
    _raize, _raize_msg, kwargs = _pull_out_raize_kwargs(kwargs)
    
    _ret = ('bool',)
    result = _is_monotonic_ret(dforig, dfcheck, dfderive, _ret=_ret, *args, **kwargs)
    
    if not result:
        return dforig
    else:
        raise _raize(_raize_msg)  
        
def _acheck_ret(dforig, dfcheck, dfderive, *args, **kwargs):
    
    try:
        _ret = kwargs['_ret']
    except KeyError:
        raise KeyError("_ret must be defined")
    
    if not isinstance(_ret, (list, tuple)):
        _ret = (_ret,)
    
    ret_specd = {'orig' : None, 'bool' : None, 'ndframe' : None, 'obj' : None}
    
    #dologicchecklogic, calculating as necessary...populating the 
    # above appropriate keys as necessary
    
    ret = [ret_specd[t] for t in _ret]
    return ret

def _acheck_raize(dforig, dfcheck, dfderive, *args, **kwargs):
    
    try:
        _raize = kwargs['_raize']
        _raize_kwargs = kwargs['_raize_kwargs']
    except KeyError:
        raise KeyError("_raize and _raize_kwargs must be defined")
    kwargs = {key : value for key, value in kwargs.iteritems() if key not in ('_raize', '_raize_kwargs')}

    #dologicchecklogic, raising when necessary...
    # or...to not duplicate code:

    _ret = ('bool',)
    result = _acheck_ret(dforig, dfcheck, dfderive, _ret=_ret, *args, **kwargs)
    
    if result:
        return dforig
    else:
        _raize(**_raize_kwargs)  

def _generic_check_maker(returner, raizer):
    def check(self, df, *args, **kwargs):
        
        slc, args = _lop_off_head_if_slice(args, self.check_slc)
        slcd, args = _lop_off_head_if_slice(args, self.derive_slc)    
        
        dfc = getattr(df, slc.mode)[slc.slc]
        dfd = getattr(df, slcd.mode)[slcd.slc]
        
        if self.raize is not None:
            result = raizer(df, dfc, dfd, 
                                   *args, _raize=self.raize, 
                                   _raize_msg=self.raize_msg, **kwargs)
        elif self.ret is not None:
            result = returner(df, dfc, dfd, *args, _ret=self.ret, **kwargs)
        else:
            raise Exception("Can't read your mind")
        return result
    return check
        
def _lop_off_head_if_slice(args, otherwise):
    if len(args) >= 1:
        if isinstance(args[0], (slice, SliceStore)):
            if len(args) >= 2:
                return args[0], args[1:]
            else:
                return args[0], []
    else:
        return otherwise, []
                    
class CheckSet(object):
    def __init__(self, ret=None, raize=None, msg=""):
        
        self.check_slc = copy(ix)
        self.derive_slc = copy(ix)
        
        self.ret = ret or ('ndframe', 'bool', 'obj')
        self.raize = raize or AssertionError
        self.raize_msg = msg
    
    acheck = _generic_check_maker(_acheck_ret, _acheck_raize)
 
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
    
    def decorator_maker(self, name, *args, **kwargs):
        def adecorator(*args, **kwargs):
            def decorate(func):
                @wraps(func)
                def wrapper(*wargs, **wkwargs):
                    result = func(*wargs, **wkwargs)
                    ans = getattr(self, name)(result, *args, **kwargs)
                    if ans:
                        result = [result] + list(ans)
                        result = tuple(result)
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
    import pandas as pd
    df = pd.DataFrame(data=[1,2,3,4])
    
    acheck = CheckSet().acheck
    acheck_dec = CheckSet().decorator_maker('acheck')

    acheck(df)
    
    @acheck_dec
    def myfunc(df):
        return df + 1.0
