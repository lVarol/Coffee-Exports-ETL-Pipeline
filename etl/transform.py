
import pandas as pd

data_path="data/Exportations.xlsx"

class Transform:
    def transform(self,data):

        if not isinstance(data,pd.DataFrame):
            raise ValueError("Expected a DataFrame but got: {}".format(type(data)))

        data = data.dropna(how='all')

        metadata_start_index = data[data.iloc[:, 0].astype(str).str.contains("\\* Cifras preliminares", na=False)].index
        if not metadata_start_index.empty:
            last_valid_index = metadata_start_index[0] - 1
            data = data.loc[:last_valid_index]

        data['Year'] = data['Año'].astype(int)
        data['Month'] = data['Mes'].astype(int)
        data['Destination_Country'] = data['País de destino']
        data['Type_of_Coffee'] = data['Tipo de café']
        data['Bags of 60 Kg. Exported'] = data['Sacos de 60 Kg. Exportados'].astype(int)

        selected_columns = ['Year','Month','Destination_Country','Type_of_Coffee','Bags of 60 Kg. Exported']
        filtered_data = data[selected_columns]

        
        output_path = "data/Exportations_cleaned.xlsx"
        filtered_data.to_excel(output_path, index=False)
    
        return filtered_data 
    