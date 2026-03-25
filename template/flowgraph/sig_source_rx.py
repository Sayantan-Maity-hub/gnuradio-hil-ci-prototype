#!/usr/bin/env python3

from gnuradio import gr, blocks, uhd
from argparse import ArgumentParser
import time

class RX(gr.top_block):
    def __init__(self, samp_rate, output_file):
        gr.top_block.__init__(self, "rx")

        self.src = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(cpu_format="fc32", channels=[0]),
        )

        self.src.set_samp_rate(samp_rate)
        self.src.set_center_freq(0, 0)
        self.src.set_gain(0, 0)

        self.sink = blocks.file_sink(
            gr.sizeof_gr_complex,
            output_file
        )

        self.connect(self.src, self.sink)


def main():
    parser = ArgumentParser()
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--output", type=str, default="rx_output.dat")

    args = parser.parse_args()

    tb = RX(32000, args.output)

    tb.start()
    time.sleep(args.duration)
    tb.stop()
    tb.wait()


if __name__ == "__main__":
    main()