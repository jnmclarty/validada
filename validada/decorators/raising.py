# -*- coding: utf-8 -*-
from validada.core import RaiseSet

none_missing = RaiseSet().decorator_maker('none_missing')
is_shape = RaiseSet().decorator_maker('is_shape')
unique_index = RaiseSet().decorator_maker('unique_index')
is_monotonic = RaiseSet().decorator_maker('is_monotonic')
within_set = RaiseSet().decorator_maker('within_set')
within_range = RaiseSet().decorator_maker('within_range')
within_n_std = RaiseSet().decorator_maker('within_n_std')
has_dtypes = RaiseSet().decorator_maker('has_dtypes')
equal_columns_sum = RaiseSet().decorator_maker('equal_columns_sum')
has_in_index = RaiseSet().decorator_maker('has_in_index')

__all__ = [none_missing, is_monotonic, is_shape, none_missing, unique_index,
           within_n_std, has_dtypes, equal_columns_sum, has_in_index]
