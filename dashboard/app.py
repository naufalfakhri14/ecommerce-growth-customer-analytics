from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title='E-Commerce Growth & Customer Analytics',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='expanded'
)


# --------------------------------------------------
# Theme
# --------------------------------------------------

PRIMARY = '#5A4636'
PRIMARY_DARK = '#3E3027'
ACCENT = '#A8785A'
ACCENT_LIGHT = '#D8BDAA'
GREEN = '#6F8267'
RED = '#B56F63'
BG = '#F6F1EB'
CARD = '#FFFCF8'
CARD_ALT = '#F1E9E1'
TEXT = '#2E2925'
MUTED = '#766C64'
BORDER = '#E2D7CD'
WHITE = '#FFFFFF'

st.markdown(
    f'''\
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    [data-testid="stSidebar"] {{
        background: {CARD_ALT};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{
        color: {TEXT};
    }}

    [data-testid="stSidebar"] .stRadio > label {{
        font-weight: 600;
    }}

    h1, h2, h3 {{
        color: {PRIMARY_DARK};
        letter-spacing: -0.02em;
    }}

    h1 {{
        font-family: 'Playfair Display', serif;
        font-size: 2.55rem;
        line-height: 1.05;
        margin-bottom: 0.2rem;
    }}

    h2 {{
        font-size: 1.5rem;
        margin-top: 1.1rem;
        margin-bottom: 0.35rem;
    }}

    h3 {{
        font-size: 1.05rem;
    }}

    .hero-kicker {{
        color: {ACCENT};
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }}

    .subtitle {{
        color: {MUTED};
        font-size: 1.02rem;
        margin-bottom: 1rem;
    }}

    .section-label {{
        color: {PRIMARY};
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        margin-top: 1rem;
        margin-bottom: 0.35rem;
    }}

    .section-copy {{
        color: {MUTED};
        font-size: 0.91rem;
        margin-bottom: 0.7rem;
    }}

    .kpi-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 17px 18px 15px 18px;
        min-height: 122px;
        box-shadow: 0 4px 16px rgba(76, 55, 40, 0.05);
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
    }}

    .kpi-value {{
        color: {PRIMARY_DARK};
        font-size: 1.72rem;
        font-weight: 700;
        margin-top: 5px;
        line-height: 1.1;
    }}

    .kpi-note {{
        color: {MUTED};
        font-size: 0.79rem;
        margin-top: 7px;
    }}

    .signal-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-left: 4px solid {ACCENT};
        border-radius: 14px;
        padding: 14px 15px;
        min-height: 120px;
        box-shadow: 0 3px 12px rgba(76, 55, 40, 0.04);
    }}

    .signal-title {{
        color: {PRIMARY};
        font-size: 0.83rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 6px;
    }}

    .signal-value {{
        color: {TEXT};
        font-size: 1rem;
        line-height: 1.4;
    }}

    .priority-card {{
        background: {PRIMARY_DARK};
        color: {WHITE};
        border-radius: 16px;
        padding: 17px 18px;
        min-height: 126px;
    }}

    .priority-title {{
        color: {ACCENT_LIGHT};
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .priority-body {{
        color: {WHITE};
        font-size: 0.94rem;
        line-height: 1.45;
    }}

    .takeaway {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 15px 17px;
        margin-bottom: 8px;
    }}

    .takeaway strong {{
        color: {PRIMARY};
    }}

    .footer-note {{
        color: {MUTED};
        font-size: 0.74rem;
        margin-top: 1.25rem;
        padding-top: 0.8rem;
        border-top: 1px solid {BORDER};
    }}

    .stDownloadButton button {{
        border-radius: 10px;
        border: 1px solid {BORDER};
        background: {CARD};
        color: {PRIMARY_DARK};
        font-weight: 600;
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {BORDER};
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        padding: 8px 14px;
        border-radius: 10px;
    }}

    </style>
    ''',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Data loading
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
PROC_DIR = BASE_DIR / 'data' / 'processed'

REQUIRED_FILES = [
    'sales_monthly.csv',
    'customer_rfm.csv',
    'customer_segments.csv',
    'delivery_review.csv',
    'product_performance.csv',
    'seller_performance.csv',
    'geographic_performance.csv'
]

missing = [f for f in REQUIRED_FILES if not (PROC_DIR / f).exists()]
if missing:
    st.error('Processed files are missing: ' + ', '.join(missing))
    st.info('Run the notebook first so the analytical CSV files are created in data/processed/.')
    st.stop()


@st.cache_data

def load_data():
    sales = pd.read_csv(PROC_DIR / 'sales_monthly.csv')
    rfm = pd.read_csv(PROC_DIR / 'customer_rfm.csv')
    segments = pd.read_csv(PROC_DIR / 'customer_segments.csv')
    delivery = pd.read_csv(PROC_DIR / 'delivery_review.csv')
    product = pd.read_csv(PROC_DIR / 'product_performance.csv')
    seller = pd.read_csv(PROC_DIR / 'seller_performance.csv')
    geo = pd.read_csv(PROC_DIR / 'geographic_performance.csv')

    sales['year_month'] = pd.to_datetime(sales['year_month'])

    delivery['late_delivery'] = (
        delivery['late_delivery']
        .astype(str)
        .str.strip()
        .str.lower()
        .eq('true')
    )

    for col in ['revenue', 'aov']:
        sales[col] = pd.to_numeric(sales[col], errors='coerce')

    return sales, rfm, segments, delivery, product, seller, geo


sales, rfm, segments, delivery, product, seller, geo = load_data()


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def money(value):
    return f'R$ {value:,.0f}'.replace(',', '.')


def money_short(value):
    value = float(value)
    if value >= 1_000_000:
        return f'R$ {value / 1_000_000:.2f}M'
    if value >= 1_000:
        return f'R$ {value / 1_000:.0f}K'
    return f'R$ {value:,.0f}'.replace(',', '.')


def number(value):
    return f'{int(round(value)):,}'.replace(',', '.')


def pct(value):
    return f'{float(value):.1f}%'


def style_fig(fig, height=370):
    fig.update_layout(
        template='simple_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color=TEXT, size=12),
        title_font=dict(family='DM Sans', color=PRIMARY_DARK, size=17),
        margin=dict(l=8, r=8, t=48, b=8),
        height=height,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font_color=TEXT),
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER, zeroline=False)
    fig.update_yaxes(gridcolor=BORDER, gridwidth=0.7, zeroline=False)
    return fig


