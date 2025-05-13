import asyncio
import aiohttp
import requests
import time
import threading
from threading import Event
import re
import nest_asyncio
import random
import pandas 
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration
OLLAMA_URL = "http://10.16.2.10:11434/api/generate"  # Adjust to your Ollama server address
DCGM_EXPORTER_URL = "http://10.16.2.10:9400/metrics"    # Adjust to your GPU server address
PROMPT = "This is a test prompt for the load test."     # Fixed prompt for consistency
NUM_CONCURRENT_REQUESTS = 50                            # Number of concurrent requests
MODEL = "llama3.3:latest"                               # Specify your Ollama model (e.g., "llama2")
fb_total_mib = 80 * 1024

# Function to collect GPU metrics in a background thread
def collect_gpu_metrics():
    """Collects GPU utilization and memory usage from DCGM Exporter every second."""
    while not stop_event.is_set():
        try:
            response = requests.get(DCGM_EXPORTER_URL, timeout=5)
            if response.status_code == 200:
                metrics_text = response.text
                gpu_utils = []
                mem_utils = []
                fb_total = 16 * 1024 * 1024  # Assume 16 GB total memory in KB; adjust as needed
                for line in metrics_text.splitlines():
                    # Parse GPU utilization
                    if line.startswith("DCGM_FI_DEV_GPU_UTIL"):
                        match = re.search(r'gpu="(\d+)"}\s+(\d+)', line)
                        if match:
                            gpu_utils.append(int(match.group(2)))
                    # Parse memory usage
                    elif line.startswith("DCGM_FI_DEV_FB_USED"):
                        match = re.search(r'gpu="(\d+)"}\s+(\d+)', line)
                        if match:
                            fb_used = int(match.group(2))
                            mem_util = (fb_used / fb_total_mib) * 100
                            mem_utils.append(mem_util)
                print(f"gpu_utils : {gpu_utils}")
                print(f"mem_utils : {mem_utils}")
                if gpu_utils and mem_utils:
                    avg_gpu_util = sum(gpu_utils) / len(gpu_utils)
                    avg_mem_util = sum(mem_utils) / len(mem_utils)
                    _data = {
                        'timestamp': time.time(),
                        'avg_gpu_util': avg_gpu_util,
                        'avg_mem_util': avg_mem_util
                    }
                    print(_data)
                    gpu_metrics.append(_data)
        except Exception as e:
            print(f"Error fetching GPU metrics: {e}")
        time.sleep(0.01)  # Collect metrics every second

# Async function to send a single request to Ollama
async def send_request(session):
    """Sends a request to Ollama and records timing and token data."""
    start_time = time.time()
    payload = {"model": MODEL, "prompt": PROMPT, "stream": False}
    try:
        async with session.post(OLLAMA_URL, json=payload, timeout=aiohttp.ClientTimeout(total=300)) as response:
            data = await response.json()
        end_time = time.time()
        processing_time = end_time - start_time
        input_tokens = data.get("prompt_eval_count", 0)  # Number of input tokens
        output_tokens = data.get("eval_count", 0)        # Number of output tokens
        _data = {
            'start_time': start_time,
            'end_time': end_time,
            'processing_time': processing_time,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        }
        [_data.update({k:v}) for k,v in data.items() if k in ['total_duration', 'prompt_eval_duration', 'eval_duration', 'prompt_eval_count', 'eval_count', 'load_duration']]
        
        requests_data.append(_data)
    except Exception as e:
        print(f"Request failed: {e}")

# Main function to run the load test
async def run_load_test():
    """Runs the load test by sending concurrent requests to Ollama."""
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(NUM_CONCURRENT_REQUESTS)]
        await asyncio.gather(*tasks)

# Data storage
requests_data = []  # Stores per-request data
gpu_metrics = []    # Stores GPU metrics over time
stop_event = Event()  # Signal to stop metrics collection
# Start GPU metrics collection
print("Starting GPU metrics collection...")
metrics_thread = threading.Thread(target=collect_gpu_metrics)
metrics_thread.start()

# Run the load test
print(f"Starting load test with {NUM_CONCURRENT_REQUESTS} concurrent requests...")

# asyncio.run(run_load_test())

nest_asyncio.apply()  # Allow nested event loops

await run_load_test()

# Stop GPU metrics collection
print("Stopping GPU metrics collection...")
stop_event.set()
metrics_thread.join()

# Process and display results
if requests_data and gpu_metrics:
    # Calculate total duration of the load test
    start_time = min(r['start_time'] for r in requests_data)
    end_time = max(r['end_time'] for r in requests_data)
    total_duration = end_time - start_time

    # Calculate queries per second (QPS)
    num_requests = len(requests_data)
    qps = num_requests / total_duration

    # Calculate average processing time
    avg_processing_time = sum(r['processing_time'] for r in requests_data) / num_requests

    # Calculate total input and output tokens
    total_input_tokens = sum(r['input_tokens'] for r in requests_data)
    total_output_tokens = sum(r['output_tokens'] for r in requests_data)
    avg_input_tokens = total_input_tokens / num_requests  # Average per request
    avg_output_tokens = total_output_tokens / num_requests

    # Calculate average GPU metrics
    avg_gpu_util = sum(m['avg_gpu_util'] for m in gpu_metrics) / len(gpu_metrics)
    avg_mem_util = sum(m['avg_mem_util'] for m in gpu_metrics) / len(gpu_metrics)

    # Display results in a table-like format
    print("\n### Load Test Results ###")
    print("#### Input Parameters")
    print(f"- **Input query tokens per request**: {avg_input_tokens:.2f}")
    print(f"- **Number of requests per second**: {qps:.2f}")

    print("#### Process")
    print(f"- **LLM processing time**: {avg_processing_time:.2f} seconds")
    print(f"- **Average GPU core utilization**: {avg_gpu_util:.2f}%")
    print(f"- **Average GPU memory utilization**: {avg_mem_util:.2f}%")

    print("#### Output Parameters")
    print(f"- **Output tokens per request**: {avg_output_tokens:.2f}")

    print(f"\nTotal duration: {total_duration:.2f} seconds")
    print(f"Total requests: {num_requests}")
else:
    print("No data collected. Check server availability and configuration.")

df = pd.DataFrame(requests_data)

df['prompt_eval_duration'] = df['prompt_eval_duration']/1e9
df['eval_duration'] = df['eval_duration']/1e9
df['total_duration'] = df['total_duration']/1e9

plt.figure(figsize=(12,8))
g = sns.pairplot(
    df[['total_duration','input_tokens', 'output_tokens']]
)
for ax in g.axes.flatten():
    ax.grid(True)
plt.show()