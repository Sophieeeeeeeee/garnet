import os
import matplotlib.pyplot as plt
import subprocess
import re

# Function to run the benchmarking command and capture the output
def run_benchmark(command):
    try:
        # Run the command and capture output
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return output.stdout
        # return result.stdout
    except Exception as e:
        print(f"Error running benchmark: {e}")
        return None

# Function to parse throughput from the benchmark output
def parse_throughput(file_names):
    throughput = []
    
    for file_name in file_names:
        # Use regular expressions to find the relevant data in the output
        with open(file_name, 'r') as file:
            output = file.read()
            rows = output.splitlines()[1:]
            line = rows[-1]
            parts = line.split()
            tpt = float(parts[-1])  # Extracting the throughput from the last column
            throughput.append(tpt)
                    
    return throughput


# Function to parse throughput from the benchmark output
def parse_latency(file_names):
    latencies = []
    
    for file_name in file_names:
        # Use regular expressions to find the relevant data in the output
        with open(file_name, 'r') as file:
            output = file.read()
            rows = output.splitlines()[1:]
            line = rows[-1]
            parts = line.split()
            latency = float(parts[9])  # Extracting the throughput from the last column
            latencies.append(latency)
                    
    return latencies


# Function to generate the bar chart
def generate_chart_throughput(x_list, throughput, config_info, graph_var, op, prefix=""):
    # Convert threads to string labels for the x-axis (categorical)
    x_labels = [str(x) for x in x_list]

    # Create bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_labels, throughput, color='skyblue')  # Use thread_labels for categorical x-axis

    # Add titles and labels
    plt.title(f'Throughput vs {graph_var}', fontsize=16)
    plt.xlabel(f'Number of {graph_var}', fontsize=12)
    plt.ylabel('Throughput (Kops/sec)', fontsize=12)

    # Add the actual throughput labels on top of each bar
    for bar, tpt in zip(bars, throughput):
        yval = bar.get_height()  # Get the height of the bar (which is the throughput value)
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{tpt:.2f}', ha='center', va='bottom')  # Add label

    # Add configuration information at the top of the graph
    plt.text(0.5, 0.95, config_info, fontsize=10, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Save the figure as an image
    plt.savefig(f"{prefix}throughput_vs_{graph_var}_{op}.png")
    print(f"Chart created and saved as 'throughput_vs_{graph_var}_{op}.png'!")

# Function to generate the bar chart
def generate_chart_latency(x_list, latencies, config_info, graph_var, op, prefix=""):
    # Convert threads to string labels for the x-axis (categorical)
    x_labels = [str(x) for x in x_list]

    # Create bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_labels, latencies, color='skyblue')  # Use thread_labels for categorical x-axis

    # Add titles and labels
    plt.title(f'Latency at 99 percentile vs {graph_var}', fontsize=16)
    plt.xlabel(f'Number of {graph_var}', fontsize=12)
    plt.ylabel('Latencies (microsec)', fontsize=12)

    # Add the actual throughput labels on top of each bar
    for bar, latency in zip(bars, latencies):
        yval = bar.get_height()  # Get the height of the bar (which is the throughput value)
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{latency:.2f}', ha='center', va='bottom')  # Add label

    # Add configuration information at the top of the graph
    plt.text(0.5, 0.95, config_info, fontsize=10, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Save the figure as an image
    plt.savefig(f"{prefix}latency_vs_{graph_var}_{op}.png")
    print(f"Chart created and saved as 'latency_vs_{graph_var}_{op}.png'!")



def main(): 
    # Configuration variables
    operation = ["SET","GET"]
    op = "SET"
    operation_percent = "100"
    keylength = 8
    valuelength = 8
    dbsize = 16777216 
    dbsize_mb = 16128
    host = "128.105.145.123"
    port = 6379
    file_name = "client_stats.txt"

    benchmark_command = f"dotnet run -c Release -f net8.0 -- --online " \
                        f"--op-workload {op} --op-percent {operation_percent} "\
                        f"--host {host} --port {port} " \
                        f"--dbsize {dbsize} --keylength {keylength} --valuelength {valuelength} " \
                        f"--itp {1} " \
                        f"--batchsize {1} " \
                        f"--threads {1} " \
                        f"--file-logger {file_name}"
    
    output = run_benchmark(benchmark_command)
    print(output)


    # for op in operation: 
    #     # # batch size 
    #     batch_list = [1, 4, 16, 64, 256, 1024, 2048, 4096]  # Convert to a list of integers
    #     print(batch_list)
    #     file_names = [f"large_val_itp_{op}_{x}.txt" for x in batch_list]
    #     # # Benchmark command (you can modify this)
    #     n = len(batch_list)

        # for i in range(n):
        #     # Remove the existing log file to start fresh
        #     if os.path.exists(file_names[i]):
        #         os.remove(file_names[i])
        #         print(f"{file_names[i]} has been deleted to start fresh.")
            
        #     benchmark_command = f"dotnet run -c Release -f net8.0 -- --online " \
        #                         f"--op-workload {op} --op-percent {operation_percent} "\
        #                         f"--host {host} --port {port} " \
        #                         f"--dbsize {dbsize} --keylength {keylength} --valuelength {valuelength} " \
        #                         f"--threads {40} " \
        #                         f"--itp {batch_list[i]} " \
        #                         f"--file-logger {file_names[i]}"

        #     output = run_benchmark(benchmark_command)


        # threads 
        # threads_list = [1, 2, 4, 8, 16, 32, 40, 64, 128]  # Convert to a list of integers
        # print(threads_list)
        # file_names = [f"large_val_threads_{op}_{x}.txt" for x in threads_list]
        # # Benchmark command (you can modify this)
        # n = len(threads_list)

        # for i in range(n):
        #     if os.path.exists(file_names[i]):
        #         os.remove(file_names[i])
        #         print(f"{file_names[i]} has been deleted to start fresh.")

        #     benchmark_command = f"dotnet run -c Release -f net8.0 -- --online " \
        #                         f"--op-workload {op} --op-percent {operation_percent} "\
        #                         f"--host {host} --port {port} " \
        #                         f"--dbsize {dbsize} --keylength {keylength} --valuelength {valuelength} " \
        #                         f"--threads {threads_list[i]} " \
        #                         f"--file-logger {file_names[i]}"
            
        #     output = run_benchmark(benchmark_command)
        #     print(output)


        # config_info = f"""
        #                 Benchmark Configuration:
        #                 - Operation: {op}
        #                 - KeyLength: {keylength}
        #                 - ValueLength: {valuelength}
        #                 - DBsize in MB: {dbsize_mb}
        #                 - itp(batchsize default): {1}
        #                 """
        #             # - Threads: {40}

        # throughput = parse_throughput(file_names)
        # generate_chart_throughput(batch_list, throughput, config_info, "itp_set_to_batchsize", op, prefix="large_val_")
        # latencies = parse_latency(file_names)
        # generate_chart_latency(batch_list, latencies, config_info, "itp_set_to_batchsize", op, prefix="large_val_")

        # throughput = parse_throughput(file_names)
        # print(throughput)
        # generate_chart_throughput(threads_list, throughput, config_info, "threads", op, prefix="large_val_")
        # latencies = parse_latency(file_names)
        # print(latencies)
        # generate_chart_latency(threads_list, latencies, config_info, "threads", op, prefix="large_val_")
        

if __name__ == '__main__':
    main()
