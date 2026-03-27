for block_name, block_cfg in ["block_test_registry"].items():
    with open(block_cfg["scenario_template"], "r") as f:
        template = f.read()

    for cfg in block_cfg["input_options"]:
        param_names = block_cfg["input_format"]
        param_values = dict(zip(param_names, cfg))

        scenario_text = template.format(
            tx_node=TX_NODE,
            rx_node=RX_NODE,
            image_tag=IMAGE_TAG,
            **param_values
        )

        with open("scenario.yaml", "w") as f:
            f.write(scenario_text)

        # create task, submit task, monitor execution, collect result