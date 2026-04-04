from cortexlab import reserve_nodes, run_experiment

def main():
   nodes = reserve_nodes()
   run_experiment(nodes)

if __name__ == "__main__":
   main()
