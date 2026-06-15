import streamlit as st
from services.market_data import MarketDataService
from services.chart_services import ChartService
from services.market_structure import MarketStructureAnalyzer
from services.indicators import IndicatorAnalyzer
from services.risk_manager import RiskManager
from services.trade_setup import TradeSetupGenerator
from chains.explanation_chain import explanation_chain
import os

st.set_page_config(
    page_title="Prophet",
    page_icon="https://cdn-icons-png.flaticon.com/512/564/564398.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #080c14;
    color: #c8d6e8;
}

.stApp {
    background: #080c14;
}

.block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
}

.prophet-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    padding: 1.5rem 0 2.5rem 0;
    border-bottom: 1px solid #1a2640;
    margin-bottom: 2rem;
}

.prophet-header img {
    height: 42px;
    width: auto;
}

.prophet-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e8f4ff;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.prophet-caption {
    font-size: 0.75rem;
    color: #4a6080;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2e6fff;
    margin-bottom: 0.6rem;
    display: block;
}

.grid-card {
    background: #0d1520;
    border: 1px solid #1a2640;
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e8f4ff;
    letter-spacing: -0.02em;
}

.metric-label {
    font-size: 0.7rem;
    color: #4a6080;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
    margin-top: 0.2rem;
}

.trade-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 2px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.badge-long {
    background: rgba(0, 210, 120, 0.12);
    color: #00d278;
    border: 1px solid rgba(0, 210, 120, 0.3);
}

.badge-short {
    background: rgba(255, 60, 80, 0.12);
    color: #ff3c50;
    border: 1px solid rgba(255, 60, 80, 0.3);
}

.badge-neutral {
    background: rgba(46, 111, 255, 0.12);
    color: #2e6fff;
    border: 1px solid rgba(46, 111, 255, 0.3);
}

.setup-row {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid #111c2d;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
}

.setup-row:last-child {
    border-bottom: none;
}

.setup-key {
    color: #4a6080;
}

.setup-val {
    color: #c8d6e8;
}

.ai-mentor-box {
    background: #0a1220;
    border: 1px solid #1a2640;
    border-left: 3px solid #2e6fff;
    border-radius: 4px;
    padding: 1.6rem;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #a8bcd4;
}

.divider-line {
    border: none;
    border-top: 1px solid #1a2640;
    margin: 2rem 0;
}

.warning-tag {
    display: inline-block;
    background: rgba(255, 180, 0, 0.08);
    border: 1px solid rgba(255, 180, 0, 0.25);
    color: #ffb400;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    margin-right: 0.4rem;
    margin-top: 0.4rem;
    letter-spacing: 0.06em;
}

stRadio > div { flex-direction: row; gap: 1rem; }

div[data-testid="stRadio"] > div {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
}

div[data-testid="stRadio"] label {
    background: #0d1520;
    border: 1px solid #1a2640;
    border-radius: 3px;
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
    cursor: pointer;
    color: #4a6080;
}

div[data-testid="stRadio"] label:has(input:checked) {
    border-color: #2e6fff;
    color: #2e6fff;
    background: rgba(46, 111, 255, 0.08);
}

div[data-testid="stSelectbox"] > div,
div[data-testid="stTextInput"] > div > div,
div[data-testid="stNumberInput"] > div > div {
    background: #0d1520 !important;
    border: 1px solid #1a2640 !important;
    border-radius: 3px !important;
    color: #c8d6e8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
}

div[data-testid="stSlider"] > div {
    color: #2e6fff;
}

.stButton > button {
    background: #2e6fff !important;
    color: #fff !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    font-weight: 700 !important;
    transition: background 0.15s ease !important;
}

.stButton > button:hover {
    background: #1a55ee !important;
}

div[data-testid="stMetric"] {
    background: #0d1520;
    border: 1px solid #1a2640;
    border-radius: 4px;
    padding: 1rem 1.2rem;
}

div[data-testid="stMetric"] label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a6080 !important;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace;
    color: #e8f4ff !important;
    font-size: 1.2rem !important;
}

