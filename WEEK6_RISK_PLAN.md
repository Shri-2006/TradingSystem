I want to improve the trading system’s risk management in a practical, incremental way. Please help me implement this step by step, with explanations as we go, and keep the design simple unless I ask for something more advanced.

Current system:
- There are at least two bots/strategies:
  1. Stable bot
  2. Risky1 bot
- Stable bot currently has a portfolio-level stop: if portfolio value drops 15% from its reference value, it sells everything and stops trading.
- Risky1 bot currently has a portfolio-level stop: if portfolio value drops 30% from its reference value, it sells everything and stops trading.
- The bots are already running, and when the market is closed they simply check every 60 seconds and sleep again if closed.

What I want:
Help me evolve this from basic “kill switch only” risk management into a cleaner multi-layer risk management system.

Priority order:
1. Keep the existing portfolio-level drawdown stop logic
2. Add per-trade risk control
3. Add position sizing
4. Optionally add reduced aggressiveness when drawdown gets worse

Please guide me through implementing the following:

1. Portfolio-level risk control
- Keep the existing max drawdown stop for each bot.
- Stable bot: stop trading and liquidate if portfolio drops 15%
- Risky1 bot: stop trading and liquidate if portfolio drops 30%
- Help me structure this cleanly in code so each bot can have its own risk limits.
- Also help define what value the drawdown is measured from:
  - starting capital
  - peak portfolio value
Explain which is better and why.

2. Trade-level risk control
I want each individual trade to have its own stop loss so one bad trade does not cause major damage.
Please help me implement:
- a stop-loss per position/trade
- optionally a take-profit later, but stop-loss is the first priority
- make the stop-loss configurable per bot or strategy

Please explain:
- how to calculate stop-loss thresholds
- whether it should be percentage-based or volatility-based for now
- what a good simple starting version looks like

3. Position sizing
Right now I do not want to overexpose the portfolio to a single trade.
Please help me implement basic position sizing.

I want a simple approach first, such as one of these:
- fixed percentage of available capital per trade
- fixed dollar allocation per trade
- risk-based sizing tied to stop-loss distance

Please explain the pros/cons of each, then recommend the best simple approach for my current stage.
I care more about something correct and understandable than something overly sophisticated.

4. Optional drawdown response
If a bot starts performing badly but has not yet hit the full kill switch, I want to consider reducing risk before total shutdown.
Please help me think about a simple rule like:
- if drawdown exceeds some warning threshold, reduce position size
- if it gets worse, reduce again
- if it hits max drawdown, liquidate and stop

This is optional after the first three are done, but I want the architecture to support it later.

Implementation goals:
- Keep the code modular and easy to understand
- Separate strategy logic from risk logic as much as possible
- Make risk settings configurable per bot
- Avoid overengineering
- Explain each design choice in plain language
- Build step by step, not all at once

Please help me with:
1. overall design / architecture for this risk system
2. file/module structure if relevant
3. exact implementation order
4. pseudocode first
5. then actual code, one part at a time
6. brief explanations of why each step matters

Important:
- Do not rewrite my entire system from scratch unless necessary
- Work with the idea that this is an existing trading bot that I am improving
- Prefer simple, production-reasonable choices over academic complexity
- When there are multiple possible designs, recommend one and explain why

At the end, I want the system to be something I can describe like this:
- portfolio-level drawdown protection
- per-trade stop-loss protection
- controlled position sizing
- strategy-specific risk tolerance
- room for future dynamic risk reduction




Clarification on project order:

When I say I want to implement the RL bot before the full risk-management upgrade, I mean I want to first create the RL bot’s code architecture and integrate it into the system, not actually run/train/deploy it yet.

So please help me design the RL bot in a way that is compatible with future risk controls.

Requirements:
- The RL bot should fit into the same overall trading system as the stable and risky1 bots
- Its design should support future portfolio-level drawdown protection
- Its design should support future per-trade stop-loss logic
- Its design should support future position sizing rules
- I do not need the full risk-management implementation yet, but I do want clean hooks/interfaces for it

Please guide me so that:
1. I implement the RL bot architecture first
2. I avoid hardcoding things that will make risk management harder later
3. After the RL bot structure is complete, I can then add a shared risk-management layer across all bots
