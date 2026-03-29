# Decision Log to keep track of what I was thinking while building

## March 28, 2026-Configuration of the system and allocation of the money and where to invest
**CONTEXT**: 

Began building the program. Created structure of the overall project, wrote config.py, readme, core folder, requirements.txt and gitignore and logger.py

Options 1: Don't put env in gitignore or put it in
Decision 1:
Put env variables into gitignore
Why: Security

Options 2: Give all bots equal capital , or split differently
Decision 2: Chose to split starter funds between 1000, 200, and 200 for stable,risky1,risky2
Why: Stable should have greater funds since less risk is always better and its better to have a safety net.

Option 3: Make stable assets dynamic like risky, or make it fixed
Decision 3: Chose to make stable assets fixed for now
Why: If it was ML like risky1, then it could get tricked by a stock that does well but is actually really risky. The stocks given are proven to be stable and "safe bets"

option 4: Choose another day amount or make it 14 days
Decision 4: 14 day trading interval
Why: 7 days is too volatile because one week can be very different from another week. Is 2 week also volatile? Yes, but it still gives more time for training and keeping the bot accurate.


Options 5: Make percentages for kill switch different or this
Decision 5: Choosing 15% and 30% kill switch for stable vs risky
Why: 15% fits stable bot profile and can be possibly regrown. 30% in a risky is because risky is more aggressive and more volatile, but also because if more than 30 is lost then its time to stop.

Options 6: Use SQLite or another alternative
Decision 6: Use SQLite
Why: There is no setup, uses a single file to transfer data, and no server process and since its only done locally and for myself, a larger database such as PostgreSQL or MySQL is not helpful at this stage or will be beneficial overall.

Option 7: run pnl and reason as opptional or make it mandatory
Decision 7: Make it optional 
Why: there might be no valid answer the system will give

Option 8: Create 3 bots or 4 bots
Decision 8: Make stable, risky1 and risky 2
Why:I didn't create a stable2 for crypto as the market does not have enough historical data for me to trust it 


**RESULT OF 3/28/2026**
Project pending, foundation complete, allocation of funds, kill switch settings, list of potential assets, trade logging complete, configuration of system done. Next step is providing the data pipeline.


## March 28, 2026 (midday)-Feature Engineering
**Context**
A way to transform the raw data of prices into understandable data that ML models can learn and train on was the work done at this time.

**Options Considered 1:**
- Separate features into multiple files per bot
-  Build features into a single file for all bots
**Decision 1:** Build a single file for all bots
**Why**: To reduce complexity of the overall program, and because these features are fairly similar across all strategies, it justs needs adjustment per strategy and that can be done in the input.

**Options Considered 2:**
- Copy the dataframe per features before adjusting the new copy
- Modify the original dataframe
**Decision 2:** Copy and modify the copy of the dataframe.
**Why:** Should the data get corrupted while doing the features, it would be best to have the original data still safe and secure

**Options Considered 3:** 
- Use normal averages of the entire time
- Use rolling averages 
**Decision 3:** Use rolling averages
**Why:** To keep the bot more accurate. Past data may no longer reflect current markets and may actually be harmful in future predictions

**Results of March 28th 2026 Midday session**
Feature engineering is now complete. Indicators that were implemented: rolling averages, RSI, momentum, Bollinger Bands, ATR, Z-score, and volume ratios. Tests have not yet happened because system is not yet ready for testing.

## March 28, 2026 Late Evening - Polygon Data Fetcher

**Context:**
Needed a source of real etf and stock price data for the bots

**Options Considered 1:** times to analyze
- Default to minute
- default to hours
- default to day
- default to other data

**Decision 1**
Stick to day data since we are sticking to free tier and minute/hour would require paid tier for Polygon.

**Options Considered 2:** how recent should the lookback of the bar be
- Fetch only today
- Fetch 5 days
- Fetch multiple days ago

**Decisions 2**: Choose 5 days since that is close enough to be related but not too small that it will be completely disregarded by outliers

**Options considered 3** Handling of empty data
- Crash
- Return with warning
- Ignore and move on

**Decision 3:** Return with a warning because the user should be warned there is no data, but the bot shouldn't simply crash. The bot also shouldn't move on without informing user because something might be wrong

**Result:** Still pending, we haven't tested yet

## March 28, 2026 (Early Night) — Switched from Kraken to Polygon for Crypto

**Context:**
I am in a location that is geoblocked by Kraken at the time of this bot creation. Kraken was supposed to be the crypto checker for risky2

**Options Considered:**
- Lie about location to use Kraken
- Use Gemini (requires phone number which I don't want to give out for this)
- Use Coinbase Advanced
- Use Polygon for data and Alpaca for execution of the transactions

**Decision:**
Decided to go with the final option 

**Why:**
since I am already using polygon for the stocks and etfs. I just wanted to have more options in case polygon failed to work, but its not worth the effort of making new accounts and ensuring all locations work, and making a whole new plan of what libraries are needed, etc. Finally, using one data source for all bots will make it easier and I won't have to do any changes to build_features() for crypto as well. :D

**Result:**
Pending system completion.