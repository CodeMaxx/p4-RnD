#!/usr/bin/env python3

# Copyright 2018-present Akash Trehan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

########################################################
# 1. Running all experiments
########################################################

import decision_time
import data_forwarding_time
import num_probe_packets
import link_traffic
import end_to_end

from utils import *


def main(pcap_data):
    cprint("STATISTICS")
    decision_time.main(pcap_data)
    data_forwarding_time.main(pcap_data)
    num_probe_packets.main(pcap_data)
    link_traffic.main(pcap_data)
    end_to_end.main(pcap_data)

if __name__ == '__main__':
    pcap_data = PcapData()
    main(pcap_data)
