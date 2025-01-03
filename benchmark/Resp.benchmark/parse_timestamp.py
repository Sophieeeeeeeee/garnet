import re
import statistics

# A function to convert tick timestamps into nanoseconds (assuming tick is 100ns)
def convert_ticks_to_ns(tick):
    return tick  # 1 tick = 100 nanoseconds

# Parsing the log to extract the timestamp and event
def parse_log(file_path, data):
    log_pattern = re.compile(r'\[(.*?)\] \((.*?)\) <(.*?)> (\w+) from (\d+\.\d+\.\d+\.\d+:\d+) at tick (\d+)')
    c = 0
    with open(file_path, 'r') as file:
        for line in file:
            # Parse each line for relevant event and timestamp
            match = log_pattern.match(line.strip())
            if match:
                timestamp = match.group(1)       # Extract timestamp
                log_level = match.group(2)       # Extract log level (e.g., Debug, Information)
                component = match.group(3)       # Extract component (e.g., GarnetServer)
                event_type = match.group(4)      # Extract event type (e.g., OnNetworkReceive)
                ip_and_port = match.group(5)     # Extract IP and port (e.g., 128.105.145.127:38280)
                clock_tick = match.group(6)      # Extract clock tick (e.g., 111296871)
                
                # Print the extracted information in the desired format
                # print(f"Event Type: {event_type}, IP and Port: {ip_and_port}, at Tick: {clock_tick}")

                if ip_and_port not in data:
                    data[ip_and_port] = {}
                    data[ip_and_port]["OnNetworkReceive"] = []
                    data[ip_and_port]["TryProcessRequest"] = []
                    data[ip_and_port]["SendResponse"] = []
                    data[ip_and_port]["SeaaBuffer_Completed"] = []
                    
                data[ip_and_port][event_type].append(clock_tick)
                c += 1
            if c == 4000000: 
                break
        
        for client in data.keys():
            print(client)
            for event in data[client].keys():
                print(f"event: {event}, len: {len(data[client][event])}")

# Calculate the process_set_duration and full_duration for each request
def calculate_durations(request_data, full_duration, process_set_duration):
    count = len(request_data["OnNetworkReceive"])

    for i in range(count):
        on_network_receive_tick = int(request_data['OnNetworkReceive'][i])
        seaa_buffer_completed_tick = int(request_data['SeaaBuffer_Completed'][i])
        full = abs(seaa_buffer_completed_tick - on_network_receive_tick)
        full_duration.append(convert_ticks_to_ns(full))

        send_response_tick = int(request_data['SendResponse'][i])
        try_process_request_tick = int(request_data['TryProcessRequest'][i])
        process = abs(send_response_tick - try_process_request_tick)
        process_set_duration.append(convert_ticks_to_ns(process))


# Calculate the averages
def calculate_averages(process_set_durations, full_durations):
    avg_process_set_duration = statistics.mean(process_set_durations) if process_set_durations else 0
    avg_full_duration = statistics.mean(full_durations) if full_durations else 0
    return avg_process_set_duration, avg_full_duration

# File path
file_path = 'timestamp.txt'

# Parsing logs
data = {}
parse_log(file_path, data)

# Calculate durations
process_set_durations = {}
full_durations = {}
for port in data.keys():
    process_set_durations[port] = []
    full_durations[port] = []
    calculate_durations(data[port], full_durations[port], process_set_durations[port])

# print(full_durations)
# print(process_set_durations)

# Calculate averages
avg_process_set_durations = {}
avg_full_durations = {}
for port in data.keys():
    avg_process_set_durations[port], avg_full_durations[port] = calculate_averages(process_set_durations[port], full_durations[port])

# Print the results
for port in data.keys():
    print(f"client:{port}")
    print(f"Process Set Duration (average): {avg_process_set_durations[port]} ns")
    print(f"Full Duration (average): {avg_full_durations[port]} ns")
