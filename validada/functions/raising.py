# -*- coding: utf-8 -*-
from validada.core import RaiseSet

none_missing = RaiseSet().none_missing
is_monotonic = RaiseSet().is_monotonic
is_shape = RaiseSet().is_shape
unique_index = RaiseSet().unique_index
within_set = RaiseSet().within_set
within_range = RaiseSet().within_range
within_n_std = RaiseSet().within_n_std
has_dtypes = RaiseSet().has_dtypes
equal_columns_sum = RaiseSet().equal_columns_sum
has_in_index = RaiseSet().has_in_index

__all__ = [is_monotonic, is_shape, none_missing, unique_index, within_n_std,
           within_range, within_set, has_dtypes, equal_columns_sum, has_in_index]

