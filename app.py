#USED LIBRARIES

import streamlit as st
import yfinance as yf
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas import json_normalize

#Title
st.title("Take the money and run",icon="🏃‍♂️‍➡️",text_alignment="center")
st.markdown("This website was created to visualize how the US stock-market behaved in the last 14 years.")
def effect():
    st.balloons()
st.button(label="Don't push this button",on_click=effect)



    



df = pd.read_csv("Stock_prices_from2012.06 (1).csv", header=[0, 1], index_col=0, parse_dates=True)
change = df["Close"].pct_change()*100

df2 = df.drop(columns=["Volume"]).droplevel(0, axis=1)
df2.head()


top7_2012 = ["AAPL", "XOM", "MSFT", "IBM", "GE", "CVX", "BRK-B"]
data_2012 = yf.download(top7_2012, start="2012-06-01", end="2026-09-17")["Close"]



normalized = ((df2 / df2.iloc[0])-1)*100
# Equal weight M7 average (ideal/theoretical distribution — 1/7 each)
normalized["M7"]= normalized[["GOOGL", "AMZN", "AAPL", "META", "MSFT","NVDA","TSLA"]].mean(axis=1)
# Simulating 1000 randomly weighted M7 portfolios and averaging to approximate realistic investor returns
mag7 = ["GOOGL", "AMZN", "AAPL", "META", "MSFT", "NVDA", "TSLA"]
#SIDE BAR:

with st.sidebar:
    st.header("Investment Calculator",icon="💶")
    st.markdown("This tool calculates how much you would have made if you had invested in the S&P 500 between given dates.")
    y_start_date = st.date_input("Investement start:",value=None,min_value=change.index.min().date())
    y_end_date = st.date_input("Investment end:",value= None)
    amount = st.number_input("Amount invested:",value=0.0)

    def yield_calc(change, start, end, invest):
        growth = (1 + change["SPY"].loc[start:end] / 100).prod()
        return invest * growth

    yield_calc(change, y_start_date, y_end_date, amount)
    st.write(f"By investing {amount:,.0f}€ from {y_start_date} until {y_end_date} would result you {yield_calc(change, y_start_date, y_end_date, amount):,.2f}€, which is {yield_calc(change, y_start_date, y_end_date, amount)-amount:,.2f}€ profit and it equals to {(yield_calc(change, y_start_date, y_end_date, amount)/amount-1)*100:,.2f}% yield")


n_simulations = 1
results = []

for _ in range(n_simulations):
    weights = np.random.dirichlet(np.ones(7))
    portfolio_return = (normalized[mag7] * weights).sum(axis=1)
    results.append(portfolio_return)

simulations = pd.DataFrame(results).T
simulations.index = normalized.index

# One average line
normalized["IRL-M7"] = simulations.mean(axis=1)
normalized.head()


normalized_1= ((data_2012/data_2012.iloc[0])-1)*100
normalized_1["2012-M7"]= normalized_1[top7_2012].mean(axis= 1)
normalized_1.head()


# # Fig 1 SPY on the market



figN1 = px.line(normalized,x=normalized.index,y=["SPY"])
figN1.update_layout(title={"text": "Change of the market over time - represented by the SnP 500 index", 'x': 0.5, 'xanchor': 'center'}, font=dict(size=18),
    yaxis_title="Change(%)",   
    xaxis_title="Date")



st.plotly_chart(figN1,key="fig1")
st.markdown("Figure 1: Price change of the S&P 500 (SPY) from 2012-06-01 to 2026-09-15.")

if st.checkbox("Show the daily closing prices & volumes of the M7 companies and the S&P 500"):
    st.dataframe(df)
st.markdown("--------------------------------------------------------------")




spy = df["Close"]["SPY"]
dd = (spy / spy.cummax() - 1) * 100  

figD3 = px.line(dd)

figD3.update_traces(hovertemplate = (
        "<b>SnP 500</b><br>"
        "Change since last max = %{y:.2f}%<br>" 
        "Date: %{x|%d %b %Y}<br>"
        "<extra></extra>"))

figD3.update_layout(
    title={"text": "Percentage fall (drawdown) compared to previous values represented on the SnP 500", 'x': 0.5, 'xanchor': 'center'},
    font=dict(size=16),
    yaxis={"title": {"text": "Change %", "font": {"size": 16}}},
    xaxis={"title": {"text": "Date", "font": {"size": 16}}, "hoverformat": "%d %b %Y"},
    showlegend=False,
    height=600,
)


