# krejcarek-jidlo-bot
Python script for sending webhooks to Slack with current food menu at Krejcárek

## Requirements

* Python 3
* Pip packages from requirements.txt

## Installation

* `pip install -r requirements.txt`

## Usage

* Rename `config.py.example` to `config.py` and enter a Slack webhook url in the `webhookEndpoint` variable 
* Run `python run.py` to receive today's food menu in a Slack channel
