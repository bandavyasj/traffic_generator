from scapy.all import *

# Maintin  VM-ethinterface-IP mapping
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
# eth3 -> eth3: FTP
# eth4 -> eth4: IM/HTTP

#def d_itg_traffic():
    # Send VOIP Packets
    # Command: ./ITGRecv

def create_icmp_packets(intf, rtr_dst):
    # ans,unans=sr(IP(dst="192.168.1.1-254")/ICMP())
    icmp = ICMP()
    packet = IP(dst=rtr_dst)
    for packet_num in range(0, 10000):
        for i_type in range(0, 256):
            for i_code in range(0, 256):
                icmp.type = i_type
                icmp.code = i_code
                send(packet/icmp/Raw(RandString(size=1200)), iface=intf) 


def create_voip_packets(intf, rtr_src, rtr_dst, dscp=184, protocol='rtp'):
    # eth, IP, Src IP, Dst IP, Qos, Payload
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
    for i in range(0, 100000000):
        sendp(packet, iface=intf)

# Main
if __name__ == '__main__':
    #rtr_src_ip = "192.168.1.2"
    #rtr_dst_ip = "192.168.1.1"
    #interface = ["eth1", "eth2", "eth3", "eth4"]
    #interface = "eth1"
    #dscp = 46
    #rtp = 1
    #for intf in interface:
    

    # Create D-ITG VOIP Packets
    d_itg = None
    if not d_itg:
        for i in range(0, 10):
            interface = 'eth1'
            rtr_src_ip = vm['id']['groupfive-west'][interface]
            rtr_dst_ip = vm['id']['groupfive-east'][interface]
            codec = 'G.729.3'
            protocol = 'RTP'
            #d_itg_traffic(rtr_src_ip, rtr_dst_ip, codec, protocol)


    # Create Scapy VoIP packets
    interface = 'eth2'
    if interface == 'eth1':
        rtr_src_ip = vm['id']['groupfive-west'][interface]
        rtr_dst_ip = vm['id']['groupfive-east'][interface]
        create_voip_packets(interface, rtr_src_ip, rtr_dst_ip)
        # create_packets(interface, rtr_src_ip, rtr_dst_ip, dscp, rtp)
    elif interface == 'eth2':
        # Create Scapy ICMP packets
        rtr_src_ip = vm['id']['groupfive-west'][interface]
        rtr_dst_ip = vm['id']['groupfive-east'][interface]
        create_icmp_packets(interface, rtr_dst_ip)
