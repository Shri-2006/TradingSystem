#Decision Log to keep track of what I was thinking while building

##March 27, 2026-Configuration of the system and allocation of the money and where to invest
**CONTEXT**: 

Began building the program. Created structure of the overall project, wrote config.py, readme, core folder, requirements.txt and gitignore

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

**RESULT OF 3/27/2026**
Project pending, only basic configuration has been set.