import os
from contextlib import contextmanager
from var import VAR
@contextmanager
def redirect_stderr(new_target):

    import sys
    old_target, sys.stderr = sys.stderr, new_target
    try:
        yield new_target
    finally:
        sys.stderr = old_target

with open(os.devnull, 'w') as errf:
    with redirect_stderr(errf):
        from scapy.all import *


#dictionary :protocal number->name
dict_pro = {0: 'HOPOPT', 1: 'ICMP', 2: 'IGMP', 3: 'GGP', 4: 'IP-in-IP', 5: 'ST', 6: 'TCP', 7: 'CBT', 8: 'EGP', 9: 'IGP', 10: 'BBN-RCC-MON', 11: 'NVP-II', 12: 'PUP', 13: 'ARGUS', 14: 'EMCON', 15: 'XNET', 16: 'CHAOS', 17: 'UDP', 18: 'MUX', 19: 'DCN-MEAS', 20: 'HMP', 21: 'PRM', 22: 'XNS-IDP', 23: 'TRUNK-1', 24: 'TRUNK-2', 25: 'LEAF-1', 26: 'LEAF-2', 27: 'RDP', 28: 'IRTP', 29: 'ISO-TP4', 30: 'NETBLT', 31: 'MFE-NSP', 32: 'MERIT-INP', 33: 'DCCP', 34: '3PC', 35: 'IDPR', 36: 'XTP', 37: 'DDP', 38: 'IDPR-CMTP', 39: 'TP++', 40: 'IL', 41: 'IPv6', 42: 'SDRP', 43: 'IPv6-Route', 44: 'IPv6-Frag', 45: 'IDRP', 46: 'RSVP', 47: 'GREs', 48: 'DSR', 49: 'BNA', 50: 'ESP', 51: 'AH', 52: 'I-NLSP', 53: 'SWIPE', 54: 'NARP', 55: 'MOBILE', 56: 'TLSP', 57: 'SKIP', 58: 'IPv6-ICMP', 59: 'IPv6-NoNxt', 60: 'IPv6-Opts', 62: 'CFTP', 64: 'SAT-EXPAK', 65: 'KRYPTOLAN', 66: 'RVD', 67: 'IPPC', 69: 'SAT-MON', 70: 'VISA', 71: 'IPCU', 72: 'CPNX', 73: 'CPHB',
     74: 'WSN', 75: 'PVP', 76: 'BR-SAT-MON', 77: 'SUN-ND', 78: 'WB-MON', 79: 'WB-EXPAK', 80: 'ISO-IP', 81: 'VMTP', 82: 'SECURE-VMTP', 83: 'VINES', 84: 'IPTM', 85: 'NSFNET-IGP', 86: 'DGP', 87: 'TCF', 88: 'EIGRP', 89: 'OSPF', 90: 'Sprite-RPC', 91: 'LARP', 92: 'MTP', 93: 'AX.25', 94: 'OS', 95: 'MICP', 96: 'SCC-SP', 97: 'ETHERIP', 98: 'ENCAP', 100: 'GMTP', 101: 'IFMP', 102: 'PNNI', 103: 'PIM', 104: 'ARIS', 105: 'SCPS', 106: 'QNX', 107: 'A/N', 108: 'IPComp', 109: 'SNP', 110: 'Compaq-Peer', 111: 'IPX-in-IP', 112: 'VRRP', 113: 'PGM', 115: 'L2TP', 116: 'DDX', 117: 'IATP', 118: 'STP', 119: 'SRP', 120: 'UTI', 121: 'SMP', 122: 'SM', 123: 'PTP', 124: 'IS-IS over IPv4', 125: 'FIRE', 126: 'CRTP', 127: 'CRUDP', 128: 'SSCOPMCE', 129: 'IPLT', 130: 'SPS', 131: 'PIPE', 132: 'SCTP', 133: 'FC', 134: 'RSVP-E2E-IGNORE', 135: 'Mobility Header', 136: 'UDPLite', 137: 'MPLS-in-IP', 138: 'manet', 139: 'HIP', 140: 'Shim6', 141: 'WESP', 142: 'ROHC'}


