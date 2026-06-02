# Benchmark Ollama Tokens Per Second (TPS)

## Table of Contents

- [Installation](#installation)
- [Benchmark Script](#benchmark-script)
- [Sample Output](#sample-output)

---

## Installation

```bash
pip install ollama
```

---

## Benchmark Script

```python
from ollama import Client


def calculate_tokens_per_sec(response):
    """
    Calculate tokens per second from an Ollama generate response.

    Args:
        response (dict): The response dictionary from ollama.Client.generate.

    Returns:
        dict: A dict containing total_tokens, total_duration_sec, and tokens_per_second.
    """
    total_tokens = response.get("eval_count", 0)
    total_duration_ns = response.get("total_duration", 1)  # prevent division by zero

    total_duration_sec = total_duration_ns / 1e9

    tokens_per_sec = total_tokens / total_duration_sec if total_duration_sec > 0 else 0.0

    return {
        "total_tokens": total_tokens,
        "total_duration_sec": total_duration_sec,
        "tokens_per_second": tokens_per_sec,
    }


if __name__ == "__main__":
    client = Client("http://nginx-ollama:11434")
    tps_list = []

    for _ in range(5):
        response = client.generate(
            model="llama3.1:70b",
            prompt="what is the meaning of life?",
        )
        result = calculate_tokens_per_sec(response)
        print(
            f"Total Tokens: {result['total_tokens']}\t"
            f"Total Duration (seconds): {result['total_duration_sec']:.2f}\t"
            f"Tokens per Second: {result['tokens_per_second']:.2f}"
        )
        tps_list.append(result['tokens_per_second'])

    print("-" * 20)
    print(f"Average Token Per Second: {sum(tps_list) / len(tps_list):.2f}")
```

---

## Sample Output

```text
Total Tokens: 531   Total Duration (seconds): 24.75   Tokens per Second: 21.46
Total Tokens: 340   Total Duration (seconds): 11.29   Tokens per Second: 30.13
Total Tokens: 456   Total Duration (seconds): 15.16   Tokens per Second: 30.07
Total Tokens: 464   Total Duration (seconds): 15.47   Tokens per Second: 29.99
Total Tokens: 525   Total Duration (seconds): 17.44   Tokens per Second: 30.11
--------------------
Average Token Per Second: 28.35
```