figD3.add_annotation(
    x="2015-08-25", y=-11.9,
    text="Panic over <br> Chinese economy",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="crimson",
    ax=-120, ay=-20,              # arrow tail offset in pixels
    bgcolor="white", bordercolor="black", borderwidth=1,
)

figD3.add_annotation(
    x="2016-02-11", y=-13.0,
    text="Fear of slowing economy",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="crimson",
    ax=0, ay=50,              # arrow tail offset in pixels
    bgcolor="white", bordercolor="black", borderwidth=1,
)


figD3.add_annotation(
    x="2018-12-24", y=-19.4,
    text="US political tension",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="crimson",
    ax=-100, ay=20,              # arrow tail offset in pixels
    bgcolor="white", bordercolor="black", borderwidth=1,
)


figD3.add_annotation(
    x="2020-03-23", y=-33.7,
    text="COVID crash",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5,arrowcolor="crimson",
    ax=-100, ay=50,              # arrow tail offset in pixels
    bgcolor="white", bordercolor="black", borderwidth=1,
)

figD3.add_annotation(
    x="2025-4-08", y=-18.8,
    text="Chinese trade tension",
    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="crimson",
    ax=0, ay=50,              # arrow tail offset in pixels
    bgcolor="white", bordercolor="black", borderwidth=1,
)


figD3.add_vrect(
    x0="2022-01-03", x1="2022-10-12",
    fillcolor="red", opacity=0.12, line_width=0,
    annotation_text="Fed hiking cycle", annotation_position="bottom",
)
figD3.update_xaxes(
    range=[dd.index.min(), dd.index.max()],
    constrain="domain",
)
figD3.update_yaxes(range=[dd.min() * 1.15, 2])
figD3.update_layout(margin=dict(l=80, r=60, t=90, b=60))
#plotting
st.plotly_chart(figD3,key="fig2")
st.markdown("Figure 2: Visual representation of the price drops of the S&P 500.")
st.markdown("--------------------------------------------------------------")
st.subheader("Deeper visual analysis of the Mag7 and the SnP 500")

figN2 = go.Figure()

# SPY
figN2.add_scatter(
    x=normalized.index,
    y=normalized["SPY"],
    name="SPY",
    mode="lines"
)

# Magnificent 7 from 2012
figN2.add_scatter(
    x=normalized_1.index,
    y=normalized_1["2012-M7"],
    name="M7 (2012)",
    mode="lines"
)
# Current Magnificent 7:

figN2.add_scatter(
    x=normalized.index,
    y=normalized["M7"],
    name= "M7",
    mode="lines")

figN2.add_scatter(
    x=normalized.index,
    y=normalized["IRL-M7"],
    name="PF-M7",
    mode="lines"
)
figN2.update_layout(
    title={"text": "SPY vs Magnificent 7 variations", 'x': 0.5, 'xanchor': 'center'},
    font=dict(size=16),
    xaxis_title="Date",
    yaxis_title="Normalized Performance (%)"
)



st.plotly_chart(figN2,key="fig3")
st.markdown("Figure 3: Price percentile comparison between the S&P 500 (SPY) and the different variations of the Magnificent seven.")
st.markdown("SPY : Top 500 companies in the US.")
st.markdown("M7 : Current magnificent seven (GOOGL, AMZN, AAPL, META, MSFT, NVDA, TSLA).")
st.markdown("M7(2012): Magnificent seven of 2012 (AAPL, BRK-B, CVX, GE, IBM, MSFT, XOM).")
st.markdown("M7-PF: A representative of a randomly weighed M7 portfolio.")
st.markdown("--------------------------------------------------------------")
st.markdown("Please select a time range where you would like to compare the percentage changes of the M7 members and the S&P 500 :")
def rebase(change, start, end):
    return ((1 + change.loc[start:end] / 100).cumprod() - 1) * 100

start_date = st.date_input("input start date:",value=None,min_value=change.index.min().date())
end_date = st.date_input("input end date:",value= None)
rebase(change, start_date, end_date)