class Packet_r():
    """Class for loading packet and further modifications"""
    def __init__(self, packet):
        self.packet = packet

    
    def expand(self):
        """expand get all payload"""
        x = self.packet
        yield x.name, x.fields
        while x.payload:
            x = x.payload
            yield x.name, x.fields
    

    def packet_to_layerlist(self):
        """layerlist get formatted list contain every layer's detail"""
        return list(self.expand())
    

    def packet_to_all(self):
        """combine every layer parsed in to a string for further searching"""
        s = ''
        for i in self.packet_to_layerlist():
            s = s + i[0] + ":\n"
            for key in i[1]:
                s = s + "\t%s: %s\n" % (key, i[1][key])
            s = s + '\n'
        try:
            s = s + packet.load + '\n'
        except:
            s = s + '\n'
        return s


    def packet_to_load_plain(self):
        """convert every packet(including headers) to hex"""
        try:
            return (bytes(self.packet).hex())
        except:
            return ("packet cannot be converted to hex")


    def packet_to_info(self):
        """return every packet's brief information for ListCtrl"""
        try:
            pkt_src = self.packet.srcsummary()
            pkt_dst = self.packet.dstsummary()

        except:
            pkt_src = self.packet.src
            pkt_dst = self.packet.dst

            if (self.packet.getlayer(IP)):

                pkt_src = self.packet[IP].src
                pkt_dst = self.packet[IP].dst
            elif (self.packet.getlayer(IPv6)):

                pkt_src = self.packet[IPv6].src
                pkt_dst = self.packet[IPv6].dst
        try:
            if (self.packet.getlayer(IP)):
                pkt_pro=dict_pro[int(self.packet[IP].proto)]
            else:
                if 'padding' in self.packet.lastlayer().name.lower():
                    if 'raw' in self.packet.lastlayer().underlayer.name.lower():
                        pkt_pro = self.packet.lastlayer().underlayer.underlayer.name
                    else:
                        pkt_pro = self.packet.lastlayer().underlayer.name
                elif 'raw' in self.packet.lastlayer().name.lower():
                    pkt_pro = self.packet.lastlayer().underlayer.name
                else:
                    pkt_pro = self.packet.lastlayer().name

            info = [
                str(self.packet.num),
                self.packet.time, pkt_src, pkt_dst,
                str(len(self.packet)), pkt_pro
            ]

        except:
            info = [
                str(self.packet.num),
                self.packet.time, "unknown",
                "unknown", "unknown", "unknown"
            ]
        return info


    def packet_to_load_utf8(self):
        """decode packet load to UTF-8"""
        try:
            tmp = codecs.decode(bytes(self.packet.load).hex(), "hex")
        except:
            return "No load layer in this packet"
        try:
            if set(tmp.decode("utf-8")) == {"\x00"}:
                return "null"
            else:
                return tmp.decode('utf-8')
        except:
            return "Cannot decoded by utf-8\n"


    def packet_to_load_gb(self):
        """decode packet load to GB2312 (particularly for Chinese)"""
        try:
            tmp = codecs.decode(bytes(self.packet.load).hex(), "hex")
        except:
            return "No load layer in this packet"
        try:
            if set(tmp.decode("GB2312")) == {"\x00"}:
                return "null"
            else:
                return tmp.decode('GB2312')
        except:
            return "Cannot decoded by GB2312\n"


    def hexdump(self):
        """return single packet's wireshark type raw hex"""
        return hexdump(self.packet)
    

    def __getattr__(self, attr):
        """In this way, class Packet Inherit all attributes of original packet"""
        return getattr(self.packet, attr)


    def len(self):
        """return length of the packet(including header)"""
        return (len(self.packet))

    def getColor(self):
        if (self.packet.haslayer(ARP)):
            return (218,238,255)
        elif (self.packet.haslayer(ICMP)):
            return (252,224,255)
        elif (self.packet.haslayer(TCP)):
            binary_flags=bin(int(self.packet[TCP].flags.split(' ')[0]))[2:].rjust(7,'0')
            if (binary_flags[-3]=='1'):#reset
                return (164,0,0)
            elif (self.packet[TCP].sport==80 or self.packet[TCP].dport==80):#http
                return (228,255,199)
            elif (binary_flags[-2]=='1' or binary_flags[-1]=='1'):#SYN/FIN
                return (160,160,160)

            return (231,230,255)
        elif (self.packet.haslayer(UDP)):
            return (218,238,255)
        elif (self.packet.haslayer(IP)):
            if(self.packet[IP].proto in (2,88,89,112)):
            ### igmp,eigrp,ospf,vrrp
                return (255,243,214)
            else:
                return (255,255,255)
        elif (self.packet.haslayer(IPv6)):
            index=0
            try:#ICMPv6 filter
                while (self.packet[index].nh!=58):
                
                    index+=1
            except IndexError:
                return (255,255,255)
            return (252,224,255)
        else:
            return (255,255,255)