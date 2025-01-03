import re

# Function to parse the client_dump.txt file
def parse_client_dump(file_path):
    send_events = []
    receive_events = []
    
    # Regular expression to match the relevant lines
    send_pattern = re.compile(r'Sending SET at (\d+) tick at (\d+) microsec')
    receive_pattern = re.compile(r'Received SET at (\d+) tick at (\d+) microsec')

    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Match "Sending" events
            send_match = send_pattern.match(line)
            if send_match:
                tick = int(send_match.group(1))
                send_events.append(tick)

            # Match "Received" events
            receive_match = receive_pattern.match(line)
            if receive_match:
                tick = int(receive_match.group(1))
                receive_events.append(tick)

    return send_events, receive_events

# Function to calculate the duration between sending and receiving events
def calculate_durations(send_events, receive_events):
    durations = []
    
    # Assuming that the events are in order and pair correctly
    for send, receive in zip(send_events, receive_events):
        duration = receive - send
        durations.append(duration)

    return durations


def convert_ticks_to_ns(tick):
    return tick  # 1 tick = 100 nanoseconds


# Main function to parse and process the log file
def main():
    # Specify the path to the client_dump.txt file
    file_path = 'client_dump.txt'

    # Parse the log file for send and receive events
    send_events, receive_events = parse_client_dump(file_path)
    
    # Print parsed events
    print(f"len send events: {len(send_events)}")
    print(f"len receive events: {len(receive_events)}")
    
    # Calculate and print the durations (in microseconds)
    durations = calculate_durations(send_events, receive_events)
    print(f"\nlen durations: {len(durations)}")
    
    # Calculate the average duration
    avg_duration = sum(durations) / len(durations) if durations else 0
    print(f"\nAverage Duration: {avg_duration:.2f} tick(nanosec)")
    print(f"\nAverage Duration: {avg_duration/1000:.2f} microsec")

# Run the main function
if __name__ == '__main__':
    main()