def empty_chart(message='No data available for this selection.'):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref='paper',
        yref='paper',
        showarrow=False,
        font=dict(size=14, color=MUTED)
    )
    fig.update_layout(
        template='simple_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=340,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    return fig


def kpi_card(label, value, note):
    return f'''<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>'''


def signal_card(title, body):
    return f'''<div class="signal-card">
        <div class="signal-title">{title}</div>
        <div class="signal-value">{body}</div>
    </div>'''


def priority_card(title, body):
    return f'''<div class="priority-card">
        <div class="priority-title">{title}</div>
        <div class="priority-body">{body}</div>
    </div>'''


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown('## E-Commerce Analytics')
    st.caption('Decision-support dashboard for sales, customer value, and experience.')

    page = st.radio(
        'Views',
        ['Executive Overview', 'Customer & Experience', 'Product & Geography'],
        label_visibility='visible'
    )

    st.markdown('---')
    st.markdown('### Filters')

    min_date = sales['year_month'].min().date()
    max_date = sales['year_month'].max().date()

    date_range = st.date_input(
        'Sales period',
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    segment_options = ['All Segments'] + sorted(segments['segment'].dropna().unique().tolist())
    selected_segment = st.selectbox('Customer segment', segment_options)

    state_options = ['All States'] + sorted(geo['customer_state'].dropna().unique().tolist())
    selected_state = st.selectbox('Customer state', state_options)

    top_n = st.slider('Top N items', 5, 15, 8)

    st.markdown('---')
    st.caption('Source: processed analytical datasets generated from the project notebook.')


# --------------------------------------------------
# Common filters
# --------------------------------------------------

sales_filtered = sales[
    (sales['year_month'].dt.date >= start_date) &
    (sales['year_month'].dt.date <= end_date)
].copy()

if selected_segment == 'All Segments':
    segments_filtered = segments.copy()
    rfm_filtered = rfm.copy()
else:
    segments_filtered = segments[segments['segment'] == selected_segment].copy()
    rfm_filtered = rfm[rfm['segment'] == selected_segment].copy()

if selected_state == 'All States':
    geo_filtered = geo.copy()
else:
    geo_filtered = geo[geo['customer_state'] == selected_state].copy()


# --------------------------------------------------
# Executive Overview
# --------------------------------------------------

if page == 'Executive Overview':
    st.markdown('<div class="hero-kicker">Management view</div>', unsafe_allow_html=True)
    st.title('E-Commerce Growth & Customer Analytics')
    st.markdown(
        '<div class="subtitle">A focused view of sales performance, customer value, and operational experience.</div>',
        unsafe_allow_html=True
    )

    total_transaction_value = sales_filtered['revenue'].sum()
    total_orders = sales_filtered['orders'].sum()
    delivered_customers = rfm['customer_unique_id'].nunique()
    avg_order_value = total_transaction_value / total_orders if total_orders else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card('Transaction Value', money_short(total_transaction_value), 'Aggregated payment value'), unsafe_allow_html=True)
    k2.markdown(kpi_card('Orders', number(total_orders), 'Order volume in selected period'), unsafe_allow_html=True)
    k3.markdown(kpi_card('Delivered Customers', number(delivered_customers), 'Unique customers in RFM base'), unsafe_allow_html=True)
    k4.markdown(kpi_card('Average Order Value', money(avg_order_value), 'Transaction value ÷ orders'), unsafe_allow_html=True)

    st.markdown('<div class="section-label">Key business signals</div>', unsafe_allow_html=True)
    signal_cols = st.columns(3)

    if not sales_filtered.empty:
        top_month = sales_filtered.loc[sales_filtered['revenue'].idxmax()]
        signal_cols[0].markdown(
            signal_card(
                'Peak sales month',
                f'<b>{top_month.year_month:%B %Y}</b> delivered {money(top_month.revenue)} in transaction value across {number(top_month.orders)} orders.'
            ),
            unsafe_allow_html=True
        )

    at_risk = segments[segments['segment'] == 'At Risk']
    if not at_risk.empty:
        row = at_risk.iloc[0]
        signal_cols[1].markdown(
            signal_card(
                'Retention opportunity',
                f'<b>{number(row.customers)} At Risk customers</b> account for {pct(row.revenue_share)} of customer revenue.'
            ),
            unsafe_allow_html=True
        )

    delivery_summary = delivery.groupby('late_delivery').agg(
        orders=('order_id', 'count'),
        average_review=('review_score', 'mean')
    ).reset_index()
    if not delivery_summary.empty:
        on_time = delivery_summary.loc[delivery_summary['late_delivery'] == False, 'average_review']
        late = delivery_summary.loc[delivery_summary['late_delivery'] == True, 'average_review']
        if not on_time.empty and not late.empty:
            gap = on_time.iloc[0] - late.iloc[0]
            signal_cols[2].markdown(
                signal_card(
                    'Customer experience',
                    f'Late orders average <b>{late.iloc[0]:.2f}</b> review score vs <b>{on_time.iloc[0]:.2f}</b> for on-time orders — a {gap:.2f}-point gap.'
                ),
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-label">Sales performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Use the date filter to explore the core sales period while keeping monthly performance comparable.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.45, 1])

    with c1:
        if not sales_filtered.empty:
            fig = px.line(
                sales_filtered,
                x='year_month',
                y='revenue',
                markers=True,
                title='Monthly Transaction Value'
            )
            fig.update_traces(line=dict(color=PRIMARY, width=3), marker=dict(color=ACCENT, size=7))
            fig.update_yaxes(title='Transaction value')
            fig.update_xaxes(title='', tickformat='%b\n%Y')
            fig = style_fig(fig, 390)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    with c2:
        if not sales_filtered.empty:
            fig = px.line(
                sales_filtered,
                x='year_month',
                y='aov',
                markers=True,
                title='Average Order Value'
            )
            fig.update_traces(line=dict(color=ACCENT, width=3), marker=dict(color=PRIMARY, size=7))
            fig.update_yaxes(title='AOV')
            fig.update_xaxes(title='', tickformat='%b\n%Y')
            fig = style_fig(fig, 390)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    st.markdown('<div class="section-label">Executive takeaways</div>', unsafe_allow_html=True)

    takeaway_cols = st.columns(3)
    top_category = product.sort_values('revenue', ascending=False).iloc[0] if not product.empty else None

    if top_category is not None:
        takeaway_cols[0].markdown(
            f'''<div class="takeaway"><strong>Commercial driver</strong><br>
            {top_category.product_category_name_english} is the leading product category in the processed sales dataset, with {money(top_category.revenue)} in category value.</div>''',
            unsafe_allow_html=True
        )

    new_potential = segments[segments['segment'] == 'New / Potential']
    if not new_potential.empty:
        row = new_potential.iloc[0]
        takeaway_cols[1].markdown(
            f'''<div class="takeaway"><strong>Growth opportunity</strong><br>
            New / Potential customers represent {pct(row.revenue_share)} of customer revenue and are a natural focus for second-purchase conversion.</div>''',
            unsafe_allow_html=True
        )

    takeaway_cols[2].markdown(
        '''<div class="takeaway"><strong>Operational priority</strong><br>
        Delivery reliability should be monitored closely because late orders are associated with materially lower review scores in the analysis.</div>''',
        unsafe_allow_html=True
    )

    p1, p2, p3 = st.columns(3)
    p1.markdown(priority_card('1 · Grow repeat purchases', 'Move New / Potential customers toward a second purchase with targeted follow-up and relevant offers.'), unsafe_allow_html=True)
    p2.markdown(priority_card('2 · Reactivate value', 'Prioritize At Risk customers with relatively high historical spend for reactivation campaigns.'), unsafe_allow_html=True)
    p3.markdown(priority_card('3 · Protect experience', 'Reduce late deliveries in underperforming operational areas and sellers.'), unsafe_allow_html=True)

    st.markdown(
        '<div class="footer-note">Metric note: “Transaction Value” uses aggregated payment value from the processed order-level data. Customer analysis is based on delivered orders and unique customer IDs.</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Customer & Experience
# --------------------------------------------------

elif page == 'Customer & Experience':
    st.markdown('<div class="hero-kicker">Customer intelligence</div>', unsafe_allow_html=True)
    st.title('Customer & Experience')
    st.markdown(
        '<div class="subtitle">Identify customer value, retention opportunities, and experience risks.</div>',
        unsafe_allow_html=True
    )

    seg_display = segments_filtered.sort_values('total_revenue', ascending=False).copy()

    if selected_segment == 'All Segments':
        customer_count = rfm.shape[0]
        avg_monetary = rfm['monetary'].mean()
    else:
        customer_count = rfm_filtered.shape[0]
        avg_monetary = rfm_filtered['monetary'].mean() if not rfm_filtered.empty else 0

    champions = segments[segments['segment'] == 'Champions']
    at_risk = segments[segments['segment'] == 'At Risk']

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_card('Customer Base', number(customer_count), 'Customers in selected segment scope'), unsafe_allow_html=True)
    c2.markdown(kpi_card('Avg. Monetary', money(avg_monetary), 'Average transaction value per customer'), unsafe_allow_html=True)
    c3.markdown(kpi_card('At Risk Revenue', pct(at_risk.iloc[0].revenue_share) if not at_risk.empty else '—', 'Share of total customer revenue'), unsafe_allow_html=True)
    c4.markdown(kpi_card('Champion Base', number(champions.iloc[0].customers) if not champions.empty else '—', 'Highest-priority repeat customers'), unsafe_allow_html=True)

    st.markdown('<div class="section-label">Customer segmentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">RFM segments are built from Recency, Frequency, and Monetary behavior and validated against repeat-purchase activity.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])

    with c1:
        if not seg_display.empty:
            fig = px.bar(
                seg_display.sort_values('total_revenue'),
                x='total_revenue',
                y='segment',
                orientation='h',
                text='revenue_share',
                title='Customer Revenue by Segment'
            )
            fig.update_traces(
                marker_color=ACCENT,
                texttemplate='%{text:.1f}%',
                textposition='outside'
            )
            fig.update_xaxes(title='Transaction value')
            fig.update_yaxes(title='')
            fig = style_fig(fig, 390)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    with c2:
        if not seg_display.empty:
            fig = px.pie(
                seg_display,
                names='segment',
                values='customers',
                hole=0.58,
                title='Customer Mix'
            )
            fig.update_traces(
                textposition='outside',
                marker=dict(line=dict(color=CARD, width=2))
            )
            fig = style_fig(fig, 390)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    if not seg_display.empty:
        display_cols = [
            'segment', 'customers', 'avg_recency', 'avg_frequency',
            'avg_monetary', 'repeat_customer_rate', 'revenue_share'
        ]
        table = seg_display[display_cols].copy()
        table.columns = [
            'Segment', 'Customers', 'Avg Recency (days)', 'Avg Frequency',
            'Avg Monetary', 'Repeat Rate (%)', 'Revenue Share (%)'
        ]
        table['Avg Recency (days)'] = table['Avg Recency (days)'].round(0).astype(int)
        table['Avg Frequency'] = table['Avg Frequency'].round(2)
        table['Avg Monetary'] = table['Avg Monetary'].round(2)
        table['Repeat Rate (%)'] = table['Repeat Rate (%)'].round(1)
        table['Revenue Share (%)'] = table['Revenue Share (%)'].round(1)
        st.dataframe(table, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label">Delivery & customer satisfaction</div>', unsafe_allow_html=True)

    delivery_summary = delivery.groupby('late_delivery').agg(
        orders=('order_id', 'count'),
        average_review=('review_score', 'mean'),
        average_delivery_days=('delivery_days', 'mean')
    ).reset_index()
    delivery_summary['status'] = delivery_summary['late_delivery'].map({False: 'On Time', True: 'Late'})

    d1, d2 = st.columns([1, 1.25])

    with d1:
        if not delivery_summary.empty:
            fig = px.bar(
                delivery_summary,
                x='status',
                y='average_review',
                title='Average Review Score by Delivery Status',
                text='average_review'
            )
            fig.update_traces(marker_color=ACCENT, texttemplate='%{text:.2f}', textposition='outside')
            fig.update_yaxes(title='Review score', range=[0, 5])
            fig.update_xaxes(title='')
            fig = style_fig(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    with d2:
        if not delivery.empty:
            fig = px.scatter(
                delivery.sample(min(6000, len(delivery)), random_state=42),
                x='delivery_days',
                y='review_score',
                color='late_delivery',
                opacity=0.28,
                title='Delivery Time vs Review Score',
                labels={'delivery_days': 'Delivery days', 'review_score': 'Review score', 'late_delivery': 'Late delivery'}
            )
            fig.update_traces(marker=dict(size=6))
            fig.update_layout(coloraxis_colorbar_title='Late delivery')
            fig = style_fig(fig, 360)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    if not delivery_summary.empty:
        on_time = delivery_summary.loc[delivery_summary['late_delivery'] == False]
        late = delivery_summary.loc[delivery_summary['late_delivery'] == True]
        if not on_time.empty and not late.empty:
            gap = on_time.iloc[0]['average_review'] - late.iloc[0]['average_review']
            st.markdown(
                f'''<div class="signal-card"><div class="signal-title">Experience finding</div>
                <div class="signal-value">On-time orders average <b>{on_time.iloc[0]['average_review']:.2f}</b> review score, compared with <b>{late.iloc[0]['average_review']:.2f}</b> for late orders. The {gap:.2f}-point difference indicates a strong association between delivery performance and customer satisfaction.</div></div>''',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-label">RFM profile</div>', unsafe_allow_html=True)
    if not rfm_filtered.empty:
        a, b, c = st.columns(3)
        a.markdown(kpi_card('Median Recency', f"{rfm_filtered['recency'].median():.0f} days", 'Lower is more recent'), unsafe_allow_html=True)
        b.markdown(kpi_card('Median Frequency', f"{rfm_filtered['frequency'].median():.0f}", 'Orders per customer'), unsafe_allow_html=True)
        c.markdown(kpi_card('Median Monetary', money(rfm_filtered['monetary'].median()), 'Customer-level transaction value'), unsafe_allow_html=True)

    st.download_button(
        'Download RFM data',
        rfm_filtered.to_csv(index=False).encode('utf-8'),
        file_name='customer_rfm_filtered.csv',
        mime='text/csv'
    )


# --------------------------------------------------
# Product & Geography
# --------------------------------------------------

else:
    st.markdown('<div class="hero-kicker">Commercial intelligence</div>', unsafe_allow_html=True)
    st.title('Product & Geography')
    st.markdown(
        '<div class="subtitle">Understand which product categories, sellers, and customer regions contribute most to performance.</div>',
        unsafe_allow_html=True
    )

    top_cat = product.sort_values('revenue', ascending=False).head(top_n).copy()
    top_seller = seller.sort_values('revenue', ascending=False).head(top_n).copy()
    top_state = geo_filtered.sort_values('revenue', ascending=False).head(top_n).copy()

    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi_card('Leading Category', top_cat.iloc[0]['product_category_name_english'] if not top_cat.empty else '—', 'Highest category value'), unsafe_allow_html=True)
    c2.markdown(kpi_card('Top Seller Value', money_short(top_seller.iloc[0]['revenue']) if not top_seller.empty else '—', 'Highest seller contribution'), unsafe_allow_html=True)
    c3.markdown(kpi_card('Top State', top_state.iloc[0]['customer_state'] if not top_state.empty else '—', 'Highest customer-state value'), unsafe_allow_html=True)

    st.markdown('<div class="section-label">Product categories</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        if not top_cat.empty:
            fig = px.bar(
                top_cat.sort_values('revenue'),
                x='revenue',
                y='product_category_name_english',
                orientation='h',
                title=f'Top {top_n} Categories by Transaction Value'
            )
            fig.update_traces(marker_color=ACCENT)
            fig.update_xaxes(title='Transaction value')
            fig.update_yaxes(title='')
            fig = style_fig(fig, 410)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    with c2:
        if not top_cat.empty:
            fig = px.bar(
                top_cat.sort_values('items_sold'),
                x='items_sold',
                y='product_category_name_english',
                orientation='h',
                title=f'Top {top_n} Categories by Items Sold'
            )
            fig.update_traces(marker_color=GREEN)
            fig.update_xaxes(title='Items sold')
            fig.update_yaxes(title='')
            fig = style_fig(fig, 410)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    st.markdown('<div class="section-label">Seller performance</div>', unsafe_allow_html=True)
    if not top_seller.empty:
        fig = px.bar(
            top_seller.sort_values('revenue'),
            x='revenue',
            y='seller_id',
            orientation='h',
            title=f'Top {top_n} Sellers by Product Value'
        )
        fig.update_traces(marker_color=PRIMARY)
        fig.update_xaxes(title='Product value')
        fig.update_yaxes(title='Seller ID')
        fig = style_fig(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-label">Geographic performance</div>', unsafe_allow_html=True)
    g1, g2 = st.columns([1.35, 1])

    with g1:
        if not top_state.empty:
            fig = px.bar(
                top_state.sort_values('revenue'),
                x='revenue',
                y='customer_state',
                orientation='h',
                title=f'Top {top_n} Customer States by Transaction Value'
            )
            fig.update_traces(marker_color=ACCENT)
            fig.update_xaxes(title='Transaction value')
            fig.update_yaxes(title='State')
            fig = style_fig(fig, 420)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    with g2:
        if not top_state.empty:
            share = top_state[['customer_state', 'revenue_share']].copy()
            fig = px.bar(
                share.sort_values('revenue_share'),
                x='revenue_share',
                y='customer_state',
                orientation='h',
                title='Revenue Share by State'
            )
            fig.update_traces(marker_color=GREEN, text=share.revenue_share, texttemplate='%{x:.1f}%', textposition='outside')
            fig.update_xaxes(title='Revenue share (%)')
            fig.update_yaxes(title='State')
            fig = style_fig(fig, 420)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.plotly_chart(empty_chart(), use_container_width=True)

    if not top_state.empty:
        state_table = top_state[['customer_state', 'orders', 'customers', 'revenue', 'revenue_share']].copy()
        state_table.columns = ['State', 'Orders', 'Customers', 'Transaction Value', 'Revenue Share (%)']
        state_table['Transaction Value'] = state_table['Transaction Value'].round(2)
        state_table['Revenue Share (%)'] = state_table['Revenue Share (%)'].round(1)
        st.dataframe(state_table, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label">Commercial readout</div>', unsafe_allow_html=True)
    top_state_name = top_state.iloc[0]['customer_state'] if not top_state.empty else '—'
    top_cat_name = top_cat.iloc[0]['product_category_name_english'] if not top_cat.empty else '—'
    st.markdown(
        f'''<div class="signal-card"><div class="signal-title">What this view is for</div>
        <div class="signal-value">Use category performance to inform assortment and commercial prioritization. Use seller rankings to identify high-contribution partners, and use geography to understand where demand is concentrated. In the current selection, <b>{top_cat_name}</b> is the leading category and <b>{top_state_name}</b> is the leading customer state by transaction value.</div></div>''',
        unsafe_allow_html=True
    )

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            'Download product performance',
            product.to_csv(index=False).encode('utf-8'),
            file_name='product_performance.csv',
            mime='text/csv'
        )
    with d2:
        st.download_button(
            'Download geographic performance',
            geo_filtered.to_csv(index=False).encode('utf-8'),
            file_name='geographic_performance_filtered.csv',
            mime='text/csv'
        )

    st.markdown(
        '<div class="footer-note">The dashboard uses processed analytical datasets generated from the project notebook. Geographic and customer metrics are presented at aggregated level.</div>',
        unsafe_allow_html=True
    )
