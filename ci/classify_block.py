import yaml

def load_registry(path="configs/block_test_registry.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_block_test_config(block_name, registry):
    return registry.get(block_name)

registry = load_registry()
block_name = "sig_source"
config = load_block_test_config(block_name, registry)

if config is None:
    print(f"No test configuration found for block: {block_name}")
    print("Developer must provide block-specific test definition.")
else:
    print("Loaded test configuration:")
    print(config)    

