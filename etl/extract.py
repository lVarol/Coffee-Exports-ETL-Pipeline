import pandas as pd
import requests

file_path = "https://federaciondecafeteros.org/app/uploads/2024/04/Exportaciones.xlsx"


class ExtractXlSX:
    def __init__(self,file_path):
        self.file_path = file_path 

        try:
            response = requests.get(file_path)
            response.raise_for_status()

            with open("data/Exportations.xlsx", "wb") as f:
                f.write(response.content)
                
        except Exception as e:
            print(f"Extraction Failed fetching data: {e}")
    

    
    def extract_data(self):
        
        try:
            data = pd.read_excel("data/Exportations.xlsx",sheet_name="7. Destino_Tipo_Vol_Val",header=7,usecols="C:I")
            
            return data
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None







