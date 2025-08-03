import os
import concurrent.futures
import pyarrow as pa
import pyarrow.parquet as pq
from scapy.all import Ether, IP, UDP, TCP
from tqdm import tqdm

def packet_to_row(pkt, filename):
    try:
        return {
            "pcap_filename": filename,
            "frame.time_epoch": str(pkt.time) if hasattr(pkt, 'time') else "",
            "frame.len": len(pkt),
            "frame.protocols": "",

            "eth.src": pkt[Ether].src if pkt.haslayer(Ether) else "",
            "eth.dst": pkt[Ether].dst if pkt.haslayer(Ether) else "",
            "eth.type": hex(pkt[Ether].type) if pkt.haslayer(Ether) else "",

            "ip.src": pkt[IP].src if pkt.haslayer(IP) else "",
            "ip.dst": pkt[IP].dst if pkt.haslayer(IP) else "",
            "ip.len": pkt[IP].len if pkt.haslayer(IP) else None,
            "ip.flags": str(pkt[IP].flags) if pkt.haslayer(IP) else "",
            "ip.flags.rb": bool(pkt[IP].flags & 0x04) if pkt.haslayer(IP) else False,
            "ip.flags.df": bool(pkt[IP].flags.DF) if pkt.haslayer(IP) else False,
            "ip.flags.mf": bool(pkt[IP].flags.MF) if pkt.haslayer(IP) else False,
            "ip.frag_offset": pkt[IP].frag if pkt.haslayer(IP) else None,
            "ip.ttl": pkt[IP].ttl if pkt.haslayer(IP) else None,
            "ip.checksum": pkt[IP].chksum if pkt.haslayer(IP) else None,
            "ip.checksum.status": "",

            "udp.srcport": pkt[UDP].sport if pkt.haslayer(UDP) else None,
            "udp.dstport": pkt[UDP].dport if pkt.haslayer(UDP) else None,
            "udp.length": pkt[UDP].len if pkt.haslayer(UDP) else None,
            "udp.checksum.status": "",

            "tcp.srcport": pkt[TCP].sport if pkt.haslayer(TCP) else None,
            "tcp.dstport": pkt[TCP].dport if pkt.haslayer(TCP) else None,
            "tcp.flags.syn": pkt[TCP].flags.S if pkt.haslayer(TCP) else False,
            "tcp.flags.ack": pkt[TCP].flags.A if pkt.haslayer(TCP) else False,
            "tcp.flags.fin": pkt[TCP].flags.F if pkt.haslayer(TCP) else False,
            "tcp.flags.rst": pkt[TCP].flags.R if pkt.haslayer(TCP) else False,
            "tcp.flags.psh": pkt[TCP].flags.P if pkt.haslayer(TCP) else False,
            "tcp.flags.urg": pkt[TCP].flags.U if pkt.haslayer(TCP) else False,
            "tcp.flags.ece": pkt[TCP].flags.E if pkt.haslayer(TCP) else False,
            "tcp.flags.cwr": pkt[TCP].flags.C if pkt.haslayer(TCP) else False,
            "tcp.checksum.status": "",

            "errors.checksum_error": False,
            "errors.malformed_packet": False,
        }
    except Exception as e:
        return {
            "pcap_filename": filename,
            **{k: None for k in [  # fill all fields as None or False on error
                "frame.time_epoch", "frame.len", "frame.protocols",
                "eth.src", "eth.dst", "eth.type",
                "ip.src", "ip.dst", "ip.len", "ip.flags", "ip.flags.rb", "ip.flags.df", "ip.flags.mf",
                "ip.frag_offset", "ip.ttl", "ip.checksum", "ip.checksum.status",
                "udp.srcport", "udp.dstport", "udp.length", "udp.checksum.status",
                "tcp.srcport", "tcp.dstport", "tcp.flags.syn", "tcp.flags.ack", "tcp.flags.fin",
                "tcp.flags.rst", "tcp.flags.psh", "tcp.flags.urg", "tcp.flags.ece", "tcp.flags.cwr",
                "tcp.checksum.status"
            ]},
            "errors.checksum_error": False,
            "errors.malformed_packet": True
        }


schema = pa.schema([
    ("pcap_filename", pa.string()),
    ("frame.time_epoch", pa.string()),
    ("frame.len", pa.int32()),
    ("frame.protocols", pa.string()),

    ("eth.src", pa.string()),
    ("eth.dst", pa.string()),
    ("eth.type", pa.string()),

    ("ip.src", pa.string()),
    ("ip.dst", pa.string()),
    ("ip.len", pa.int32()),
    ("ip.flags", pa.string()),
    ("ip.flags.rb", pa.bool_()),
    ("ip.flags.df", pa.bool_()),
    ("ip.flags.mf", pa.bool_()),
    ("ip.frag_offset", pa.int32()),
    ("ip.ttl", pa.int32()),
    ("ip.checksum", pa.int32()),
    ("ip.checksum.status", pa.string()),

    ("udp.srcport", pa.int32()),
    ("udp.dstport", pa.int32()),
    ("udp.length", pa.int32()),
    ("udp.checksum.status", pa.string()),

    ("tcp.srcport", pa.int32()),
    ("tcp.dstport", pa.int32()),
    ("tcp.flags.syn", pa.bool_()),
    ("tcp.flags.ack", pa.bool_()),
    ("tcp.flags.fin", pa.bool_()),
    ("tcp.flags.rst", pa.bool_()),
    ("tcp.flags.psh", pa.bool_()),
    ("tcp.flags.urg", pa.bool_()),
    ("tcp.flags.ece", pa.bool_()),
    ("tcp.flags.cwr", pa.bool_()),
    ("tcp.checksum.status", pa.string()),

    ("errors.checksum_error", pa.bool_()),
    ("errors.malformed_packet", pa.bool_()),
])

from scapy.all import RawPcapReader

def process_pcap_file(src_path, filename, output_path):
    full_path = os.path.join(src_path, filename)
    print(f"Processing: {full_path}")
    try:
        rows = []
        for pkt_data, _ in RawPcapReader(full_path):
            pkt = Ether(pkt_data)
            rows.append(packet_to_row(pkt, filename))

        if rows:
            table = pa.Table.from_pylist(rows, schema=schema)

            output_file = os.path.join(output_path, f"{filename}.parquet")
            pq.write_table(table, output_file)
            print(f"✅ Done: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Failed: {filename} — {e}")
        return None



def process_pcap_wrapper(args):
    return process_pcap_file(*args)


if __name__ == "__main__":
    output_path = "parquets"
    src_path = 'archive'

    os.makedirs(output_path, exist_ok=True)
    # Collect both .pcap and .pcapng files
    pcaps = [f for f in os.listdir(src_path)]

    # Prepare arguments: (src_path, filename, output_path)
    args = [(src_path, f, output_path) for f in pcaps]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(process_pcap_wrapper, args))