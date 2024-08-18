import pytest
import sys
import os
import json
from unittest.mock import mock_open, patch

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "sol_one"))
)
from fixed_width_generator import FixedWidthGenerator
from csv_generator import DelimitedParser
from spec import Spec
from main import FileProcessorFactory


# Spec Tests
def test_spec_initialization():
    spec_data = {
        "ColumnNames": ["Name", "Age", "City"],
        "Offsets": ["10", "3", "15"],
        "FixedWidthEncoding": "utf-8",
        "DelimitedEncoding": "utf-8",
        "IncludeHeader": "True",
    }
    spec = Spec(spec_data)
    assert spec.column_names == ["Name", "Age", "City"]
    assert spec.offsets == [10, 3, 15]
    assert spec.fixed_width_encoding == "utf-8"
    assert spec.delimited_encoding == "utf-8"
    assert spec.include_header == True


def test_spec_from_json():
    json_content = json.dumps(
        {
            "ColumnNames": ["Name", "Age", "City"],
            "Offsets": ["10", "3", "15"],
            "FixedWidthEncoding": "utf-8",
            "DelimitedEncoding": "utf-8",
            "IncludeHeader": "True",
        }
    )
    with patch("builtins.open", mock_open(read_data=json_content)):
        spec = Spec.from_json("dummy.json")
        assert spec.column_names == ["Name", "Age", "City"]
        assert spec.offsets == [10, 3, 15]
        assert spec.fixed_width_encoding == "utf-8"
        assert spec.delimited_encoding == "utf-8"
        assert spec.include_header == True


# FixedWidthGenerator Tests
@pytest.fixture
def fixed_width_generator():
    return FixedWidthGenerator()


@pytest.fixture
def sample_spec():
    return Spec(
        {
            "ColumnNames": ["Name", "Age", "City"],
            "Offsets": ["10", "3", "15"],
            "FixedWidthEncoding": "utf-8",
            "DelimitedEncoding": "utf-8",
            "IncludeHeader": "True",
        }
    )


def test_fixed_width_generator_process(fixed_width_generator, sample_spec, tmp_path):
    with patch("os.makedirs"):
        with patch("builtins.open", mock_open()) as mock_file:
            result = fixed_width_generator.process(sample_spec, num_rows=5)
            assert result == "fixed_width_data.txt"
            assert mock_file.call_count == 1


def test_get_fake_dataset(fixed_width_generator, sample_spec):
    dataset = fixed_width_generator._get_fake_dataset(sample_spec, num_rows=3)
    assert len(dataset) == 4  # Header + 3 rows
    assert len(dataset[0]) == sum(sample_spec.offsets)  # Header
    for row in dataset[1:]:
        assert len(row) == sum(sample_spec.offsets)


def test_generate_random_data(fixed_width_generator):
    data = fixed_width_generator._generate_random_data(10)
    assert len(data) == 10
    assert all(c.isalnum() for c in data)


def test_generate_data_row(fixed_width_generator, sample_spec):
    row = fixed_width_generator._generate_data_row(sample_spec.offsets)
    assert len(row) == sum(sample_spec.offsets)


def test_generate_header(fixed_width_generator, sample_spec):
    header = fixed_width_generator._generate_header(
        sample_spec.column_names, sample_spec.offsets
    )
    assert len(header) == sum(sample_spec.offsets)
    assert header.startswith("Name      Age")


# DelimitedParser Tests
@pytest.fixture
def delimited_parser():
    return DelimitedParser()


def test_delimited_parser_process_error(delimited_parser, sample_spec):
    with pytest.raises(Exception):
        delimited_parser.process(sample_spec, "non_existent_file.txt", "output.csv")


# FileProcessorFactory Tests
def test_file_processor_factory():
    assert isinstance(
        FileProcessorFactory.get_processor("fixed_width_generator"), FixedWidthGenerator
    )
    assert isinstance(
        FileProcessorFactory.get_processor("delimited_parser"), DelimitedParser
    )
    with pytest.raises(ValueError):
        FileProcessorFactory.get_processor("invalid_processor")


# Run the tests
if __name__ == "__main__":
    pytest.main()
