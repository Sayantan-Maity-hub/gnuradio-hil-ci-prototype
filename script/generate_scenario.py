def build_scenario(tx_node, rx_node, image_tag):
    return {
        "description": "GNU Radio HIL CI experiment",
        "duration": 300,
        "nodes": {
            tx_node: {
                "container": [{
                    "image": image_tag,
                    "command": "python3 /app/tx.py --config /app/run_config.json"
                }]
            },
            rx_node: {
                "container": [{
                    "image": image_tag,
                    "command": "python3 /app/rx.py --config /app/run_config.json"
                }]
            }
        }
    }