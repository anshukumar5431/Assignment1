import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pd.set_option('display.width', 140)

# load both files
trades = pd.read_csv('/mnt/user-data/uploads/historical_data.csv')
fg = pd.read_csv('/mnt/user-data/uploads/fear_greed_index.csv')

# trades timestamp is dd-mm-yyyy hh:mm, need to convert before we can join on date
trades['Timestamp IST'] = pd.to_datetime(trades['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
trades['date'] = trades['Timestamp IST'].dt.normalize()

fg['date'] = pd.to_datetime(fg['date']).dt.normalize()
fg = fg[['date', 'classification', 'value']].drop_duplicates('date')  # just in case there are dupes

df = trades.merge(fg, on='date', how='left')
print("rows with no sentiment match:", df['classification'].isna().sum(), "/", len(df))
df = df.dropna(subset=['classification']).copy()

# collapse the 5 classes down to 3 buckets, easier to eyeball trends this way
def bucket(c):
    if 'Fear' in c:
        return 'Fear'
    elif 'Greed' in c:
        return 'Greed'
    return 'Neutral'

df['sentiment_bucket'] = df['classification'].apply(bucket)

df['is_close'] = df['Closed PnL'] != 0
df['win'] = df['Closed PnL'] > 0
df['loss'] = df['Closed PnL'] < 0

df.to_parquet('/home/claude/analysis/merged.parquet')
print(df.shape)

order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
closes = df[df['is_close']].copy()
print("closing trades (nonzero pnl):", len(closes), "out of", len(df))

# win rate + avg pnl per trade, 5-class 
g = closes.groupby('classification').agg(
    trades=('Closed PnL', 'count'),
    win_rate=('win', 'mean'),
    avg_pnl=('Closed PnL', 'mean'),
    median_pnl=('Closed PnL', 'median'),
    total_pnl=('Closed PnL', 'sum'),
)
print(g.reindex(order))

# same thing but 3-bucket
g2 = closes.groupby('sentiment_bucket').agg(
    trades=('Closed PnL', 'count'),
    win_rate=('win', 'mean'),
    avg_pnl=('Closed PnL', 'mean'),
    total_pnl=('Closed PnL', 'sum'),
)
print(g2)

# avg trade size by sentiment - curious if people size up during fear or greed
print(df.groupby('classification')['Size USD'].agg(['mean', 'median', 'sum']).reindex(order))

# long/short bias - only look at opening fills
opens = df[df['Direction'].isin(['Open Long', 'Open Short'])]
bias = opens.groupby(['classification', 'Direction']).size().unstack(fill_value=0).reindex(order)
bias['pct_long'] = bias['Open Long'] / (bias['Open Long'] + bias['Open Short'])
print(bias)

# avg size for wins vs losses, split by sentiment
risk = closes.groupby(['classification', 'win'])['Size USD'].mean().unstack()
print(risk.reindex(order))

# per-account totals, sorted, top 10
acct = closes.groupby(['Account', 'sentiment_bucket'])['Closed PnL'].sum().unstack(fill_value=0)
acct['total'] = acct.sum(axis=1)
acct = acct.sort_values('total', ascending=False)
print(acct.head(10))

# quick correlation check between the raw index value and daily pnl
daily = closes.groupby('date').agg(pnl=('Closed PnL', 'sum'), value=('value', 'first')).dropna()
print("corr (sentiment value vs daily pnl):", daily['pnl'].corr(daily['value']))

top_coins = df['Coin'].value_counts().head(8).index
coin_g = closes[closes['Coin'].isin(top_coins)].groupby(['Coin', 'sentiment_bucket'])['Closed PnL'].sum().unstack(fill_value=0)
print(coin_g)

# CHARTS 
plt.rcParams['font.size'] = 11
COLORS = {'Extreme Fear': '#8B0000', 'Fear': '#E06666', 'Neutral': '#B7B7B7', 'Greed': '#93C47D', 'Extreme Greed': '#38761D'}

# chart 1 - win rate bars + avg pnl line on twin axis
g = closes.groupby('classification').agg(win_rate=('win', 'mean'), avg_pnl=('Closed PnL', 'mean')).reindex(order)

fig, ax1 = plt.subplots(figsize=(9, 5))
bars = ax1.bar(g.index, g['win_rate'] * 100, color=[COLORS[i] for i in g.index], alpha=0.85)
ax1.set_ylabel('Win Rate (%)')
ax1.set_ylim(0, 100)
for b in bars:
    ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, f"{b.get_height():.1f}%", ha='center', fontsize=10)

ax2 = ax1.twinx()
ax2.plot(g.index, g['avg_pnl'], color='black', marker='o', linewidth=2, label='Avg PnL/trade')
ax2.set_ylabel('Avg Closed PnL per Trade (USD)')
for i, v in enumerate(g['avg_pnl']):
    ax2.annotate(f"${v:.0f}", (i, v), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, fontweight='bold')

plt.title('Win Rate and Average PnL per Trade by Market Sentiment')
fig.tight_layout()
plt.savefig('/home/claude/analysis/chart1_winrate_pnl.png', dpi=150)
plt.close()

# chart 2 - long/short split
bias_pct = bias[['Open Long', 'Open Short']].div(bias['Open Long'] + bias['Open Short'], axis=0) * 100

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(bias_pct.index, bias_pct['Open Long'], label='Long %', color='#38761D')
ax.bar(bias_pct.index, bias_pct['Open Short'], bottom=bias_pct['Open Long'], label='Short %', color='#CC0000')
ax.axhline(50, color='black', linestyle='--', linewidth=1)
ax.set_ylabel('% of Opened Positions')
ax.set_title('Long vs Short Positioning by Market Sentiment')
ax.legend()
for i, (l, s) in enumerate(zip(bias_pct['Open Long'], bias_pct['Open Short'])):
    ax.text(i, l / 2, f"{l:.0f}%", ha='center', color='white', fontweight='bold')
    ax.text(i, l + s / 2, f"{s:.0f}%", ha='center', color='white', fontweight='bold')
fig.tight_layout()
plt.savefig('/home/claude/analysis/chart2_long_short_bias.png', dpi=150)
plt.close()

# chart 3 - avg trade size
size_g = df.groupby('classification')['Size USD'].mean().reindex(order)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(size_g.index, size_g.values, color=[COLORS[i] for i in size_g.index], alpha=0.85)
ax.set_ylabel('Average Trade Size (USD)')
ax.set_title('Average Trade Size by Market Sentiment')
for b in bars:
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 50, f"${b.get_height():,.0f}", ha='center', fontsize=10)
fig.tight_layout()
plt.savefig('/home/claude/analysis/chart3_trade_size.png', dpi=150)
plt.close()

