# -*- coding: utf-8 -*-

from validada.core import ReturnSet

none_missing = ReturnSet().none_missing
is_monotonic = ReturnSet().is_monotonic
is_shape = ReturnSet().is_shape
unique_index = ReturnSet().unique_index
within_set = ReturnSet().within_set
within_range = ReturnSet().within_range
within_n_std = ReturnSet().within_n_std
has_dtypes = ReturnSet().has_dtypes
equal_columns_sum = ReturnSet().equal_columns_sum
has_in_index = ReturnSet().has_in_index

__all__ = [is_monotonic, is_shape, none_missing, unique_index, within_n_std,
           within_range, within_set, has_dtypes, equal_columns_sum, has_in_index]