.structure-pill {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #00d278;
    margin-bottom: 0.5rem;
}

.rr-highlight {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    color: #2e6fff;
    font-weight: 700;
}

.prophecy-section {
    background: #0a1220;
    border: 1px solid #1a2640;
    border-left: 3px solid #2e6fff;
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-top: 0.5rem;
}

.prophecy-section p {
    color: #8aa0be;
    font-size: 0.88rem;
    line-height: 1.9;
    margin-bottom: 0.85rem;
}

.prophecy-section strong {
    color: #c8d6e8;
    font-weight: 600;
}

.prophecy-section ul {
    padding-left: 1.2rem;
    margin-bottom: 0.85rem;
}

.prophecy-section li {
    color: #7a95b4;
    font-size: 0.85rem;
    line-height: 1.8;
    margin-bottom: 0.4rem;
}

.prophecy-section li strong {
    color: #b8cce4;
}

.stMarkdown h3 {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #2e6fff !important;
    margin: 1.4rem 0 0.5rem 0 !important;
    border-bottom: 1px solid #1a2640 !important;
    padding-bottom: 0.4rem !important;
}

.stMarkdown h4 {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #4a6080 !important;
    margin: 1rem 0 0.3rem 0 !important;
}

.stMarkdown p {
    color: #8aa0be;
    font-size: 0.88rem;
    line-height: 1.9;
}

.stMarkdown ul li {
    color: #7a95b4;
    font-size: 0.85rem;
    line-height: 1.8;
}

