import pandas as pd
import matplotlib.pyplot as plt

import os

print(os.listdir(r"C:\Users\sagar\Downloads\Research Work\task8_week3&4"))

# 1. Player recommendations (H1)
df_mentions = pd.read_csv("mentions_by_condition.csv")
h1 = df_mentions[df_mentions["hypothesis_id"]=="H1"]

pivot = h1.pivot(index="condition", columns="entity", values="total_mentions")
pivot.plot(kind="bar", figsize=(8,5))
plt.title("Player Mentions by Framing Condition (H1)")
plt.ylabel("Mentions")
plt.tight_layout()
plt.savefig("h1_player_mentions.png", dpi=300)

# 2. Sentiment by condition
sent = pd.read_csv("sentiment_by_condition.csv")
sent_plot = sent[sent["hypothesis_id"].isin(["H1","H3"])]

pivot2 = sent_plot.pivot(index="condition", columns="hypothesis_id", values="mean_sentiment")
pivot2.plot(kind="bar", figsize=(8,5))
plt.title("Sentiment by Condition (H1 & H3)")
plt.ylabel("Mean Sentiment Score")
plt.tight_layout()
plt.savefig("sentiment_by_condition.png", dpi=300)

# 3. Strategy axis (H3)
strategy = pd.read_csv("recommendation_strategy_by_condition.csv")
h3 = strategy[strategy["hypothesis_id"]=="H3"]

pivot3 = h3.pivot(index="condition", columns="strategy_axis", values="count")
pivot3.plot(kind="bar", stacked=True, figsize=(8,5))
plt.title("Strategy Axis by Condition (H3)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("h3_strategy_axis.png", dpi=300)

# 4. Fabrication rate
fab = pd.read_csv("fabrication_rate_by_condition.csv")
fab_h3 = fab[fab["hypothesis_id"]=="H3"]

fab_h3.plot(kind="bar", x="condition", y="fabrication_rate", figsize=(6,4))
plt.title("Fabrication Rate by Condition (H3)")
plt.ylabel("Rate")
plt.tight_layout()
plt.savefig("fabrication_rate.png", dpi=300)
