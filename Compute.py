from DataPreprocessor import ReadandCombine
from SparkConnection import ConnectSpark
from InformationExtraction import InformationExtraction   
from pyspark.sql import functions
from PartTwo import PartTwo


#  PART ONE 
# Creating the spark connection
spark_connection = ConnectSpark.create_spark_session()


# reading parquet data
data = spark.read.option("pathGlobFilter", "*.parquet").parquet("data/") 
data = data.dropDuplicates()


# Extracting information from the data
print("Extracting ")
factors = analysis_factors() 


info_extraction = InformationExtraction(dataframe=data, dataformat=factors)

print(info_extraction.dataformat)

info_extraction.count_packets()
info_extraction.length_factors()
info_extraction.timespan()
info_extraction.count_unique_ip()
info_extraction.top_five_talkers()
info_extraction.checksums_errors()
info_extraction.malformed_errors()

print(f" This is the data extracted in total\n : {info_extraction.dataformat}") 



# dumpisn thr extarcted information into json format
with open("data_partone.json", "w", encoding="utf-8") as f:
    json.dump(info_extraction.dataformat, f, indent=2, ensure_ascii=False)

# PART TWO 

batched_data = PartTwo(data).group_per_minute()


with open("data_partwo.json", "w", encoding="utf-8") as f:
    json.dump(batched_data, f, indent=2, ensure_ascii=False) 
    
    
plt_data = batched_data.toPandas()

fig = px.line(
    plt_data,
    x="minute",
    y="packet_count",
    title="Interactive Plot: Frames (Packets) per Minute",
    labels={"minute": "Minute", "packet_count": "Number of Frames"},
    markers=True
)


# Update line trace style
fig.update_traces(
    hovertemplate="<b>Minute</b>: %{x}<br><b>Frames</b>: %{y}",
    line=dict(width=2, color="orange")  # Set line color to orange
)


# Dark-style layout
fig.update_layout(
    hovermode="x unified",
    xaxis=dict(showgrid=True, tickangle=-45, color='white'),
    yaxis=dict(showgrid=True, color='white'),
    template=None,  # Disable default template to allow custom styling
    plot_bgcolor='rgba(20,20,20,1)',   # dark grayish background for plot area
    paper_bgcolor='rgba(10,10,10,1)',  # even darker for the whole figure
    font=dict(color='white'),
    title_font=dict(size=20, color='orange'),
    margin=dict(l=40, r=40, t=60, b=80)
)


fig.show()


# List of TCP flags and aliases
tcp_flags = {
    "`tcp.flags.syn`": "syn",
    "`tcp.flags.ack`": "ack",
    "`tcp.flags.fin`": "fin",
    "`tcp.flags.rst`": "rst",
    "`tcp.flags.psh`": "psh",
    "`tcp.flags.urg`": "urg",
    "`tcp.flags.ece`": "ece",
    "`tcp.flags.cwr`": "cwr"
}


# Build the column expressions
flag_exprs = [
    functions.sum(functions.col(col).cast("int")).alias(alias)
    for col, alias in tcp_flags.items()
]

# Select and compute the sums
flag_counts = data.select(flag_exprs)
with open("data_parthree.json", "w", encoding="utf-8") as f:
    json.dump(flag_counts, f, indent=2, ensure_ascii=False)

# Convert to Pandas for plotting
flag_df = flag_counts.toPandas().T.reset_index()
flag_df.columns = ["flag", "count"]
flag_df.sort_values(by="count", ascending=False, inplace=True)

fig = px.bar(
    flag_df,
    x="flag",
    y="count",
    title="Distribution of TCP Flags",
    labels={"flag": "TCP Flag", "count": "Count"},
    color="flag",
    template="plotly_dark"
)


fig.update_layout(
    plot_bgcolor='rgba(20,20,20,1)',
    paper_bgcolor='rgba(10,10,10,1)',
    font=dict(color='white'),
    title_font=dict(size=20, color='orange'),
    xaxis=dict(tickangle=-45),
    margin=dict(l=40, r=40, t=60, b=60)
)

fig.show()