rebased = rebase(change, start_date, end_date)
close = df["Close"].loc[rebased.index]
daily  = change.loc[rebased.index]

figD2 = px.line(rebased, color='Ticker',
               labels={"value": "Change %", "index": "Date"})

for tr in figD2.data:
    tr.customdata = np.stack([
        daily[tr.name].to_numpy(),
        close[tr.name].to_numpy(),],
        axis = 1)
    tr.hovertemplate = (
        "<b>%{fullData.name}</b><br>"
        "Total Change: %{y:.2f}%<br>"
        "Daily Change: %{customdata[0]:.2f}%<br>" 
        "Close Price: $%{customdata[1]:.2f}<br>"
        "Date: %{x|%d %b %Y}<br>"
        "<extra></extra>"
    )

figD2.update_layout(
    title={"text": "Percentage change of stocks over time", 'x': 0.5, 'xanchor': 'center'},
    font=dict(size=16),
    yaxis={"title": {"text": "Change %", "font": {"size": 18}}},
    xaxis={"title": {"text": "Date", "font": {"size": 18}}, "hoverformat": "%d %b %Y"},
    height=600,
)


st.plotly_chart(figD2,key="fig4")
st.markdown("figure 4 :Percentage change of the single members of the M7 compared to the S&P 500 on a selected time scale.")
st.markdown("--------------------------------------------------------------")        
st.subheader("The magnicifent seven's performance since 2012")
normalized_yearly = normalized.resample("YE").last()

# Reshape to long format
normalized_long = normalized_yearly.reset_index().melt(
    id_vars="Date",
    var_name="Company",
    value_name="Return"
)

normalized_long["Date"] = normalized_long["Date"].dt.strftime("%Y-%m")


# Events
events = {
    "2013-12": "2013: Steve Ballmer announces retirement",
    "2014-12": "2014: Satya Nadella becomes Microsoft CEO",
    "2015-12": "Microsoft under new leadership",
    "2016-12": "NVDA & TSLA take over the market",
    "2022-06": "2022: Inflation + Fed rate hikes + Ukraine war",
}


# Create animation
fig5 = px.bar(
    normalized_long,
    x="Company",
    y="Return",
    animation_frame="Date",
    range_y=[0.01, normalized_long["Return"].max() * 1.3],
    log_y=True,
    title="Company performance from 2012"
)


# Add / remove annotations for each frame
for frame in fig5.frames:

    year = frame.name[:4]

    # Show event from 2013 through 2022
    if year in ["2013", "2014", "2015", "2016","2022"]:

        frame.layout = {
            "annotations": [
                {
                    "x": 0.5,
                    "y": 0.95,
                    "xref": "paper",
                    "yref": "paper",
                    "text": events.get(
                        frame.name,
                        "2022-06: 2022: Inflation + Fed rate hikes + Ukraine war"
                    ),
                    "showarrow": False,
                    "font": {
                        "size": 18
                    }
                }
            ]
        }

    # Remove annotation after 2016
    else:
        frame.layout = {
            "annotations": []
        }


# Slow down animation
fig5.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
fig5.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 800

st.plotly_chart(fig5,key="fig5")
st.markdown("figure 5 : Companies runs from 2012.")
st.markdown("IRL-M7 : A representative of a randomly weighed M7 portfolio.")
st.markdown("--------------------------------------------------------------")
st.subheader("The return of each company in the M7 since they opened their shares publicly")
normalized_1= ((data_2012/data_2012.iloc[0])-1)*100
normalized_1["M7"]= normalized_1[top7_2012].mean(axis= 1)
normalized_1.head()


individual_growth={}
for ticker in mag7:
    data=yf.download(ticker,period="max")["Close"].squeeze().dropna()
    normalized_ticker= ((data/data.iloc[0])-1 )*100
    individual_growth[ticker]= normalized_ticker
df_individual=pd.DataFrame(individual_growth)


final_returns = df_individual.iloc[-1]

# Calculate years public
years = df_individual.apply(lambda x: x.dropna().shape[0] / 252).round(1)

fig7 = px.bar(x=final_returns.index, y=final_returns.values,
              title="Total Return Since IPO",
              labels={"x": "Company", "y": "% Return"},
              log_y=True,
              text=[f"{y} yrs" for y in years])

