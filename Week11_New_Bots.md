
## Bot 4 & 5 (do this absolutely last, make sure the first 3 bots work)
- Implement a RL version of stable and risky1 for stocks and etfs

## Bot 6(do this absolutely last, make sure the first 3 bots work)
- Implement a supervised learning version of risky2 (for crypto)

## Bot 7,8,9(do this absolutely last, make sure the first 3 bots work)
-Implement a unsupervised learning version of stable,risky1, risky2



## Cloud SQL update
Have the model ping a cloud server (maybe your onedrive?) and upload the models that have been created. ONLY ON ORACLE CLOUD INSTANCE. This will prevent the bot from seeming like its inactive (so do it like once every 10 min). Doing this will also create a backup in case your instance crashes, so you dont have to train a brand new model for each strategy from scratch again. Now that we are on oracle, change the command in config.py to true in featureflags
