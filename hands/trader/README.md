# Trading Hand

Autonomous market intelligence and trading engine -- multi-signal analysis, adversarial bull/bear reasoning, calibrated confidence scoring, strict risk management, and portfolio-level analytics.

## Configuration

| Field | Value |
|-------|-------|
| Category | `data` |
| Agent | `trader-hand` |
| Routing | `trade`, `portfolio`, `market analysis`, `paper trade`, `stock trading` |

## Integrations

None required. Alpaca API keys needed for live trading mode.

## Settings

- **Trading Mode** -- `analysis` (signals only), `paper` (simulated), `live` (real via Alpaca)
- **Market Focus** -- `us_stocks`, `crypto`, `multi_asset`
- **Strategy Style** -- `scalping`, `day`, `swing`, `position`
- **Risk Per Trade** -- `1%`, `2%`, `3%`, `5%` of portfolio
- **Max Daily Loss** -- `2%`, `5%`, `10%` circuit breaker threshold
- **Analysis Depth** -- `quick`, `standard`, `deep`
- **Scan Schedule** -- `15m`, `1h`, `4h`, `daily`
- **Watchlist** -- Comma-separated tickers (default: `SPY,QQQ,AAPL,MSFT,NVDA,BTC,ETH`)
- **Initial Capital** -- Starting portfolio value (default: `$10,000`)
- **Approval Mode** -- Require approval before live trades (default: on)

## Usage

```bash
librefang hand run trader
```
