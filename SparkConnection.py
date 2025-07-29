from pyspark.sql import SparkSession

class ConnectSpark:
    @staticmethod
    def connect_spark():
        try:
            spark = SparkSession.builder \
                .appName('app') \
                .master('local[*]') \
                .config("spark.hadoop.io.nativeio.NativeIO", "false") \
                .getOrCreate()
            print("Spark session has started successfully")
            return spark
        except Exception as e:
            print(f"There is an error in starting Spark session: {e}")
