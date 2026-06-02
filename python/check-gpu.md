# Check GPU with PyTorch

## Table of Contents

- [Installation](#installation)
- [Quick GPU Check](#quick-gpu-check)
- [Extended Load Test](#extended-load-test)

---

## Installation

Install PyTorch with CUDA 12.1 support:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

---

## Quick GPU Check

Verify CUDA availability and run a basic matrix multiplication on the GPU:

```python
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU count:", torch.cuda.device_count())
    print("Current device index:", torch.cuda.current_device())
    print("Current device name:", torch.cuda.get_device_name(torch.cuda.current_device()))

    # Basic GPU computation test
    x = torch.randn(5000, 5000, device="cuda")
    y = torch.randn(5000, 5000, device="cuda")
    z = x @ y  # matrix multiply on GPU
    print("Result shape:", z.shape)
    print("Sum:", z.sum().item())
else:
    print("No CUDA GPU detected by PyTorch")
```

---

## Extended Load Test

Run a sustained load test to stress the GPU over many iterations:

```python
import torch
from tqdm.auto import tqdm
import time

for i in tqdm(range(100_000_000)):
    x = torch.randn(5000, 5000, device="cuda")
    y = torch.randn(5000, 5000, device="cuda")
    z = x @ y  # matrix multiply on GPU
    time.sleep(0.1)
```
