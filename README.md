# Crash August 2023 Analysis

Could we use Crypto News Sentiment to foresee the recent BTC melt?

## Pre-requisites

- conda-like environment manager (e.g. [miniconda](https://docs.conda.io/en/latest/miniconda.html))
- `.env` file with 


## Setup environment

Inside of the project folder:

```bash
# create environment
conda env create --file config_files/local_environment.yml

# activate environment
conda activate crash-aug23-analysis

# pip install
pip install -r config_files/requirements.txt
```

## Run notebooks

```bash
# activate environment
conda activate crash-aug23-analysis
```
### Daily Data Analysis

```bash
# run notebooks
jupyter notebook notebooks/analysis_daily_data.ipynb
```

### 15-min Data Analysis

```bash
# run notebooks
jupyter notebook notebooks/analysis_15min_data.ipynb
```

## Binder viewer

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/trading-smart/crash-aug23-analysis/HEAD)
