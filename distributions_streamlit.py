import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")
plt.rcParams.update({'font.size': 16})

# Import functions (assuming these are in a functions.py file)
from functions import process_ticker, plot_distributions

def main():
    # Title at the very top of the window
    st.title('Comparison of Distributions')

    # Ticker mappings (Ticker Symbol: Display Name)
    ticker_mapping = {
        "FXI": "FXI - iShares China Large-Cap ETF",
        "SPY": "SPY - SPDR S&P 500 ETF Trust",
        "IBIT": "IBIT - iShares Bitcoin Trust ETF",
        "TLT": "TLT - iShares 20+ Year Treasury Bond ETF",
        "XLF": "XLF - Financial Select Sector SPDR Fund",
        "HYG": "HYG - iShares iBoxx $ High Yield Corporate Bond ETF",
        "QQQ": "QQQ - Invesco QQQ Trust Series I",
        "EEM": "EEM - iShares MSCI Emerging Markets ETF",
        "KWEB": "KWEB - KraneShares CSI China Internet ETF",
        "LQD": "LQD - iShares iBoxx $ Investment Grade Corporate Bond ETF",
        "IWM": "IWM - iShares Russell 2000 ETF",
        "GDX": "GDX - VanEck Gold Miners ETF",
        "SLV": "SLV - iShares Silver Trust"
    }

    # Sidebar for inputs
    with st.sidebar:
        st.header('Select Tickers')
        
        # Dropdowns for ticker selection
        display_names = list(ticker_mapping.values())  # Display names
        ticker_symbols = list(ticker_mapping.keys())  # Corresponding ticker symbols

        default_ticker1 = "SPY"  # Default: SPY
        default_ticker2 = "IBIT"  # Default: IBIT

        selected_display_name1 = st.selectbox(
            'First Ticker',
            display_names,
            index=ticker_symbols.index(default_ticker1)
        )
        selected_display_name2 = st.selectbox(
            'Second Ticker',
            display_names,
            index=ticker_symbols.index(default_ticker2)
        )

        # Get the actual ticker symbols
        ticker1 = ticker_symbols[display_names.index(selected_display_name1)]
        ticker2 = ticker_symbols[display_names.index(selected_display_name2)]

        # Add some text below the existing sidebar content
        st.markdown("---")  # Add a divider
        st.markdown("""
        ### About This App
        This app compares the accuracy of two statistical distributions applied to publicly traded ETF's:
        - Normal distribution
        - Student's t distribution

        The plots shown here confirm current knowledge that the student's t distribution better fits financial data.
        There are exceptions shown here, such as Bitcoin, where the returns are less predictable.

        The data sets available here are the ETF's with the highest traded volume, excluding any leveraged or inverse ETF's.
        """)

    # Process tickers
    tickers_to_analyze = [ticker1, ticker2]
    results = {}
    for ticker in tickers_to_analyze:
        results[ticker] = process_ticker(ticker, start_date='1900-01-01', end_date='2024-12-01')

    # Create plots
    # First Plot: Distribution Histograms
    fig1, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig1.suptitle('Histogram of Returns with Fitted Distributions')

    for i, ticker in enumerate(tickers_to_analyze):
        filtered_data, mape_values, distribution_names, distribution_params, norm_mu, t_mu, t_df = results[ticker]
        plot_distributions(axes[i], ticker, filtered_data, distribution_params, distribution_names)

    plt.tight_layout()
    st.pyplot(fig1)

    # Second Plot: Goodness of Fit Comparison
    fig2, ax = plt.subplots(figsize=(15, 5))
    bar_width = 0.35
    x = np.arange(len(tickers_to_analyze))

    distribution_names = results[tickers_to_analyze[0]][2]  # Assuming same distributions for both
    
    for i, distribution_name in enumerate(distribution_names):
        mape_values = [results[ticker][1][i] for ticker in tickers_to_analyze]
        ax.bar(x + i * bar_width, mape_values, bar_width, label=distribution_name)

    ax.set_xticks(x + bar_width / 2)
    ax.set_xticklabels(tickers_to_analyze)
    ax.set_title('Goodness of Fit Comparison - Mean Absolute Percentage Error')
    ax.set_xlabel('Ticker')
    ax.set_ylabel('MAPE [%]')
    ax.legend()
    ax.grid(axis='y')

    st.pyplot(fig2)

if __name__ == '__main__':
    main()
