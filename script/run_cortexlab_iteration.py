template = open(block_cfg["sig_source_scenario.yaml"]).read()

scenario_text = template.format(
    tx_node=TX_NODE,
    rx_node=RX_NODE,
    image_tag=IMAGE_TAG,
    block_name="sig_source",
    duration=params["duration"]
)

with open(f"{iter_dir}/scenario.yaml", "w") as f:
    f.write(scenario_text)