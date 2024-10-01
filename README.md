# OpenAI Client Example

## Description

This repository contains examples for interacting with LLMs deployed via llama.cpp (or any other OpenAI API-compatible runtime) using the OpenAI Python library.

Ansible playbooks for setting up llama.cpp on IBM Power (ppc64le) can be found here: [DahlitzFlorian/ai-on-ibm-power-playbooks](https://github.com/DahlitzFlorian/ai-on-ibm-power-playbooks?tab=readme-ov-file)


## Usage

Create a virtual environment, install the dependencies, and start the desired script.

```shell
python -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

python src/basic_example.py
```
