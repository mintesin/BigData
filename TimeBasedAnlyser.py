"""
1.  General Information (Summary Stats)

    Total number of packets captured -conting the rows 

    Total data volume (sum of frame lengths) - summing the frame size

    Count of unique protocols seen (e.g., TCP, UDP)- counting the appearance of the TCP and UDP

    Packet count by transport protocol (TCP vs UDP)

    Average packet size (frame.len) - devide the total data volume by the total number of packest captured 

    Min/Max packet size - capturing the smallest and biggest pakacge in size

    Number of unique IP addresses (src/dst IP count) - coounting the numbe riP addresses -use Set

    Number of unique MAC addresses (src/dst eth.addr count)- counting the number of mac addresses - again use Set 

    IP checksum errors - counting the number of Ip check sums error - use counter 

    malformed packets - counting the number of malformed pakets - use counter
2.
    1. Number of packets per time group by the time 
    
            -includes converting frame.time_epoch to datetime
            
            -roundint time to 1hr or so 
            
    2. Time Delat between packets
    
            -soting the data frmae with time
            
        -includes convertingt frame.time_epoch to datetime 
        
        -using .diff() to calculate the span
        
            - use visualization 
            
    3. Protocol usage Trends over time 
    
        - convert to daatetime from epoch 
        
        - grpoup by time and protocol 
        
        - perform count operation 
        
    4. Cumulative Bytes overtime 
    
        -sort data by time
        
        -calculate the comulative sum 
        
        -Merge is back  with  time  column 
    
    """