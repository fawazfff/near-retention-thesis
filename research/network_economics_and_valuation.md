# NEAR network economics and valuation workplan

**Status:** research framework, not a completed financial model. The current cohort CSV contains no fees, revenue, supply, staking or market-price observations.

## 0. Dated market, usage and revenue snapshot (14 November 2026)

CoinGecko showed NEAR around **$3.36**, market capitalization around **$4.40B**, fully diluted valuation around **$4.40B**, circulating supply around **1.312B NEAR**, and TVL around **$107.1M**. DeFiLlama's chain-level NEAR TVL was approximately **$125.08M**. These are much closer than the previously compared $276.2M figure: that larger DeFiLlama "NEAR Protocol (Combined)" figure aggregates assets across multiple chains, including roughly $110.31M on Ethereum. It is not a like-for-like NEAR-chain TVL denominator. The chain-only market-cap/TVL ratios are approximately **41×** using CoinGecko's TVL and **35×** using DeFiLlama's. Reconcile provider scope and token pricing timestamp before treating either as a valuation multiple.

DeFiLlama separately lists **NEAR Intents TVL of about $176.7M** as of 13 November. NEAR Intents operates across 26 chains, so its TVL is cross-chain collateral, not the same thing as NEAR-chain DeFi TVL. It may overlap with other protocol-level TVL aggregates and must not be added to them.

NEAR Intents processed approximately **$3.63B of DEX volume over 30 days**, generated **$5.83M of fees**, and captured about **$1.81M of protocol revenue**. The broader DeFiLlama NEAR Protocol view reported **$5.95M total fees**, **$1.93M protocol revenue** and **$1.81M holders revenue** over 30 days. Fees are gross charges, not the same as captured revenue. On these figures, captured protocol revenue is about **32.4% of gross fees**. The remaining fee amount should not be described as burned or retained by NEAR without checking the detailed fee split.

DeFiLlama describes NEAR Intents holders revenue as captured revenue used to buy back NEAR on the open market since 23 February 2026. This is **buyback-based holder value capture, not a token burn**. The 30-day $1.81M figure implies a simple annualized run rate of about **$21.7M**, or around **0.50% of a $4.38B market capitalization**. That is an arithmetic snapshot, not a guaranteed recurring yield. Confirm actual buyback transactions, amounts, dates and execution wallet flows before treating it as realized value accrual.

The trailing-year DeFiLlama figures were approximately **$54.14M fees** and **$9.64M protocol revenue**. At a roughly $4.376B market capitalization, the screening multiples are about **81× fees** and **454× protocol revenue**. These are high multiples relative to current captured economics. They do not prove NEAR is mispriced, but they mean a bullish valuation requires substantial durable revenue growth, broader value capture, or a defensible monetary premium beyond cash-flow multiples.

### Revenue growth hurdles, not price targets

At a constant $4.376B market capitalization:

| Market cap / annual revenue | Annual revenue required | Multiple of current $9.64M |
|---:|---:|---:|
| 100× | $43.8M | 4.5× |
| 50× | $87.5M | 9.1× |
| 25× | $175.0M | 18.2× |

These are arithmetic hurdles, not justified valuation multiples or price targets. They illustrate the scale of recurring revenue growth needed to reduce the current screening multiple.

The $3.63B of monthly Intents volume is **not revenue**. Gross swap volume can be large while the net amount retained by NEAR is much smaller. The current 30-day fee/revenue split and buyback series are more relevant than volume headlines, but a 12-month monthly history is still needed to assess durability, cyclicality and concentration.

Sources:
- [CoinGecko NEAR market data](https://www.coingecko.com/en/coins/near)
- [DeFiLlama NEAR Protocol combined TVL, fees and revenue](https://defillama.com/protocol/near-protocol)
- [DeFiLlama NEAR Intents TVL, volume, fees and revenue](https://defillama.com/protocol/near-intents)
- [DeFiLlama NEAR chain TVL](https://defillama.com/chains/NEAR)
- [DeFiLlama NEAR holders revenue](https://defillama.com/holders-revenue/chain/near)
- [NEAR Revenue dashboard](https://revenue.near.org/)
- [DeFiLlama fee adapter methodology](https://github.com/DefiLlama/dimension-adapters/blob/master/fees/near-intents/index.ts)

## 1. Protocol-level economics

Track these separately rather than treating all fees as token value accrual:

- Gross transaction fees paid by users, separated by base-layer gas and NEAR Intents/product fees.
- The developer gas rebate was removed under HSP-027 and protocol version 87, activated on 4 November 2026. Eligible execution gas that previously generated a 30% contract rebate is now fully burned. Confirm live protocol parameters and distinguish fee components before modelling.
- Validator issuance and treasury issuance.
- Net issuance = new tokens issued minus tokens burned. Report both NEAR and percentage of circulating supply.
- NEAR locked in storage and staked, with care not to count the same token twice.
- Validator gross staking yield and real yield after issuance dilution. Staking yield is not the same as protocol revenue.

### Does fee burn offset issuance?

A recent chain-data analysis measured about **88,000 NEAR issued per day** and about **890 NEAR burned per day** after protocol version 87 took effect on 4 November. That is only about **1.0% of daily issuance** offset by gas burn in the first eight days. At those observed rates, net issuance remains strongly positive. The sample is short and daily fees vary, so do not treat it as a forecast. It does show why “100% of eligible gas is burned” must not be confused with “NEAR is deflationary”: the burn base is currently small relative to issuance.

The same analysis estimated that even ten times the observed fee burn would offset only about 10% of issuance. The 2.5% maximum issuance setting therefore remains the dominant supply-side input until actual issuance changes or fee activity grows substantially.

Source: [Unlocks Insights, NEAR inflation and fee-burn analysis (13 November 2026)](https://insights.unlocks.app/near-halved-its-inflation-a-year-ago-the-chain-shows-the-cut-held/).

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
- DeFiLlama records a **$3.8M NEAR Intents exploit on 1 October 2026**. The 16 October postmortem revised the initial explanation: the root cause was a deposit-notification bug in the NEAR Intents contract, not an Omni bridge bug. Twenty-three deliberately failing deposit notifications created unbacked internal balances that were later withdrawn through cross-chain infrastructure. The team says all funds were returned on 2 October and affected users were made whole. The vulnerable notification feature was removed on 7 October after a second critical report. The incident appears financially recovered, but it exposed a contract-accounting and monitoring weakness. Treat it as an ecosystem product/security-control risk, not evidence of a NEAR base-layer consensus failure.

Incident sources: [NEAR Intents postmortem, 16 October 2026](https://x.com/AlexAuroraDev/status/2106049685928677585), [deposit-notification removal, near/intents PR #374](https://github.com/near/intents/pull/374), [DeFiLlama incident record](https://defillama.com/protocol/near-intents).

## 5. Required evidence before a valuation conclusion

1. Reproducible monthly supply/issuance/burn series from protocol data.
2. Verified product revenue with dates, source addresses and transaction hashes.
3. Staking participation and validator concentration series.
4. Application-level cohort and contract concentration analysis.
5. At least 12 months of comparable financial and market data.
6. Base, bull and bear cases with explicit growth, margin, dilution and token-capture assumptions.

Until those inputs are collected, the thesis should say **valuation not yet underwritten**, not cheap, expensive or undervalued.
