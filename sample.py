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

# Interface and traffic mapping
# eth1 -> eth1: VOIP
# eth2 -> eth2: ICMP with Payload Size
# eth3 -> eth3: FTP
# eth4 -> eth4: IM/HTTP

def d_itg_traffic():
    # Send VOIP Packets
    # Command: ./ITGRecv



def create_packets(intf, rtr_src, rtr_dst, dscp, rtp):
    # eth, IP, Src IP, Dst IP, Qos, Payload

    
    if rtp == 1:
        rtp = {
	    "sequence": 1,
	    "timestamp": 1,
	    "marker": 1,
	    "payload_type": 17
    	}
	data = "Hello"
	packet = IP(dst=rtr_dst, 
	            src=rtr_src, 
                    tos=dscp, 
                    ttl=10)/UDP(sport=12345, dport=12345)/RTP(**rtp)/Raw(load=data)
    else:
        packet = IP(dst=rtr_dst, src=rtr_src, tos=dscp, ttl=10)
    for i in range(0, 10000):
        sendp(packet, iface=intf)
    


if __name__ == '__main__':
    #rtr_src_ip = "192.168.1.2"
    #rtr_dst_ip = "192.168.1.1"
    #interface = ["eth1", "eth2", "eth3", "eth4"]
    #interface = "eth1"
    #dscp = 46
    #rtp = 1
    #for intf in interface:
    

    # Create D-ITG VOIP Packets
    for i in range(0, 10):
        interface = 'eth1'
        rtr_src_ip = vm['id']['groupfive-west'][interface]
        rtr_dst_ip = vm['id']['groupfive-east'][interface]
        codec = 'G.729.3'
        protocol = 'RTP'
        d_itg_traffic(rtr_src_ip, rtr_dst_ip, codec, protocol)



    # create_packets(interface, rtr_src_ip, rtr_dst_ip, dscp, rtp)
