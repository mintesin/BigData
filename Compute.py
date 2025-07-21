from DataPreprocessor import ReadandCombine

paths = ["data/Car_dataset_three - Sheet2.csv"]
output_json_path = "output/json_data"

combiner = ReadandCombine(paths)
output_json_path = "/output/json_data"
combiner.combine(output_json_path)