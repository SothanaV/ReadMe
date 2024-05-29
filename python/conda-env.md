# conda env
how to persistent environment on jupyterhub/lab
0. deactivate on base env
```
bash
conda deactivate
```
1. create env on path `~/work/conda-env/`
```
conda create -p ~/work/conda-env/<ENV_NAME> python=3.x
```
2. activate env using path
```
conda activate ~/work/conda/env/<ENV_NAME>
```
3. install ipykernel for use with jupyter
```
pip install jupyter
python -m ipykernel install --user --name  <ENV_ NAME> --display-name "Python (<ENV_NAME>)"
```