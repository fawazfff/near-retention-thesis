# NEAR network economics and valuation workplan

**Status:** research framework, not a completed financial model. The current cohort CSV contains no fees, revenue, supply, staking or market-price observations.

## 0. Dated market snapshot (14 November 2026)

CoinGecko's page snapshot showed approximately **$3.36 per NEAR**, **$4.40 billion market capitalization**, **$4.40 billion FDV**, **1.312 billion circulating NEAR**, **$107.1 million TVL**, and a **41.1× market-cap/TVL ratio**. The same page displayed roughly **$35.4k 24-hour fees** and **$30.4k 24-hour project revenue**.

These are third-party, time-sensitive snapshot figures, not independently reconciled protocol accounts. A single 24-hour revenue observation must not be multiplied by 365 and treated as sustainable annual revenue. Market-cap/TVL is a rough capital-efficiency screen, not a cash-flow valuation.

As of 14 November 2026, the active maximum annual issuance remains 2.5%. House of Stake proposal HSP-029 passed its vote on 2 November and proposes a linear 24-month reduction to 1.6%, but the Security Council veto window runs through 16 November and protocol implementation/validator adoption is still required. Do not model 1.6% as already active. NEAR's February 2026 tokenomics post describes product-revenue capture and buyback mechanisms; verify governance status, on-chain transfers and realized token amounts before treating buybacks or revenue capture as completed. A September 2026 SEC filing predates the November 4 rebate removal and therefore describes the previous 70% burn / 30% contract rebate. Do not use that older split as the current fee rule.

Sources:
- House of Stake HSP-029 proposal and status: https://gov.near.org/t/hsp-029-establish-a-24-month-issuance-ramp-to-a-1-6-target-rate-of-near-token-emissions/42644
- House of Stake HSP-027 ratification: https://houseofstake.org/blog/house-of-stake-update-hsp-027-ratified
- nearcore release notes (protocol version 87, removal of gas rewards): https://github.com/near/nearcore/releases
- NEAR Revenue dashboard: https://revenue.near.org/
- CoinGecko live market, TVL and financial data: https://www.coingecko.com/en/coins/near
- NEAR Foundation, *Evolving NEAR Tokenomics*, 24 February 2026: https://near.org/blog/evolving-near-tokenomics
- SEC filing, 16 September 2026: https://www.sec.gov/Archives/edgar/data/2067111/000119312526393240/ck0002067111-20260916.htm

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
