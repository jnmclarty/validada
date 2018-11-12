from .slicers import SliceStore

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
        
    kwargs = {key : value for key, value in kwargs.items() if key not in ('_raize', '_raize_kwargs')}
    
    return _raize, _raize_msg, kwargs


def _read_arg_or_kwarg(args, pos, kwargs, arg, ifnone=None):
    if arg in kwargs:
        val = kwargs[arg]
        if val is None:
            val = ifnone
    elif len(args) >= (pos + 1):
        val = args[pos]
    else:
        val = ifnone
    return val

def _read_required_arg_or_kwarg(args, pos, kwargs, arg):
    if arg in kwargs:
        val = kwargs[arg]
    elif len(args) >= (pos + 1):
        val = args[pos]
    else:
        raise Exception("Keyword argument '{}' must be defined in function".format(arg))
    return val
    
def _ret_proper_objects(_ret, ret_specd):
    ret = [ret_specd[t] for t in _ret]
    
    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)

def _make_generic_raizer(returner):
    def raizer(dforig, dfcheck, dfderive, *args, **kwargs):
        
        _raize, _raize_msg, kwargs = _pull_out_raize_kwargs(kwargs)
        
        _ret = ('bool',)
        result = returner(dforig, dfcheck, dfderive, _ret=_ret, *args, **kwargs)
        
        if not result:
            return dforig
        else:
            raise _raize(_raize_msg)
    return raizer

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
            return otherwise, args
    return otherwise, []