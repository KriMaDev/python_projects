# Crypto Prices

Live cryptocurrency prices in the terminal, from the free [CoinGecko API](https://www.coingecko.com/en/api).
Every update shows whether a coin went up (green ↑), down (red ↓) or stayed the same (white -).

| Script | What it does |
|---|---|
| `cr_pr.py` | Prints the USD price of a list of coins every 15 seconds until you press `esc` |
| `coin_list.py` | Prints every coin CoinGecko knows, with the ID you pass to `cr_pr.py --coins` |

No API key is needed.

## Setup

From the repository root, with your virtual environment active (see the [main README](../README.md#setup)):

```bash
pip install -r Crypto_Prices/requirements.txt
```

## cr_pr.py: live prices

```bash
python Crypto_Prices/cr_pr.py                                   # default coins, every 15 s
python Crypto_Prices/cr_pr.py --coins bitcoin,solana,dogecoin   # your own coins
python Crypto_Prices/cr_pr.py --interval 60                     # update every minute
python Crypto_Prices/cr_pr.py --help
```

| Option | Default | Meaning |
|---|---|---|
| `--coins` | `bitcoin,ethereum,crypto-com-chain,pepe,pax-gold` | Comma separated CoinGecko **IDs** (not symbols, see `coin_list.py`) |
| `--interval` | `15` | Seconds between updates. The free API allows roughly 5–15 calls per minute |

Press **`esc`** or **`Ctrl+C`** to stop.

> The `esc` listener uses the [`keyboard`](https://github.com/boppreh/keyboard) package. On Linux it needs root
> and on macOS the terminal needs Accessibility permission. Without those, use `Ctrl+C`.

Example output:

```text
To exit the program please press 'esc' (or Ctrl+C)
Coins: bitcoin, ethereum, crypto-com-chain, pepe, pax-gold

| 20/10/2026 12:20:57 | - | Bitcoin          : $81528.00
| 20/10/2026 12:20:57 | - | Ethereum         : $2386.20
| 20/10/2026 12:20:57 | - | Crypto-com-chain : $0.05645300
| 20/10/2026 12:20:57 | - | Pepe             : $0.00000417
| 20/10/2026 12:20:57 | - | Pax-gold         : $4114.62
...
```

The first update always shows `-`. From the second update on, each line is green with `↑` if the price rose,
red with `↓` if it fell, and white with `-` if it didn't change. Prices below $1 are shown with 8 decimals so
small coins like Pepe stay readable.

## coin_list.py: find coin IDs

```bash
python Crypto_Prices/coin_list.py                     # all coins (up to 9001 lines)
python Crypto_Prices/coin_list.py --search solana     # only matching symbol, ID or name
python Crypto_Prices/coin_list.py --limit 50          # first 50 coins
```

Example output:

```text
Attempting to fetch coin list...
Number               Symbol               ID                                                           Name
============================================================================================================================================
1                    apax                 apa-xstock                                                   APA xStock
2                    paxg                 pax-gold                                                     PAX Gold
3                    paxgy                paxgy                                                        PAXGy
```

Use the value in the **ID** column with `cr_pr.py --coins`.

## Libraries

| Package | Used for | Licence |
|---|---|---|
| [requests](https://pypi.org/project/requests/) | HTTP calls to CoinGecko | Apache-2.0 |
| [colorama](https://pypi.org/project/colorama/) | Coloured output on Windows | BSD-3-Clause |
| [keyboard](https://pypi.org/project/keyboard/) | Listening for the `esc` key | MIT |

Price data provided by [CoinGecko](https://www.coingecko.com/).
