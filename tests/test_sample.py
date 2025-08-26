"""Tests for the sample Python module."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from src.python_placeholder import SampleClass, sample_function


def test_sample_function():
    """Test the sample function."""
    result = sample_function()
    assert result == "Hello from Python!"
    assert isinstance(result, str)


class TestSampleClass:
    """Test cases for SampleClass."""

    def test_init_default(self):
        """Test initialization with default value."""
        obj = SampleClass()
        assert obj.value is None

    def test_init_with_value(self):
        """Test initialization with a value."""
        obj = SampleClass("test")
        assert obj.value == "test"

    def test_get_value(self):
        """Test getting the value."""
        obj = SampleClass("test_value")
        assert obj.get_value() == "test_value"

    def test_set_value(self):
        """Test setting the value."""
        obj = SampleClass()
        result = obj.set_value("new_value")
        assert obj.value == "new_value"
        assert result is obj  # Should return self

    def test_set_value_chaining(self):
        """Test method chaining with set_value."""
        obj = SampleClass()
        final_obj = obj.set_value("chain_test")
        assert final_obj.get_value() == "chain_test"
