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

**Options Considered1:**
- Lie about location to use Kraken
- Use Gemini (requires phone number which I don't want to give out for this)
- Use Coinbase Advanced
- Use Polygon for data and Alpaca for execution of the transactions

**Decision1:**
Decided to go with the final option 

**Why1:**
since I am already using polygon for the stocks and etfs. I just wanted to have more options in case polygon failed to work, but its not worth the effort of making new accounts and ensuring all locations work, and making a whole new plan of what libraries are needed, etc. Finally, using one data source for all bots will make it easier and I won't have to do any changes to build_features() for crypto as well. :D

**Result1:**
Pending system completion.

## March 28, 2026 (Early Night) — Added sentiment fetcher 

**Context1:**
Need something to calculate sentiment

**Options Considered1:**
- Use Textblob
- Use BERT
- Use other complex models

**Decision1:**
Decided to go with the first option 

**Why1:**
Textblob takes 2 lines to setup, its instant, its decent accuracy (not as good as more complex models, but works well enough), is beginner friendly, and it runs locally on the model, without requiring additional hardware. The only limitations is that it doesn't understand financial jargon, and fails to consider context.

**Result:**
Pending system completion.



**Context1:**
What to return when there is no news?
**Options Considered1:**
- Return error
- return positive
- return negative
- return neutral

**Decision1:**
Decided to go with the final option 

**Why1:**
Since there is no news, it is literally neutral, there is no feelings. It is possible there won't be no news so error is off the table, and its not necessarily positive or negative so I cannot do that.

**Result1:**
Pending system completion.


**Context1:**
What to apply in score column for rows

**Options Considered1:**
- Use different scores per row
- Use scores only in first row
- Use same score for all rows

**Decision1:**
Decided to go with the final option 

**Why1:**
Since the rows are talking about the same content, and we are inputting average score, we should use the same score for all rows.

**Result:**
Pending system completion.




## March 28, 2026 (Late Night) - Regime Detector

**Context1:**
Need to determine what to check first : volatile or trending
**Options Considered1:**
- Check trending first
- check volatile first

**Decision1:**
Decided to go with the final option 

**Why1:**
If you check trending first, then if its trending because its volatile, thats bad. If its volatile, then you aren't trading.

**Result:**
Pending system completion.


**Context2:**
Where to allow stable, either in RANGING and TRENDING and /or VOLATILE
**Options Considered2:**
- Allow in all
- Allow in first 2
- Choose something else

**Decision2:**
Decided to go with the second option 

**Why2:**
stable cannot be in volatile because it is opposing the exact meaning of volatile. Ranging and trending however could fit within the expectations
**Result:**
Pending system completion.




**Context2:**
I need to decide which bots to allow in VOLATILE
**Options Considered2:**
- Allow  all
- Allow in first 2
- Allow only risky2
- other choices
**Decision2:**
Decided to go with the third option 

**Why2:**
risky2 could be in volatile because crypto is inherently volatile, and doesn't have as much history as risky1. Additionally new coins could result in market change. However, stock markets are significantly more stable and as such should not be as volatile, thus risky1 is not allowed
**Result:**
Pending system completion.






## March 29, 2026 (Late Night) - Stable and Risky1 Supervised Learning Model Trainer creation

**Context1:**
Need to choose something to train model
**Options Considered1:**
- XGBoost
- LightGBM
- CatBoost
- Random Forest
- Spark MLib GBT
- AdaBooost
- LinearBoost

**Decision1:**
Decided to go with XGBoost

**Why1:**
XGboost is a industry standard and is used often. LightGBM was also considered greatly as it is comparable, and occasionally even better than XGBoost. This was a coin toss because LightGBM was essentially the same based on what my use would be (Its not going to have a huge difference in speed due to what we are testing on-years of daily bars of data). CatBoost is for categorical, I am using numbers. Random Forest is weaker than XGBoost on financial data and tends to be more overfitting. Spark MLib GBT would require more computers but I am using a single VPS
AdaBoost is slower, less accurate than XGBoost and older. I think XGBoost is considered the successor of AdaBoost? They both have Boost in their names
LinearBoost: Finance is not necessarily linear and might not be as good a fit.
**Result:**
Pending system completion.


**Context2:**
Need to decide how to split data into testing and training
**Options Considered2:**
- Standard split of 80 and 20 (First learned during ESE 188 understanding machine learning class in freshmen year, then learned this at Incture in India internship)
- 50 50
- other proportions

**Decision2:**
Decided to go with standard split
**Why2:**
Keeps enough test data (20 for test) while giving 80 for training. Theres enough to train without giving away the answers of the 20 testing. 
**Result:**
Pending system completion.


## March 29, 2026 (Late Night)— Per-Bot PAPER_MODE Flags

**Context:**
Bots need to be chosen when to be live or be paper traded because if its still be trained you don't want to use real money. 

**Options Considered:**
- One global PAPER_MODE flag for all bots
- Per-bot PAPER_MODE dictionary

**Decision:**
- Per bot paper mode

**Why:**
Stable and risky1 use supervised ML which is easier to test and make it go live earlier. risky2 is RL and would need a lot more paper trading time to prove itself. A single change would make them all switch at the same time. Its best to avoid risking money when not needed. Also, risky1 should also take more time than stable due to its inherent nature of being risky.

**Result:**
Pending system completetion.

## March 29, 2026 (Late Night)— Retraining of supervised learning bots creation

**Context:**
What data to train on? 
**Options Considered:**
- Once a year
- Once every two weeks
- Some other time
- 2 years

**Decision:**
- per 2 years

**Why:**
Train on 2 years training data because it is recent enough to be effective but not so recent that it will be entirely affected by outliers

**Result:**
Pending system completetion.


**Context:**
How to schedule retrain?
**Options Considered:**
- background scheduler
- blocking scheduler

**Decision:**
- background

**Why:**
We don't really need to see the scheduling reset every single time we look because its not the main point of the program

**Result:**
Pending system completetion.