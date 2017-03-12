from __future__ import absolute_import, division, print_function, unicode_literals

try:
    import pyros_msgs
    import genpy
except ImportError:
    import pyros_setup
    pyros_setup.configurable_import().configure().activate()
    import pyros_msgs
    import genpy

import six

from pyros_msgs.common.typechecker import (
    six_long,
    maybe_list,
    maybe_tuple,
    Sanitizer, Accepter, Array, Any, MinMax,
    TypeChecker,
    TypeCheckerException,
)

import sys
import math
import numpy  # only for nextafter
import pytest
from hypothesis import given, example, assume, settings, Verbosity, HealthCheck
import hypothesis.strategies as st

from . import float_type_checker, float_type_checker_min_max, proper_basic_strategy_selector, bad_basic_strategy_selector


@given(proper_basic_strategy_selector(float_type_checker))  # where we learn that in python
@settings(verbosity=Verbosity.verbose, timeout=1, suppress_health_check=[HealthCheck.too_slow])
def test_typechecker_maintains_equality(value):
    """
    Verify that value is accepted and the sanitized value is "equal" to original value
    This means that sanitization conserve value equality, in the python sense.
    """
    assume(not math.isnan(value) and not math.isinf(value))  # because equality doesnt hold for inf and nan
    assert float_type_checker(value) == value


@given(bad_basic_strategy_selector(float_type_checker))
@settings(verbosity=Verbosity.verbose, timeout=1, suppress_health_check=[HealthCheck.too_slow])
def test_typechecker_breaks_on_bad_values(value):
    """
    Verify that value is not accepted
    """
    with pytest.raises(TypeCheckerException) as excinfo:
        float_type_checker(value)
    assert "is not accepted by Accepter from <type 'float'>" in excinfo.value.message


@given(proper_basic_strategy_selector(float_type_checker_min_max))
@settings(verbosity=Verbosity.verbose, timeout=1, suppress_health_check=[HealthCheck.too_slow])
def test_typechecker_with_minmax_accepter_maintains_equality(value):
    """
    Verify that value is accepted and the sanitized value is "equal" to original value
    This means that sanitization conserve value equality, in the python sense.
    """
    assert float_type_checker_min_max(value) == value


@given(bad_basic_strategy_selector(float_type_checker_min_max))
@settings(verbosity=Verbosity.verbose, timeout=1, suppress_health_check=[HealthCheck.too_slow])
def test_typechecker_with_minmax_accepter_breaks_on_bad_nonfloat_values(value):
    """
    Verify that value is not accepted
    """
    with pytest.raises(TypeCheckerException) as excinfo:
        float_type_checker_min_max(value)
    assert "is not accepted by MinMax [-42.0..1.38350580553e+19] of Accepter from <type 'float'>" in excinfo.value.message


# Separate test because of float arithemtics...
# TODO FIXME
@given(bad_basic_strategy_selector(float_type_checker_min_max))
@settings(verbosity=Verbosity.verbose, timeout=1, suppress_health_check=[HealthCheck.too_slow])
def test_typechecker_with_minmax_accepter_breaks_on_bad_float_values(value):
    """
    Verify that value is not accepted
    """
    with pytest.raises(TypeCheckerException) as excinfo:
        float_type_checker_min_max(value)
    assert "is not accepted by MinMax [-42.0..1.38350580553e+19] of Accepter from <type 'float'>" in excinfo.value.message