from scapy.all import *
import argparse
from matplotlib import pyplot
    
def main():
    args = get_args()
    split_by_time(args.file, args.start, args.add)


def split_by_time(file, start, add):
    packets = rdpcap(file) 
    fileName = file.split(".pcap")[0] + "_splited.pcap"
    start_packet = get_start_time(packets, start)
    write_packet = []
    for p in packets:
        if p.time > packets[start_packet].time and packets[start_packet].time + add > p.time:
            if p["Ethernet"].type == int("0x0800",16):
                write_packet.append(p)
                
    wrpcap(fileName, write_packet)

def get_start_time(packets, start) -> int:
    i=0
    for p in packets:
        i+=1
        if p.time - packets[0].time > start:
            return i


def get_args():
    #準備
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", type=str)
    parser.add_argument("--start", type=int)
    parser.add_argument("--add", type=int)

    #結果を受け取る
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
