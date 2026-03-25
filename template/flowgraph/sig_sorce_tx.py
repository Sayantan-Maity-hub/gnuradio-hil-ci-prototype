#!/usr/bin/env python3

from gnuradio import gr, analog, blocks, uhd
from argparse import ArgumentParser
import time

class TX(gr.top_block):
    def __init__(self, waveform, freq, amp, samp_rate):
        gr.top_block.__init__(self, "tx")

        # Map waveform string → GNU Radio constant
        wave_map = {
            "sine": analog.GR_SIN_WAVE,
            "cosine": analog.GR_COS_WAVE,
            "square": analog.GR_SQR_WAVE,
            "triangle": analog.GR_TRI_WAVE
        }

        self.src = analog.sig_source_c(
            samp_rate,
            wave_map[waveform],
            freq,
            amp,
            0
        )

        self.sink = uhd.usrp_sink(
            ",".join(("", "")),
            uhd.stream_args(cpu_format="fc32", channels=[0]),
        )

        self.sink.set_samp_rate(samp_rate)
        self.sink.set_center_freq(0, 0)
        self.sink.set_gain(0, 0)

        self.connect(self.src, self.sink)


def main():
    parser = ArgumentParser()
    parser.add_argument("--waveform", type=str, default="sine")
    parser.add_argument("--frequency", type=float, default=1000)
    parser.add_argument("--amplitude", type=float, default=1.0)
    parser.add_argument("--duration", type=int, default=10)

    args = parser.parse_args()

    tb = TX(args.waveform, args.frequency, args.amplitude, 32000)

    tb.start()
    time.sleep(args.duration)
    tb.stop()
    tb.wait()


if __name__ == "__main__":
    main()