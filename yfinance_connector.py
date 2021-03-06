import yfinance as yf


def get_ohlc(ticker, period, interval):
    t = yf.Ticker(ticker)
    print(period)
    print(interval)
    history = t.history(period=period, interval=interval)
    history = history[["Open", "High", "Low", "Close"]]
    return history


def add_MA(df, window_size):
    df[f'MA_{window_size}'] = df["Close"].rolling(window=window_size).mean()
    return df


def add_crossings(df, ma_1, ma_2):
    previous_ma_1 = df[ma_1].shift(1)
    previous_ma_2 = df[ma_2].shift(1)
    df['Crossover'] = (((df[ma_1] <= df[ma_2]) & (previous_ma_1 >= previous_ma_2))
                | ((df[ma_1] >= df[ma_2]) & (previous_ma_1 <= previous_ma_2)))
    return df


def get_prepped_df(ticker, short_ma_period, long_ma_period, period, interval):
    ohlc = get_ohlc(ticker, period=period, interval=interval)
    ohlc = add_MA(ohlc, short_ma_period)
    ohlc = add_MA(ohlc, long_ma_period)
    ohlc = add_crossings(ohlc, f"MA_{short_ma_period}", f"MA_{long_ma_period}")
    return ohlc


