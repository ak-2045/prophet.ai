import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ChartService:
    # ----------------------------------
    # Candlestick Chart
    # ----------------------------------
    @staticmethod
    def create_candlestick_chart(df):

        fig = go.Figure()

        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price"
            )
        )

        fig.update_layout(
            title="Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            height=700,
            xaxis_rangeslider_visible=False
        )

        return fig

    # ----------------------------------
    # Closing Price Trend
    # ----------------------------------
    @staticmethod
    def create_price_chart(df):

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.update_layout(
            title="Price Trend",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",
            height=500
        )

        return fig

    # ----------------------------------
    # Volume Chart
    # ----------------------------------
    @staticmethod
    def create_volume_chart(df):

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df["Volume"],
                name="Volume"
            )
        )

        fig.update_layout(
            title="Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume",
            template="plotly_dark",
            height=300
        )

        return fig

    # ----------------------------------
    # Combined Trading Dashboard
    # ----------------------------------
    @staticmethod
    def create_market_dashboard(df):

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.75, 0.25]
        )

        # Candlesticks
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Price"
            ),
            row=1,
            col=1
        )

        # Volume
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df["Volume"],
                name="Volume"
            ),
            row=2,
            col=1
        )

        fig.update_layout(
            title="Market Dashboard",
            template="plotly_dark",
            height=850,
            xaxis_rangeslider_visible=False
        )

        return fig
