from extract import ExtractXlSX,file_path
from transform import Transform, data_path
from load import SQLLoad, db_path, table_name


class ETLPipeline:
    def __init__(self, extractor: ExtractXlSX, transformer: Transform, loader: SQLLoad):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        extracted_data = self.extractor.extract_data()
        transformed_data = self.transformer.transform(extracted_data)
        self.loader.load(transformed_data)


extract_service = ExtractXlSX(file_path)
transform_service = Transform()
load_service = SQLLoad(db_path, table_name)

pipeline = ETLPipeline(extract_service, transform_service,load_service)
pipeline.run()