.stMarkdown strong {
    color: #c8d6e8 !important;
}
</style>
""", unsafe_allow_html=True)

logo_path = "assets\images\prophet.png"

if os.path.exists(logo_path):
    h_logo, h_title = st.columns([0.4, 1], vertical_alignment="center")

    with h_logo:
        st.image(
            logo_path,
            use_container_width=True
        )

    with h_title:
        st.markdown("""
        <div style="
            height:100%;
            display:flex;
            flex-direction:column;
            justify-content:center;
            padding-left:1rem;
        ">
            <div class="prophet-title">PROPHET.ai</div>
            <div class="prophet-caption">
                INTELLIGENT TRADING MENTOR · MARKET ANALYSIS TERMINAL
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="prophet-header">
        <div class="prophet-title">PROPHET</div>
        <div class="prophet-caption">
            INTELLIGENT TRADING MENTOR · MARKET ANALYSIS TERMINAL
        </div>
    </div>
    """, unsafe_allow_html=True)

ASSETS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Tesla": "TSLA",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Dow Jones": "^DJI",
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Gold": "GC=F",
    "Other": "OTHER"
}

col_mode, col_spacer = st.columns([2, 5])
with col_mode:
    mode = st.radio(
        "Input Mode",
        ["Live Market Data", "Custom Data"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

if mode == "Live Market Data":

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        asset_name = st.selectbox("Asset", list(ASSETS.keys()))
        if asset_name == "Other":
            symbol = st.text_input("Ticker Symbol", placeholder="e.g. META")
        else:
            symbol = ASSETS[asset_name]

    with c2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=2)

    with c3:
        interval = st.selectbox("Interval", ["1d", "1h", "15m"])

else:

    c1, c2, c3 = st.columns(3)

    with c1:
        asset_name = st.text_input("Asset", value="BTC")
        price = st.number_input("Current Price", value=108000.0)

    with c2:
        rsi = st.slider("RSI", 0, 100, 68)
        volume = st.selectbox("Volume Trend", ["Increasing", "Decreasing", "Neutral"])

    with c3:
        support = st.number_input("Support Level", value=106500.0)
        resistance = st.number_input("Resistance Level", value=108100.0)

st.markdown("<br>", unsafe_allow_html=True)

analyze = st.button("Analyze Market", use_container_width=False)

if analyze:

    if mode == "Live Market Data":

        with st.spinner("Fetching market data..."):

            market_data = MarketDataService()
            market_data.set_asset(symbol)
            info = market_data.get_market_info()
            df = market_data.get_history(period=period, interval=interval)

            current_price = info["current_price"]
            prices = df["Close"].tolist()
            volume = "Neutral"
            support = df["Low"].tail(20).min()
            resistance = df["High"].tail(20).max()
            rsi = 50

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Price", current_price)
        with c2:
            st.metric("Volume", info["volume"])
        with c3:
            st.metric("Support", round(support, 2))
        with c4:
            st.metric("Resistance", round(resistance, 2))

        st.markdown("<br>", unsafe_allow_html=True)

        dashboard = ChartService.create_market_dashboard(df)
        st.plotly_chart(dashboard, use_container_width=True)

        price = current_price

    else:

        prices = [
            price * 0.98,
            price * 0.99,
            price,
            price * 1.01,
            price
        ]

    with st.spinner("Running analysis..."):

        market_service = MarketStructureAnalyzer()
        indicator_service = IndicatorAnalyzer()
        risk_service = RiskManager()
        trade_service = TradeSetupGenerator()

        market = market_service.analyze(
            prices=prices,
            current_price=price,
            support=support,
            resistance=resistance,
            volume=volume
        )

        indicators = indicator_service.analyze(
            current_price=price,
            rsi=rsi,
            volume=volume
        )

        entry = resistance
        stop_loss = support
        target = entry + abs(entry - stop_loss) * 2

        risk = risk_service.analyze(
            capital=100000,
            risk_percent=2,
            entry=entry,
            stop_loss=stop_loss,
            target=target
        )

        setup = trade_service.generate(
            current_price=price,
            support=support,
            resistance=resistance,
            market_structure=market,
            indicators=indicators,
            risk=risk
        )

        explanation = explanation_chain.invoke(
            {
                "market_structure": market["structure"],
                "market_reason": market["reason"],
                "bias": indicators["overall_bias"],
                "rsi": indicators["rsi_signal"],
                "volume": indicators["volume_signal"],
                "trade_type": setup["trade_type"],
                "entry": setup["entry"],
                "stop_loss": setup["stop_loss"],
                "target": setup["target"],
                "risk_reward": risk["risk_reward_ratio"],
                "warnings": ", ".join(setup["warnings"]) if setup["warnings"] else "None"
            }
        )

    st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<span class="section-label">Market Structure</span>', unsafe_allow_html=True)

        trade_type = setup["trade_type"].upper() if setup.get("trade_type") else "NEUTRAL"
        badge_cls = "badge-long" if "LONG" in trade_type else ("badge-short" if "SHORT" in trade_type else "badge-neutral")

        st.markdown(f'<div class="trade-badge {badge_cls}">{trade_type}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="structure-pill">{market["structure"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#6880a0;font-size:0.85rem;line-height:1.6;">{market["reason"]}</p>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<span class="section-label">Trade Setup</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:0.4rem;">
            <div class="setup-row"><span class="setup-key">Entry</span><span class="setup-val">{setup['entry']}</span></div>
            <div class="setup-row"><span class="setup-key">Stop Loss</span><span class="setup-val">{setup['stop_loss']}</span></div>
            <div class="setup-row"><span class="setup-key">Target</span><span class="setup-val">{setup['target']}</span></div>
            <div class="setup-row"><span class="setup-key">Risk / Reward</span><span class="rr-highlight">1 : {risk['risk_reward_ratio']}</span></div>
        </div>
        """, unsafe_allow_html=True)

        if setup.get("warnings"):
            st.markdown("<br>", unsafe_allow_html=True)
            warnings_html = "".join([f'<span class="warning-tag">⚠ {w}</span>' for w in setup["warnings"]])
            st.markdown(warnings_html, unsafe_allow_html=True)

    st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family:\'Space Mono\',monospace;font-size:2rem;color:#F5D21F ;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:1rem;">— Our Prophecy —</p>', unsafe_allow_html=True)
    st.markdown(explanation)
    st.markdown('</div>', unsafe_allow_html=True)