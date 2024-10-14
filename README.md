# OpenAI Client Example

## Description

This repository contains examples for interacting with LLMs deployed via llama.cpp (or any other OpenAI API-compatible runtime) using the OpenAI Python library.

Ansible playbooks for setting up llama.cpp on IBM Power (ppc64le) can be found here: [DahlitzFlorian/ai-on-ibm-power-playbooks](https://github.com/DahlitzFlorian/ai-on-ibm-power-playbooks?tab=readme-ov-file)


## Usage

Create a virtual environment, install the dependencies, and start the desired script.
Make sure to adjust the config-file in the `src` directory before running any scripts.

```shell
python -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt

python src/basic_example.py --config-path src/example_config.ini
```


### Command-line parameters

- `--config-file` (_Path_, default: `src/config.ini`): Path to the configuration file.
- `--max-tokens` (_int_, default: `300`): Maximum number of tokens to predict
- `--prompt-file` (_Path_, default: `None`): Path to a file reading the prompt from (otherwise script asks for input)
- `--timeout` (_float_, default: `300.0`): Timeout in seconds