fig7.update_traces(textposition="outside")
st.plotly_chart(fig7,key="fig6")
st.markdown("figure 6 : Total return of each company since their initial public offering(IPO).")
st.markdown("--------------------------------------------------------------")
st.subheader("How much each company of the M7 makes on average annualy")
growth_velocity = ((1 + final_returns/100) ** (1/years) - 1) * 100
fig_velocity=px.bar(growth_velocity,x=growth_velocity.index,y=growth_velocity.values,labels={"x": "Company", "y": "Annualized Return (CAGR %)"})

fig_velocity.update_layout(title=dict(text="Annualized Return (CAGR) Since IPO", font=dict(size=24)))

st.plotly_chart(fig_velocity,key="fig7")

st.markdown("Figure 7 : Average annual returns of each company since its IPO.")
st.markdown("--------------------------------------------------------------")
st.subheader("Price and traded volume correlation visual studies")

change_vol = df["Volume"].pct_change()*100

price = df["Close"]
vol = df["Volume"]

tickers=list(price.columns)

figD4 = make_subplots(rows=3, cols=3, subplot_titles = tickers, horizontal_spacing=0.07, vertical_spacing=0.09)

for i, t in enumerate(tickers):
    r, c = divmod(i, 3)
    x = price[t]
    y = vol[t]

    ok = x.notna() & y.notna() & (y > 0)
    logy = np.log10(y[ok])
    slope, intercept = np.polyfit(x[ok], logy, 1)
    corr = np.corrcoef(x[ok], logy)[0, 1]

    xs = np.linspace(x[ok].min(), x[ok].max(), 100)
    ys = 10 ** (slope * xs + intercept)

    figD4.add_trace(
        go.Scatter(
            x=x, y=y, mode="markers",
            marker=dict(size=3, opacity=0.3),
            showlegend=False,
        ),
        row=r + 1, col=c + 1,
    )

    figD4.add_trace(
        go.Scatter(x=xs, y=ys, mode="lines",
                   line=dict(color="red", width=2),
                   showlegend=False, hoverinfo="skip"),
        row=r + 1, col=c + 1,
    )

    figD4.add_annotation(
        text=f"R²={corr**2:.2f}", x=0.05, y=0.95,
        xref="x domain", yref="y domain", showarrow=False,
        font=dict(size=12, color="red"),
        row=r + 1, col=c + 1,
    )

figD4.update_layout(height=900, title={"text":"Traded volume vs price", 'x':0.5, 'xanchor':'center'}, font=dict(size=16),
    hovermode=False)
figD4.update_yaxes(type="log")
st.plotly_chart(figD4,key="fig8")
st.markdown("Figure 8 : Visual representation of how the traded volume of the individual stocks of the Mag7 and the SnP 500 decreased with the rise of their price. A trendline was fitted for each case.")
st.markdown("--------------------------------------------------------------")

rel_vol = vol / vol.rolling(63).median()

long = (change.stack().rename("change").to_frame()
        .join(rel_vol.stack().rename("rel_vol"))
        .join(vol.stack().rename("volume"))
        .dropna().reset_index())

surge = long[long["rel_vol"] >= 2.5].copy()     # days with 2x+ normal volume

figD5 = px.scatter(
    surge, x="Date", y="change",
    size="rel_vol", color="rel_vol",
    color_continuous_scale="Viridis",
    facet_col="Ticker", facet_col_wrap=2,
    size_max=18, opacity=0.7, height=1000,
    labels={"change": "Daily change (%)", "rel_vol": "Vol/med"},
    hover_data={"Date": "|%d %b %Y", "change": ":.2f", "rel_vol": ":.1f", "volume": ":,.0f"},
    )
figD5.add_hline(y=0, line_dash="dash", line_color="grey")
figD5.update_layout(title={"text":"High-volume days: when they happened, which way price moved, how big the surge", 'x':0.5, 'xanchor':'center'}, font=dict(size=16)),

#st.plotly_chart(figD5,key="fig9")
st.markdown("Figure 9 : Scatter plot of the high volume trade days (>2.5 x the 63 day median value) of each individual stocks of the Mag7 and the SnP 500. No conclusions were made whether the trade volume was greater because of the price change or the price changed because there was a greater volume traded. This would need deeper analysis of the news around certain dates and the price changes throughout affected days.")
st.markdown("--------------------------------------------------------------")