# chart 4 - cumulative pnl over time
daily_cum = closes.groupby('date').agg(pnl=('Closed PnL', 'sum')).reset_index().sort_values('date')
daily_cum['cum_pnl'] = daily_cum['pnl'].cumsum()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(daily_cum['date'], daily_cum['cum_pnl'], color='#1155CC', linewidth=1.8)
ax.set_ylabel('Cumulative Closed PnL (USD)')
ax.set_title('Cumulative Trader PnL Over Time')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
fig.tight_layout()
plt.savefig('/home/claude/analysis/chart4_cumulative_pnl.png', dpi=150)
plt.close()

# chart 5 - pnl distribution, clipped so the outliers don't wreck the scale
fig, ax = plt.subplots(figsize=(9, 5))
data = [closes[closes['classification'] == c]['Closed PnL'].clip(-500, 500) for c in order]
bp = ax.boxplot(data, labels=order, showfliers=False, patch_artist=True)
for patch, c in zip(bp['boxes'], order):
    patch.set_facecolor(COLORS[c])
    patch.set_alpha(0.7)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel('Closed PnL per Trade (USD, clipped +/-500 for visibility)')
ax.set_title('Distribution of Trade PnL by Market Sentiment')
fig.tight_layout()
plt.savefig('/home/claude/analysis/chart5_pnl_distribution.png', dpi=150)
plt.close()

print("done, charts saved to /home/claude/analysis/")
