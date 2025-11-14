# Check GPU
- install pytorch
```
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

- test
```py
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())


if torch.cuda.is_available():
    print("GPU count:", torch.cuda.device_count())
    print("Current device index:", torch.cuda.current_device())
    print("Current device name:", torch.cuda.get_device_name(torch.cuda.current_device()))

    # small GPU computation test
    x = torch.randn(5000, 5000, device="cuda")
    y = torch.randn(5000, 5000, device="cuda")
    z = x @ y  # matrix multiply on GPU
    print("Result shape:", z.shape)
    print("Sum:", z.sum().item())
else:
    print("No CUDA GPU detected by PyTorch")
```

- long test
```py
import torch
from tqdm.auto import tqdm
import time

for i in tqdm(range(100_000_000)):
    x = torch.randn(5000, 5000, device="cuda")
    y = torch.randn(5000, 5000, device="cuda")
    z = x @ y  # matrix multiply on GPU
    time.sleep(0.1)
```