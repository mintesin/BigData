from SparkConnection import ConnectSpark
import os

"""
This module reads multiple CSV files using PySpark,
stacks them together, and saves the result as JSON.
"""

class ReadandCombine:
    def __init__(self, paths):
        self.paths = paths 
        self.output_path = 'output'
        self.spark = ConnectSpark.connect_spark()
        self.combined_data = None

    def combine(self, output_path) -> object:
        try:
            for enum, data in enumerate(self.paths):
                data_frame = self.spark.read.option("header", "true") \
                                            .option("inferSchema", "true") \
                                            .csv(data)
                print("reading is done ......")
                if self.combined_data is None:
                    self.combined_data = data_frame
                else:
                    self.combined_data = self.stack_csv(self.combined_data, data_frame)
            print("The data satcked ....")
            print(self.combined_data.head(10)) 
            self.change_csv_to_json(self.combined_data, output_path)

        except Exception as e:
            print(f"The process of reading and stacking data failed: {e}")

    def stack_csv(self, data_one: object, data_two: object) -> object:
        return data_one.unionByName(data_two)

    def change_csv_to_json(self, data: object, output_path: str) -> None:
        try:
            data.write.option("inferSchema", "true").mode("overwrite").json(output_path)
        except Exception as e:
            print(f"The file conversion is not done {e}")
