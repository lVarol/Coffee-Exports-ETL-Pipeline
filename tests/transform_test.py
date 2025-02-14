import pytest
import pandas as pd
from etl.transform import Transform

@pytest.fixture
def sample_data():
    """Create a sample DataFrame simulating raw extracted data"""
    return pd.DataFrame({
        "Año": [2023, 2024, 2024],
        "Mes": [1, 2, 3],
        "País de destino": ["USA", "Germany", "France"],
        "Tipo de café": ["Arabica", "Robusta", "Blend"],
        "Sacos de 60 Kg. Exportados": [500, 600, 700]
    })

@pytest.fixture
def transformer():
    """Fixture to initialize Transform class"""
    return Transform()

def test_transform_data(transformer, sample_data):
    """Check if transformation works correctly"""
    transformed_data = transformer.transform(sample_data)

    assert isinstance(transformed_data, pd.DataFrame), "Output is not a DataFrame"
    assert not transformed_data.empty, "Transformed DataFrame is empty"
    
    expected_columns = ['Year', 'Month', 'Destination_Country', 'Type_of_Coffee', 'Bags of 60 Kg. Exported']
    assert list(transformed_data.columns) == expected_columns, "Transformed DataFrame has incorrect columns"
