class PartTwo:
    def __init__(self, dataframe: DataFrame):
        self.dataframe = dataframe

    def group_per_minute(self) -> DataFrame:
        # Convert epoch to timestamp
        df = self.dataframe.withColumn(
            'timestamp',
            functions.from_unixtime(functions.col("`frame.time_epoch`").cast("double")).cast("timestamp")
        )

        # Truncate timestamp to minute
        df = df.withColumn(
            "minute",
            functions.date_trunc("minute", functions.col("timestamp"))
        )

        # Group by minute and aggregate packet count and total bytes
        batched_data = (
            df.groupBy("minute")
            .agg(
                functions.count("*").alias("packet_count"),
                functions.sum(functions.col("`frame.len`").cast("long")).alias("total_bytes")  # safer to cast to long
            )
            .orderBy("minute")
        )

        return batched_data 



