# NEAR network economics and valuation workplan

**Status:** research framework, not a completed financial model. The current cohort CSV contains no fees, revenue, supply, staking or market-price observations.

## 0. Dated market and revenue snapshot (14 November 2026)

CoinGecko showed NEAR around **$3.36**, **$4.40 billion market capitalization**, **$4.40 billion FDV**, **1.312 billion circulating NEAR**, **$107.1 million TVL**, and a **41.1× market-cap/TVL ratio**. DeFiLlama's NEAR Protocol page reported a materially different **$276.2 million TVL** on the same date. That implies a market-cap/TVL ratio closer to **15.9×**. The discrepancy likely reflects different protocol coverage or TVL definitions; it must be reconciled before using TVL in a valuation multiple. Do not choose the more attractive denominator without explaining it.

DeFiLlama reported approximately **$5.95 million fees** and **$1.93 million protocol revenue** over 30 days, and trailing-year annualized figures of **$54.14 million fees** and **$9.64 million revenue**. At a $4.376 billion market capitalization, that implies roughly **81× market-cap/trailing-year fees** and **454× market-cap/trailing-year revenue**. These are screening multiples, not a fair-value model. Product-level attribution, rebates, operator costs, and what reaches NEAR tokenholders must be checked. Do not treat gross cross-chain volume as revenue.

A single 24-hour fee or revenue observation must not be multiplied by 365 and treated as sustainable. The trailing-year figures are more useful, but still require a source reconciliation and a consistent definition of protocol revenue.

Sources:
- [CoinGecko NEAR market data](https://www.coingecko.com/en/coins/near)
- [DeFiLlama NEAR Protocol fees, revenue and TVL](https://defillama.com/protocol/near-protocol)
- [NEAR Revenue dashboard](https://revenue.near.org/)

## 0. Dated market and revenue snapshot (14 November 2026)

CoinGecko showed NEAR around **$3.36**, **$4.40 billion market capitalization**, **$4.40 billion FDV**, **1.312 billion circulating NEAR**, **$107.1 million TVL**, and a **41.1× market-cap/TVL ratio**. DeFiLlama's NEAR Protocol page reported a materially different **$276.2 million TVL** on the same date. That implies a market-cap/TVL ratio closer to **15.9×**. The discrepancy likely reflects different protocol coverage or TVL definitions; it must be reconciled before using TVL in a valuation multiple. Do not choose the more attractive denominator without explaining it.

DeFiLlama reported approximately **$5.95 million fees** and **$1.93 million protocol revenue** over 30 days, and trailing-year annualized figures of **$54.14 million fees** and **$9.64 million revenue**. At a $4.376 billion market capitalization, that implies roughly **81× market-cap/trailing-year fees** and **454× market-cap/trailing-year revenue**. These are screening multiples, not a fair-value model. Product-level attribution, rebates, operator costs, and what reaches NEAR tokenholders must be checked. Do not treat gross cross-chain volume as revenue.

A single 24-hour fee or revenue observation must not be multiplied by 365 and treated as sustainable. The trailing-year figures are more useful, but still require a source reconciliation and a consistent definition of protocol revenue.

Sources:
- [CoinGecko NEAR market data](https://www.coingecko.com/en/coins/near)
- [DeFiLlama NEAR Protocol fees, revenue and TVL](https://defillama.com/protocol/near-protocol)
- [NEAR Revenue dashboard](https://revenue.near.org/)

## 1. Protocol-level economics

Track these separately rather than treating all fees as token value accrual:

- Gross transaction fees paid by users, separated by base-layer gas and NEAR Intents/product fees.
- The developer gas rebate was removed under HSP-027 and protocol version 87, activated on 4 November 2026. Eligible execution gas that previously generated a 30% contract rebate is now fully burned. Confirm live protocol parameters and distinguish fee components before modelling.
- Validator issuance and treasury issuance.
- Net issuance = new tokens issued minus tokens burned. Report both NEAR and percentage of circulating supply.
- NEAR locked in storage and staked, with care not to count the same token twice.
- Validator gross staking yield and real yield after issuance dilution. Staking yield is not the same as protocol revenue.

## 2. Product and ecosystem economics

NEAR Intents and other products can generate revenue outside the base transaction-fee line. For each product, collect:
- Gross volume, number of settled transactions and unique counterparties.
- Fees collected, rebates/distributor share, operating costs and net revenue.
- Revenue actually converted into NEAR, used for buybacks, burned, staked or retained in treasury.
- Public evidence of recurring usage rather than one-off volume.

Do not add Intents volume to base-layer transaction volume as if both were revenue. Do not count announced buybacks as completed until transaction hashes and amounts are verified.

## 3. Valuation framework

Calculate on a common date:
- Market cap = spot price × circulating supply.
- FDV and fully diluted supply assumptions.
- Annualized protocol fees, product revenue and net revenue, each with source and time window.
- Market-cap / annualized revenue, market-cap / fees and market-cap / TVL. These are screening ratios, not standalone fair-value models.
- Net issuance yield = (issuance - burns - verified buybacks) / circulating supply.
- Revenue-to-token-holder capture = verifiable buybacks, burns, staking or other direct token mechanisms divided by product revenue. Keep indirect ecosystem benefits separate.

A high market-cap / revenue ratio requires substantial future growth to justify the price. A low ratio is not automatically cheap if revenue is temporary, subsidized or not captured by NEAR holders.

## 4. Risks and disconfirming evidence

- User activity may be incentive-driven, bot-driven, or concentrated in a few applications.
- Cross-chain volume may not translate into recurring NEAR-denominated revenue.
- Product revenue may accrue to operators or distribution partners rather than NEAR holders.
- Issuance can exceed fee burns and buybacks, diluting holders.
- Staking yield can be largely issuance-funded rather than organic cash flow.
- Application concentration, validator concentration, governance changes, bridge/custody risk, smart-contract exploits, regulatory restrictions, liquidity and token unlock/treasury sales can impair the thesis.
- Competitors may capture the same AI, chain-abstraction and cross-chain demand with stronger distribution or economics.

## 5. Required evidence before a valuation conclusion

1. Reproducible monthly supply/issuance/burn series from protocol data.
2. Verified product revenue with dates, source addresses and transaction hashes.
3. Staking participation and validator concentration series.
4. Application-level cohort and contract concentration analysis.
5. At least 12 months of comparable financial and market data.
6. Base, bull and bear cases with explicit growth, margin, dilution and token-capture assumptions.

Until those inputs are collected, the thesis should say **valuation not yet underwritten**, not cheap, expensive or undervalued.
