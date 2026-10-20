# Python Projects

[![CI](https://github.com/KriMaDev/python_projects/actions/workflows/ci.yml/badge.svg)](https://github.com/KriMaDev/python_projects/actions/workflows/ci.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Practical Python tools I built while learning Python. Each one is small and self-contained,
does one useful job from the command line, and has its own README with setup steps and example output.

| Tool | What it does | Main libraries |
|---|---|---|
| [Crypto_Prices](Crypto_Prices/) | Live crypto prices in the terminal, green/red when they go up/down | requests, colorama, keyboard |
| [Idle_Fighter](Idle_Fighter/) | Text-based auto battler: pick a class and fight a boss (my first OOP project) | standard library only |
| [Network_Scanner](Network_Scanner/) | Find devices on your LAN, look up IP owners and VPNs, identify MAC vendors | scapy, ipwhois, requests |
| [Pdf_Merger](Pdf_Merger/) | Merge all PDFs in a folder into one file | pypdf, colorama |
| [Weather_Forecast](Weather_Forecast/) | Compare current weather and hourly forecasts from three weather APIs | requests, python-dotenv, colorama |

## Setup

You need **Python 3.10 or newer** and Git.

```bash
git clone https://github.com/KriMaDev/python_projects.git
cd python_projects

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell / cmd)
source .venv/bin/activate       # macOS / Linux

# Install everything (all tools, pytest and ruff) ...
pip install -r requirements-dev.txt
# ... or only what one tool needs
pip install -r Pdf_Merger/requirements.txt
```

**API keys (only for Weather_Forecast).** Copy `Weather_Forecast/.env.example` to `Weather_Forecast/.env`
and add your free keys. `.env` is ignored by Git, so keys never end up in the repository. See the
[Weather_Forecast README](Weather_Forecast/README.md#setup) for where to get the keys.

## Running the tools

Run everything from the repository root. Every script has `--help`. Scripts that ask questions also accept
the answers as arguments.

| Script | Example | Notes |
|---|---|---|
| `Crypto_Prices/cr_pr.py` | `python Crypto_Prices/cr_pr.py --coins bitcoin,solana` | Stop with `esc` or `Ctrl+C` |
| `Crypto_Prices/coin_list.py` | `python Crypto_Prices/coin_list.py --search solana` | Finds the coin IDs for `cr_pr.py` |
| `Idle_Fighter/main.py` | `python Idle_Fighter/main.py --class tank` | Asks for a class if omitted |
| `Network_Scanner/scan_network.py` | `python Network_Scanner/scan_network.py` | Admin/root, Npcap on Windows, [your own network only](Network_Scanner/README.md) |
| `Network_Scanner/check_ip.py` | `python Network_Scanner/check_ip.py 8.8.8.8` | Asks for an IP if omitted |
| `Network_Scanner/check_mac.py` | `python Network_Scanner/check_mac.py 00:1A:2B:3C:4D:5E` | Shows a menu if omitted |
| `Pdf_Merger/merge_pdf.py` | `python Pdf_Merger/merge_pdf.py ./scans -o merged.pdf` | Defaults to the current folder |
| `Weather_Forecast/weather.py` | `python Weather_Forecast/weather.py Brussels --hourly` | Needs API keys in `.env` |

## Tests and code quality

```bash
pytest          # unit tests for the pure functions of every tool (no network or API keys needed)
ruff check .    # linting and import order
```

Both run automatically on every push through [GitHub Actions](.github/workflows/ci.yml) on Python 3.10 and 3.13.

## Project structure

```text
python_projects/
├── Crypto_Prices/        each tool: scripts + README.md + requirements.txt
├── Idle_Fighter/
├── Network_Scanner/
├── Pdf_Merger/
├── Weather_Forecast/     also .env.example
├── tests/                pytest tests, one file per tool
├── .github/workflows/    CI: ruff + pytest
├── pyproject.toml        ruff and pytest settings
└── requirements-dev.txt  all tool dependencies + pytest + ruff
```

## About AI-assisted development

These tools started as my own learning projects. My newer projects are built with AI-assisted development
using [Claude Code](https://claude.com/claude-code), and I used it for this repository's clean-up too
(tests, CI, documentation and refactoring). I review, run and understand every change before it goes in.

## License

My code in this repository is under the [MIT License](LICENSE). Third-party libraries keep their own
licences, listed in each tool's README. Scapy, used by Network_Scanner, is GPL-2.0.
