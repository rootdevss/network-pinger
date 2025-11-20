# Network Pinger
High-performance ICMP network pinger written in Python using asyncio

## Features
- Ping multiple hosts simultaneously
- Measures round-trip time (RTT) in milliseconds
- Works on Linux with root privileges
- Async and non-blocking for high performance

## Requirements
- Python 3.7+
- Linux (root) or WSL for raw socket access

## Installation
Clone the repository:
git clone https://github.com/rootdevss/network-pinger.git
cd network-pinger
Install dependencies (if any, currently none required):
pip install -r requirements.txt

## Usage
Run the pinger:
sudo python3 pinger.py
You can edit the `hosts` list in `pinger.py` to ping your desired IPs

## License
MIT License
