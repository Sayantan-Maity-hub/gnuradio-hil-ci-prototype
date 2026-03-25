def generate_rx(rx_lines):
    with open("rx.py", "w") as f:
        f.write("from gnuradio import gr, blocks, uhd\n")
        f.write("class RX(gr.top_block):\n")
        f.write("    def __init__(self):\n")
        f.write("        gr.top_block.__init__(self, 'rx')\n")

        for line in rx_lines:
            f.write("        " + line)