# forex_sniper_bot.py

import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import datetime

# -------------------------
# CONFIGURATION
# -------------------------
OANDA_ACCOUNT_ID = 'YOUR_ACCOUNT_ID'
OANDA_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
SYMBOL = 'USD/JPY'  # Forex pair
GRANULARITY = 'H1'  # 1-hour candles
LOOKBACK_CANDLES = 100
REWARD_RATIO = 2
RISK_PCT = 1
ACCOUNT_BALANCE = 1000

client = API(access_token=OANDA_ACCESS_TOKEN)

# -------------------------
# FETCH HISTORICAL DATA
# -------------------------
def fetch_ohlc(symbol, granularity, count=LOOKBACK_CANDLES):
    params = {"count": count, "granularity": granularity}
    r = instruments.InstrumentsCandles(instrument=symbol, params=params)
    client.request(r)
    candles = r.response['candles']

    data = []
    for c in candles:
        if c['complete']:
            data.append([
                c['time'],
                float(c['mid']['o']),
                float(c['mid']['h']),
                float(c['mid']['l']),
                float(c['mid']['c'])
            ])
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
    return df

# -------------------------
# TREND DETECTION
# -------------------------
def detect_trend(data, window=20):
    data['ma'] = data['close'].rolling(window=window).mean()
    if data['ma'].iloc[-1] > data['ma'].iloc[-2]:
        return 'uptrend'
    else:
        return 'downtrend'

# -------------------------
# FAIR VALUE GAP DETECTION
# -------------------------
def find_fvg(data):
    fvg_list = []
    for i in range(1, len(data)-1):
        prev = data.iloc[i-1]
        curr = data.iloc[i]
        # Gap up
        if curr['low'] > prev['high']:
            fvg_list.append((i, 'gap_up', prev['high'], curr['low']))
        # Gap down
        elif curr['high'] < prev['low']:
            fvg_list.append((i, 'gap_down', curr['high'], prev['low']))
    return fvg_list

# -------------------------
# FILTER TRADES BY TREND
# -------------------------
def filter_trades_by_trend(fvg_list, current_trend):
    trades = []
    for fvg in fvg_list:
        index, gap_type, low, high = fvg
        if current_trend == 'uptrend' and gap_type == 'gap_up':
            trades.append((index, 'long', low, high))
        elif current_trend == 'downtrend' and gap_type == 'gap_down':
            trades.append((index, 'short', low, high))
    return trades

# -------------------------
# GENERATE TRADE SIGNALS
# -------------------------
def generate_trade_signals(trades, reward_ratio=REWARD_RATIO):
    signals = []
    for trade in trades:
        index, trade_type, entry_low, entry_high = trade
        if trade_type == 'long':
            entry = entry_low
            sl = entry_low - (entry_high - entry_low)
            tp = entry + (entry - sl) * reward_ratio
        elif trade_type == 'short':
            entry = entry_high
            sl = entry_high + (entry_high - entry_low)
            tp = entry - (sl - entry) * reward_ratio
        signals.append({
            'index': index,
            'type': trade_type,
            'entry': entry,
            'stop_loss': sl,
            'take_profit': tp
        })
    return signals

# -------------------------
# BACKTEST
# -------------------------
def backtest(signals, data):
    balance = ACCOUNT_BALANCE
    wins = 0
    losses = 0
    for s in signals:
        index = s['index']
        trade_type = s['type']
        entry = s['entry']
        sl = s['stop_loss']
        tp = s['take_profit']
        if index+1 >= len(data):
            continue
        next_candle = data.iloc[index+1]
        hit_tp = False
        hit_sl = False
        if trade_type == 'long':
            if next_candle['low'] <= sl:
                hit_sl = True
            elif next_candle['high'] >= tp:
                hit_tp = True
        else:
            if next_candle['high'] >= sl:
                hit_sl = True
            elif next_candle['low'] <= tp:
                hit_tp = True
        trade_risk = balance * (RISK_PCT / 100)
        if hit_tp:
            balance += trade_risk * REWARD_RATIO
            wins += 1
        elif hit_sl:
            balance -= trade_risk
            losses += 1
    print(f"Backtest: Balance=${balance:.2f}, Wins={wins}, Losses={losses}")

# -------------------------
# MAIN EXECUTION
# -------------------------
def main():
    data = fetch_ohlc(SYMBOL, GRANULARITY)
    current_trend = detect_trend(data)
    fvg_list = find_fvg(data)
    trades = filter_trades_by_trend(fvg_list, current_trend)
    trade_signals = generate_trade_signals(trades)
    print("Trade Signals:")
    for ts in trade_signals:
        print(ts)
    backtest(trade_signals, data)

if __name__ == "__main__":
    main()
