import json
from pyspark.sql import DataFrame, functions

# Schema of  the JSON data to be returned
def analysis_factors():
    return {
        "total_packets": "",
        "total_frame_size": "", 
        "total_packet_size": "",
        "average_frame_size": "",
        "average_packet_size": "",
        "minmax_frame_size": {"min": "", "max": ""},
        "minmax_packet_size": {"min": "", "max": ""},
        "number_of_unique_ip": {"dst_ip": "", "src_ip": ""},
        "top_talkers": {"top_talkers_by_dst": "", "top_talkers_by_src": ""},
        "checksum_errors": {"true": "", "false": ""},
        "malformed_errors": ""
    }

class InformationExtraction:
    """
    This class is to extract the necessary information from the parquet to finish 
    Part one analysis of the project. The methods include.
    - Counting the total number of packets.
    - The timepan in which the packets are sniffed in Hours.
    - Total frame length(Transport layer) and total packet length (network layer).
    - Count of unique IP addresses from both the source and the destination.
    - Top five talkers from both the source and destination of the packets. 
    - Count of checksum errors done.
    - Malformed errors.
    """
    def __init__(self, dataframe: DataFrame, dataformat: dict):
        self.dataframe = dataframe
        self.dataformat = dataformat

    def count_packets(self):
        print("Counting the total number of packets.......")
        count = self.dataframe.count()
        self.dataformat["total_packets"] = count
        return count
    def timespan(self):
        print("Extracting the timespan of the sniffing .......")
        min_time_epoch = self.dataframe.select(functions.min("`frame.time_epoch`")).first()[0]
        max_time_epoch = self.dataframe.select(functions.max("`frame.time_epoch`")).first()[0]

        # Compute period in seconds, then convert to hours
        time_span_seconds = float(max_time_epoch) - float(min_time_epoch)
        time_span_hours = time_span_seconds / 3600
        self.dataformat['sniffing_timespan'] = time_span_hours 
        
    def length_factors(self):
        print("Calculating the total frame size captured......")
        total_frame_length = self.dataframe.select(functions.sum("`frame.len`")).first()[0]
        total_packet_length = self.dataframe.select(functions.sum("`ip.len`")).first()[0] 
        count = self.count_packets()

        self.dataformat["total_frame_size"] = total_frame_length
        self.dataformat["total_packet_size"] = total_packet_length
        self.dataformat["average_frame_size"] = total_frame_length / count
        self.dataformat["average_packet_size"] = total_packet_length / count

        self.dataformat["minmax_frame_size"]["min"] = self.dataframe.select(functions.min("`frame.len`")).first()[0]
        self.dataformat["minmax_frame_size"]["max"] = self.dataframe.select(functions.max("`frame.len`")).first()[0]
        self.dataformat["minmax_packet_size"]["min"] = self.dataframe.select(functions.min("`ip.len`")).first()[0]
        self.dataformat["minmax_packet_size"]["max"] = self.dataframe.select(functions.max("`ip.len`")).first()[0]

    def count_unique_ip(self):
        print("Counting the unique IP addresses .....")
        self.dataformat["number_of_unique_ip"]["src_ip"] = self.dataframe.select("`ip.src`").distinct().count()
        self.dataformat["number_of_unique_ip"]["dst_ip"] = self.dataframe.select("`ip.dst`").distinct().count()
       

    def top_five_talkers(self): 
        print("Getting top five talkers .....")
        src_rows = self.dataframe.groupBy("`ip.src`").count().orderBy(functions.col("count").desc()).limit(5).collect()
        dst_rows = self.dataframe.groupBy("`ip.dst`").count().orderBy(functions.col("count").desc()).limit(5).collect()
        self.dataformat["top_talkers"]["top_talkers_by_src"] = [row["ip.src"] for row in src_rows]
        self.dataformat["top_talkers"]["top_talkers_by_dst"] = [row["ip.dst"] for row in dst_rows]

    def checksums_errors(self):
        print("Counting the number of checksum Errors.....")
        rows = self.dataframe.groupBy("`errors.checksum_error`").count().collect()
        for row in rows:
            self.dataformat["checksum_errors"][str(row["errors.checksum_error"]).lower()] = row["count"]
    def malformed_errors(self):
        print("Counting the malformed errors ....")
        rows = self.dataframe.groupBy("`errors.malformed_packet`").count().collect()
        malformed_dict = {str(row["errors.malformed_packet"]).lower(): row["count"] for row in rows}
        self.dataformat["malformed_errors"] = malformed_dict
 

