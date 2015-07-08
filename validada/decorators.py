# -*- coding: utf-8 -*-
from engarde.core import CheckSet

none_missing = CheckSet().decorator_maker('none_missing')
is_shape = CheckSet().decorator_maker('is_shape')
#unique_index = CheckSet().decorator_maker('unique_index')
is_monotonic = CheckSet().decorator_maker('is_monotonic')
#within_set = CheckSet().decorator_maker('within_set')
#within_range = CheckSet().decorator_maker('within_range')
#within_n_std = CheckSet().decorator_maker('within_n_std')
has_dtypes = CheckSet().decorator_maker('has_dtypes')

__all__ = [none_missing, is_monotonic] #, is_shape, none_missing, unique_index, within_n_std,
           #within_range, within_set, has_dtypes]
