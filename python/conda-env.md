# Conda Environment for JupyterHub / JupyterLab

How to create a persistent conda environment on JupyterHub or JupyterLab so the kernel survives server restarts.

## Table of Contents

- [Steps](#steps)

---

## Steps

### 0. Deactivate the Base Environment

```bash
conda deactivate
```

### 1. Create the Environment at a Persistent Path

Store the environment under `~/work/` so it is not lost when the server pod restarts:

```bash
conda create -p ~/work/conda-env/<ENV_NAME> python=3.x
```

### 2. Activate the Environment by Path

```bash
conda activate ~/work/conda-env/<ENV_NAME>
```

### 3. Install ipykernel and Register the Kernel

```bash
pip install jupyter
python -m ipykernel install --user --name <ENV_NAME> --display-name "Python (<ENV_NAME>)"
```

After registration the kernel will appear in the JupyterLab launcher and will persist across sessions.
