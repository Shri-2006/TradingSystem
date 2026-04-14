#!/bin/bash
# Install main dependencies
pip install -r requirements.txt

# Install alpaca separately after — it downgrades websockets but polygon works anyway
pip install alpaca-trade-api==3.0.0

# Restore websockets for polygon
pip install "websockets>=14.0"
