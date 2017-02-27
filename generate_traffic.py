#!/usr/bin/python

import sys, getopt
from scapy.all import *
import os
from multiprocessing import Process

# Maintain VM-ethinterface-IP mapping
vm = {
    "id": {
        "groupfive-east": {
            "eth1": "192.168.1.1",
            "eth2": "192.168.2.1",
            "eth3": "192.168.3.1",
            "eth4": "192.168.4.1"
        },
        "groupfive-west": {
            "eth1": "192.168.1.2",
            "eth2": "192.168.2.2",
            "eth3": "192.168.3.2",
            "eth4": "192.168.4.2"
        }
    }
}


'''rtp_payload_types = {
    # http://www.iana.org/assignments/rtp-parameters
    0:  'G.711 PCMU',    3:  'GSM',
    4:  'G723',          5:  'DVI4',
    6:  'DVI4',          7:  'LPC',
    8:  'PCMA',          9:  'G722',
    10: 'L16',           11: 'L16',
    12: 'QCELP',         13: 'CN',
    14: 'MPA',           15: 'G728',
    16: 'DVI4',          17: 'DVI4',
    18: 'G729',          25: 'CelB',
    26: 'JPEG',          28: 'nv',
    31: 'H261',          32: 'MPV',
    33: 'MP2T',          34: 'H263' }
'''


# Interface and traffic mapping
# eth1 -> eth1: VOIP
# eth2 -> eth2: ICMP with Payload Size
# eth3 -> eth3: TCP/UDP
# eth4 -> eth4: HTTP


# Perform TFTP copy
'''
def create_tftp_transfer(rtr_dst_ip):
    connect = 'tftp ' + rtr_dst_ip
    os.system(connect)
    while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        if line == "tftp>":
            count = 1
            print 'File transfer complete'
            os.system('quit')
        else: # an empty line means stdin has been closed
            print('eof')
            exit(0)
    else:
        print 'Failed to request TFTP file'
'''

# Create TCP and UDP packets
def create_tcp_udp_packets(intf, rtr_src_ip, rtr_dst_ip, total_packets):
    print 'Start of create_tcp_udp_packets'
    packet_tcp = IP(dst=rtr_dst_ip, src=rtr_src_ip)/TCP()/Raw(RandString(size=1000))
    packet_udp = IP(dst=rtr_dst_ip, src=rtr_src_ip)/UDP()/Raw(RandString(size=1000))
    for packets in range(0, total_packets):
        send(packet_tcp, iface=intf)
        send(packet_udp, iface=intf)

     
# Create HTTP packets
def create_http_packets(intf, rtr_dst_ip, total_packets):
    print 'Start of create_http_packets'
    packet = IP(dst=rtr_dst_ip)/TCP()/"GET / HTTP/1.0\r\n\r\n"/Raw(RandString(size=1000))
    for packets in range(0, total_packets):
        send(packet, iface=intf)


# Create ICMP packets
def create_icmp_packets(intf, rtr_dst, total_packets):
    print 'Start of create_icmp_packets'
    icmp = ICMP()
    packet = IP(dst=rtr_dst)
    for packet_num in range(0, total_packets):
        for i_type in range(0, 256):
            for i_code in range(0, 256):
                icmp.type = i_type
                icmp.code = i_code
                send(packet/icmp/Raw(RandString(size=1200)), iface=intf) 


# Create VoIP packets
def create_voip_packets(intf, rtr_src, rtr_dst, total_packets, dscp=184, protocol='rtp'):
    # eth, IP, Src IP, Dst IP, Qos, Payload
    print 'Start of create_voip_packets'
    if protocol == 'rtp':
        rtp = {
	    "sequence": 1,
	    "timestamp": 1,
	    "marker": 1,
	    "payload_type": 17
    	}
        # Construct random data for the payload
        data = 'x0b\\x0c\\r\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\x1a\\x1b\\x1c\\x1d\\x1e\\x1f'
	packet = IP(dst=rtr_dst, 
	            src=rtr_src, 
                    tos=dscp, 
                    ttl=5)/UDP(sport=12345, dport=12345)/RTP(**rtp)/Raw(RandString(size=900))
    else:
        packet = IP(dst=rtr_dst, src=rtr_src, tos=dscp, ttl=5)
    for i in range(0, total_packets):
        sendp(packet, iface=intf)

# Main function
def main(argv):
    src_loc = ''
    dst_loc = ''
    try:
        opts, args = getopt.getopt(argv, "hd:s", ["sloc=","dloc="])
    except getopt.GetoptError:
        print 'generate_traffic.py -s <traffic_source_location> -d <traffic_destination_location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'generate_traffic.py -s <traffic_source_location> -d <traffic_destination_location>'
            sys.exit()
        elif opt in ("-s", "--sloc"):
            src_loc = arg
        elif opt in ("-d", "--dloc"):
            dst_loc = arg
    print 'Source Location for traffic generation is: ', src_loc
    print 'Destination Location for traffic end is: ', dst_loc

    # Assign number of packets
    total_packets = 10000
    
    # Create VoIP packets
    interface = 'eth1'
    rtr_src_ip = vm['id'][src_loc][interface]
    rtr_dst_ip = vm['id'][dst_loc][interface]
    process_id_1 = Process(target = create_voip_packets(interface, rtr_src_ip, rtr_dst_ip, total_packets)) 
    process_id_1.start()    
    
    # Create Scapy ICMP packets
    interface = 'eth2' 
    rtr_src_ip = vm['id'][src_loc][interface]
    rtr_dst_ip = vm['id'][dst_loc][interface]        
    process_id_2 = Process(target = create_icmp_packets(interface, rtr_dst_ip, total_packets))
    process_id_2.start()
    
    # Create TFTP transfer of a file
    interface = 'eth3' 
    rtr_src_ip = vm['id'][src_loc][interface]
    rtr_dst_ip = vm['id'][dst_loc][interface]
    # process_id_3 = Process(target = create_tftp_transfer(rtr_dst_ip))
    process_id_3 = Process(target = create_tcp_udp_packets(interface, rtr_src_ip, rtr_dst_ip, total_packets))
    process_id_3.start()

    # Create HTTP packets
    interface = 'eth4' 
    rtr_src_ip = vm['id'][src_loc][interface]
    rtr_dst_ip = vm['id'][dst_loc][interface]
    process_id_4 = Process(target = create_http_packets(interface, rtr_dst_ip, total_packets))
    process_id_4.start()    
    
    # Join processes
    process_id_1.join()
    process_id_2.join()
    process_id_3.join()
    process_id_4.join()


if __name__ == "__main__":
    main(sys.argv[1:])
