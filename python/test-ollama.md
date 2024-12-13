# Benchmark Ollama TPS(Token Per Second)

- install ollama
```sh
pip install ollama
```
- run python code client
```py
from ollama import Client

def calculate_tokens_per_sec(response):
    """
    Calculate tokens per second from the Ollama response.

    Args:
        response (dict): The response dictionary from Ollama's client.generate.

    Returns:
        float: Tokens per second.
    """
    # Extract necessary information
    total_tokens = response.get("eval_count", 0)
    total_duration_ns = response.get("total_duration", 1)  # Prevent division by zero
    
    # Convert nanoseconds to seconds
    total_duration_sec = total_duration_ns / 1e9
    
    # Calculate tokens per second
    if total_duration_sec > 0:
        tokens_per_sec = total_tokens / total_duration_sec
    else:
        tokens_per_sec = 0.0
    
    return {
        "total_tokens": total_tokens,
        "total_duration_sec": total_duration_sec,
        "tokens_per_second": tokens_per_sec
    }


# Example usage
if __name__ == "__main__":
    # Simulated response from client.generate
    client = Client("http://nginx-ollama:11434")
    tps = []
    for _ in range(5):
        response = client.generate(
            model="llama3.1:70b",
            prompt="what is meaning of life?"
        )

        # Calculate tokens per second
        result = calculate_tokens_per_sec(response)
        
        # Display the result
        print(f"Total Tokens: {result['total_tokens']}\tTotal Duration (seconds): {result['total_duration_sec']:.2f}\tTokens per Second: {result['tokens_per_second']:.2f}")
        tps.append(result['tokens_per_second'])
    print("-"*20)
    print(f"Average Token Per sec : {sum(tps)/len(tps):.2f}")
```