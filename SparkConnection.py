from pyspark.sql import SparkSession

class ConnectSpark:

   def create_spark_session(): 
    
    """
    Create a Spark session and return the session with a success message and Spark context.
    In case of failure, it prints an error message.
    """
    try:
        spark = SparkSession.builder \
            .appName("Network Packet Analysis") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
        print(f"The spark session is created successfully with context of \n {spark.sparkContext.master} and \n {spark.sparkContext.appName}")
        return spark
    except Exception as e:
        print(f"Creating spark session has failed with an error of: {e}")
