import re

#client 
def parse_node1_logs(filename):
    """Parse Node 1 logs to extract 'Sending SET' and 'Finished SET' timestamps."""
    sending_times = []
    finished_times = []
    with open(filename, 'r') as file:
        for line in file:
            sending_match = re.search(r"Sending SET at: (\d+) μs", line)
            finished_match = re.search(r"Finished SET at: (\d+) μs", line)
            if sending_match:
                sending_times.append(int(sending_match.group(1)))
            if finished_match:
                finished_times.append(int(finished_match.group(1)))
    return sending_times, finished_times

#server
def parse_node2_logs(filename):
    """Parse Node 2 logs to extract 'OnNetworkReceive' and 'SeaaBuffer_Completed' timestamps."""
    network_receive_times = []
    seaa_buffer_times = []
    with open(filename, 'r') as file:
        for line in file:
            network_receive_match = re.search(r"OnNetworkReceive.*at (\d+) μs", line)
            seaa_buffer_match = re.search(r"SeaaBuffer_Completed.*at (\d+) μs", line)
            if network_receive_match:
                network_receive_times.append(int(network_receive_match.group(1)))
            if seaa_buffer_match:
                seaa_buffer_times.append(int(seaa_buffer_match.group(1)))
    return network_receive_times[1:], seaa_buffer_times[1:]

def calculate_latencies(node1_sending, node1_finished, node2_receive, node2_complete):
    """Calculate Node 1 to Node 2 and Node 2 to Node 1 latencies."""
    node1_to_node2 = [recv - send for send, recv in zip(node1_sending, node2_receive)]
    node2_to_node1 = [complete - finish for finish, complete in zip(node1_finished, node2_complete)]
    return node1_to_node2, node2_to_node1

def main():
    # File paths (update with your actual file paths)
    clientfile = "client.txt.txt"
    serverfile = "timestamp.txt"

    # Parse logs
    node1_sending, node1_finished = parse_node1_logs(clientfile)
    node2_receive, node2_complete = parse_node2_logs(serverfile)

    # Calculate latencies
    node1_to_node2_latencies, node2_to_node1_latencies = calculate_latencies(
        node1_sending, node1_finished, node2_receive, node2_complete
    )

    # Print results
    print("Node 1 to Node 2 Latencies (μs):")
    print(node1_to_node2_latencies)
    print("\nNode 2 to Node 1 Latencies (μs):")
    print(node2_to_node1_latencies)

if __name__ == "__main__":
    main()
