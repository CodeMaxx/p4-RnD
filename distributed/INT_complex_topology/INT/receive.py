#!/usr/bin/env python
import sys
import struct
import os

from scapy.all import sniff, sendp, hexdump, get_if_list, get_if_hwaddr
from scapy.all import Packet, IPOption
from scapy.all import ShortField, IntField, LongField, BitField, FieldListField, FieldLenField, ByteField
from scapy.all import Ether, IP, UDP, TCP, Raw
from scapy.layers.inet import _IPOption_HDR

HOPS = 3
ShimSize = 4
TailSize = 4
INTSize = 8
MetadataSize = 8

class ShimHeader(Packet):
    name = 'Shim Header'
    fields_desc = [
        ByteField('int_type', 0),
        ByteField('rsvd1', 0),
        ByteField('len', 0),
        ByteField('rsvd2', 0),
    ]


class TailHeader(Packet):
    name = 'Tail Header'
    fields_desc = [
        ByteField('next_proto', 0),
        ShortField('dest_port', 0),
        ByteField('dscp', 0),
    ]


class INTHeader(Packet):
    name = 'INT Header'
    fields_desc = [
        BitField('ver', 0, 4),
        BitField('rep', 0, 2),
        BitField('c', 0, 1),
        BitField('e', 0, 1),
        BitField('m', 0, 1),
        BitField('rsvd1', 0, 7),
        BitField('rsvd2', 0, 3),
        BitField('ins_cnt', 0, 5),
        ByteField('remaining_hop_cnt', 0),
        BitField('instruction_mask_0003', 0, 4),
        BitField('instruction_mask_0407', 0, 4),
        BitField('instruction_mask_0811', 0, 4),
        BitField('instruction_mask_1215', 0, 4),
        ShortField('rsvd3', 0)
    ]


class MetadataHeader(Packet):
    name = 'Metadata Header'
    fields_desc = [
        IntField('SwitchID', 0),
        ShortField('IngressPort', 0),
        ShortField('EgressPort', 0)
    ]


def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

class IPOption_MRI(IPOption):
    name = "MRI"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="swids",
                                  adjust=lambda pkt,l:l+4),
                    ShortField("count", 0),
                    FieldListField("swids",
                                   [],
                                   IntField("", 0),
                                   length_from=lambda pkt:pkt.count*4) ]


def handle_pkt(pkt):
    print("got a packet")
    print("pkt length=")
    print(len(pkt))
    pkt.show2()
    p1 = pkt.copy()

    p1 = p1.payload.payload.payload

    p1_bytes = bytes(p1)

    ShimHeader(p1_bytes[0:ShimSize]).show()
    p1_bytes = p1_bytes[ShimSize:]

    INTHeader(p1_bytes[0:INTSize]).show()
    p1_bytes = p1_bytes[INTSize:]

    for i in range(HOPS):
        MetadataHeader(p1_bytes[0:MetadataSize]).show()
        p1_bytes = p1_bytes[MetadataSize:]

    TailHeader(p1_bytes).show()

#    hexdump(pkt)
    sys.stdout.flush()


def main():
    ifaces = filter(lambda i: 'eth' in i, os.listdir('/sys/class/net/'))
    iface = ifaces[0]
    print("sniffing on %s" % iface)
    sys.stdout.flush()
    sniff(filter="tcp", iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()
