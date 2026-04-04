from registry import load_registry
from utils import get_changed_block

def main():
   block = get_changed_block()
   registry = load_registry()
   entry = registry.get(block)

   print("=== HIL Review Summary ===")
   print(f"Detected Block: {block}")
   print(f"Registry Found: {entry is not None}")

   if entry:
       print(f"TX Template: {entry['tx_template']}")
       print(f"RX Template: {entry['rx_template']}")
       print(f"Input Scenarios: {entry['input_scenarios']}")
       print(f"Expected Metrics: {entry['expected_metrics']}")
   else:
       print("No registry entry found. Block is not yet HIL-supported.")

if __name__ == "__main__":
   main()
