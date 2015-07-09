# -*- coding: utf-8 -*-
from validada.core import ReturnSet

none_missing = ReturnSet().decorator_maker('none_missing')
is_shape = ReturnSet().decorator_maker('is_shape')
unique_index = ReturnSet().decorator_maker('unique_index')
is_monotonic = ReturnSet().decorator_maker('is_monotonic')
within_set = ReturnSet().decorator_maker('within_set')
within_range = ReturnSet().decorator_maker('within_range')
within_n_std = ReturnSet().decorator_maker('within_n_std')
has_dtypes = ReturnSet().decorator_maker('has_dtypes')
equal_columns_sum = ReturnSet().decorator_maker('equal_columns_sum')
has_in_index = ReturnSet().decorator_maker('has_in_index')

__all__ = [none_missing, is_monotonic, is_shape, none_missing, unique_index,
           within_n_std, has_dtypes, equal_columns_sum, has_in_index]
