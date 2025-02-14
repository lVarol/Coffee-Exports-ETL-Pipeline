import pytest
import os
import pandas as pd
from etl.extract import ExtractXlSX
from etl import ExtractXlSX, Transform, SQLLoad
import openpyxl



FILE_PATH = "https://federaciondecafeteros.org/app/uploads/2024/04/Exportaciones.xlsx"
LOCAL_FILE_PATH = "data/Exportations.xlsx"

@pytest.fixture
def extractor():
    """Fixture to initialize ExtractXlSX"""
    return ExtractXlSX(FILE_PATH)

def test_file_download(extractor):
    """Check if the file is downloaded successfully"""
    assert os.path.exists(LOCAL_FILE_PATH), "File was not downloaded"

def test_extract_data(extractor):
    """Check if extract_data() returns a valid DataFrame"""
    data = extractor.extract_data()

    print(f"Extracted data type: {type(data)}")  # ✅ Debug print
    if data is not None:
        print(f"Extracted DataFrame Shape: {data.shape}")  # ✅ Debug print
        print(f"Extracted Columns: {data.columns}")  # ✅ Debug print

    assert data is not None, "Extracted data is None (possibly due to an extraction error)"
    assert isinstance(data, pd.DataFrame), f"Extracted data is not a DataFrame, got {type(data)} instead"
