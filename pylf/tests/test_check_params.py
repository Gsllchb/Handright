# coding: utf-8
from pylf import _check_params
import pytest


def test_check_text():
    with pytest.raises(TypeError):
        _check_params._check_text(1)
    with pytest.raises(TypeError):
        _check_params._check_text(None)
    with pytest.raises(TypeError):
        _check_params._check_text(list("a"))
    with pytest.raises(TypeError):
        _check_params._check_text(list("abc"))


def test_check_template2():
    with pytest.raises(TypeError):
        _check_params._check_template2([])
    # TODO


def test_check_worker():
    with pytest.raises(TypeError):
        _check_params._check_worker(1.0)
    with pytest.raises(ValueError):
        _check_params._check_worker(0)
    with pytest.raises(ValueError):
        _check_params._check_worker(-1)


def test_check_seed():
    with pytest.raises(TypeError):
        _check_params._check_worker([1, 2])
