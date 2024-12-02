import pytest
import sys
import json
import os
import tempfile
from parser import ConfigParser, main

def test_is_valid_name():
    parser = ConfigParser()
    assert parser.is_valid_name("valid_name")
    assert parser.is_valid_name("a")
    assert parser.is_valid_name("a1_2_3")
    assert not parser.is_valid_name("1invalid")
    assert not parser.is_valid_name("Invalid")
    assert not parser.is_valid_name("invalid-name")

def test_parse_value():
    parser = ConfigParser()
    assert parser.parse_value(42) == "42"
    assert parser.parse_value(3.14) == "3.14"
    assert parser.parse_value("test") == '"test"'
    assert parser.parse_value(True) == "1"
    assert parser.parse_value(False) == "0"

    # Nested dictionary
    nested_dict = {"inner_key": "inner_value"}
    result = parser.parse_value(nested_dict)
    assert "$[" in result
    assert " inner_key : \"inner_value\"" in result

    with pytest.raises(ValueError):
        parser.parse_value([1, 2, 3])

def test_parse_dict():
    parser = ConfigParser()
    
    # Simple dictionary
    result = parser.parse_dict({"a": 1, "b": "test"})
    assert result.startswith("$[")
    assert result.endswith("]")
    assert " a : 1" in result
    assert ' b : "test"' in result

    # Nested dictionary
    nested_result = parser.parse_dict({
        "nested": {"inner_key": "inner_value"},
        "number": 42
    })
    assert " nested : $[" in nested_result
    assert " number : 42" in nested_result

    # Invalid key name
    with pytest.raises(ValueError):
        parser.parse_dict({"Invalid Name": 1})

def test_parse_const():
    parser = ConfigParser()
    
    # Valid constant
    result = parser.parse_const("base_value", 100)
    assert result == "const base_value = 100"
    assert parser.constants["base_value"] == 100

    # Different types of constants
    assert parser.parse_const("str_const", "test") == 'const str_const = "test"'
    assert parser.parse_const("bool_const", True) == "const bool_const = 1"

    # Invalid constant name
    with pytest.raises(ValueError):
        parser.parse_const("Invalid", 42)

def test_get_const_value():
    parser = ConfigParser()
    parser.parse_const("test_const", 42)
    assert parser.get_const_value("test_const") == "?(test_const)"

    with pytest.raises(ValueError):
        parser.get_const_value("non_existent")

def test_parse_input_full_scenarios():
    parser = ConfigParser()
    
    # Full config with constants, nested structures
    input_data = {
        "const": {
            "base_value": 100,
            "multiplier": 1.5,
            "flag": True
        },
        "config": {
            "comment": "Test configuration",
            "name": "example",
            "enabled": True,
            "nested": {
                "key": "value",
                "numbers": [1, 2, 3]
            }
        }
    }
    
    result = parser.parse_input(input_data)
    
    # Check constants
    assert "const base_value = 100" in result
    assert "const multiplier = 1.5" in result
    assert "const flag = 1" in result
    
    # Check comment
    assert "/*\nTest configuration\n*/" in result
    
    # Check config
    assert '$[ name : "example"' in result
    assert "enabled : 1" in result

def test_parse_input_error_cases():
    parser = ConfigParser()
    
    # Non-dictionary input
    with pytest.raises(ValueError, match="Ожидался JSON объект"):
        parser.parse_input([1, 2, 3])
    
    # Invalid const type
    with pytest.raises(ValueError, match="Поле 'const' должно быть словарем"):
        parser.parse_input({"const": 42})

def test_main_functionality():
    # Create temporary input and output files
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as input_file, \
         tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as output_file:
        
        # Prepare input JSON
        input_data = {
            "const": {"test_const": 100},
            "config": {"name": "test_config"}
        }
        json.dump(input_data, input_file)
        input_file.close()
        output_file.close()

        # Modify sys.argv to simulate command-line arguments
        original_argv = sys.argv
        sys.argv = ['parser.py', input_file.name, output_file.name]

        try:
            # Run main function
            main()

            # Check output file
            with open(output_file.name, 'r') as f:
                result = f.read()
                assert "const test_const = 100" in result
                assert '$[ name : "test_config"' in result
        
        finally:
            # Clean up
            os.unlink(input_file.name)
            os.unlink(output_file.name)
            sys.argv = original_argv

def test_error_handling():
    # Invalid JSON file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as invalid_file, \
         tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as output_file:
        
        invalid_file.write("{invalid json}")
        invalid_file.close()
        output_file.close()

        # Modify sys.argv
        original_argv = sys.argv
        sys.argv = ['parser.py', invalid_file.name, output_file.name]

        # Capture stderr
        try:
            from io import StringIO
            import sys

            # Redirect stderr
            old_stderr = sys.stderr
            sys.stderr = captured_output = StringIO()

            # Try to run main (should exit)
            with pytest.raises(SystemExit):
                main()

            # Check error message
            assert "Ошибка JSON" in captured_output.getvalue()
        
        finally:
            # Restore stderr and clean up files
            sys.stderr = old_stderr
            os.unlink(invalid_file.name)
            os.unlink(output_file.name)
            sys.argv = original_argv