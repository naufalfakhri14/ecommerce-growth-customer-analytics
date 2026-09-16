# E-Commerce Growth & Customer Analytics

An end-to-end analytics project focused on understanding **sales performance, customer value, customer experience, product performance, and geographic patterns** in an e-commerce business.

The project combines data preparation, exploratory analysis, customer segmentation, business analysis, and an interactive Streamlit dashboard to turn transaction data into actionable insights.

> **Dataset:** Olist Brazilian E-Commerce Public Dataset  
> **Analysis period:** September 2016 – October 2018  
> **Primary tools:** Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn, Plotly, Streamlit

---

## Business Context

An e-commerce business needs to understand what is driving its performance and where improvement opportunities exist.

This project looks at the business from several perspectives:

- How is sales performance changing over time?
- Which customer groups contribute the most value?
- Is delivery performance associated with customer satisfaction?
- Which product categories and sellers contribute most to sales?
- Which geographic areas generate the most orders and transaction value?
- What actions could help improve repeat purchases, customer retention, and operational performance?

The goal is not only to describe the data, but to translate the findings into **business-oriented recommendations**.

---

## Key Business Questions

### 1. Sales Performance
How are revenue, order volume, and average order value changing over time?

### 2. Customer Experience
Is delivery performance associated with customer review scores?

### 3. Customer Value
Which customer segments are the most valuable, and which groups should be prioritized for retention or reactivation?

### 4. Product & Seller Performance
Which product categories and sellers contribute the most to transaction value and order volume?

### 5. Geographic Performance
Which customer states contribute the most to orders and transaction value?

---

## Dataset

The analysis uses multiple tables from the Olist Brazilian E-Commerce Public Dataset.

| Dataset | Rows | Purpose |
|---|---:|---|
| Customers | 99,441 | Customer identity and location |
| Orders | 99,441 | Order status and timestamps |
| Order Items | 112,650 | Products purchased in each order |
| Payments | 103,886 | Payment information |
| Reviews | 99,224 | Customer review scores and comments |
| Products | 32,951 | Product information |
| Sellers | 3,095 | Seller information |
| Geolocation | 1,000,163 | Geographic information |
| Category Translation | — | Portuguese-to-English product categories |

The raw datasets are used for analysis, while the dashboard reads processed analytical datasets generated from the notebook.

---

# Analysis Workflow

The project is organized around a single main notebook:

`notebooks/ecommerce_growth_customer_analytics.ipynb`

The workflow follows:

```text
Business Questions
       ↓
Data Audit
       ↓
Data Preparation
       ↓
Sales Analysis
       ↓
Customer Experience Analysis
       ↓
RFM Customer Segmentation
       ↓
Product & Seller Analysis
       ↓
Geographic Analysis
       ↓
Business Insights
       ↓
Recommendations
       ↓
Processed Data
       ↓
Streamlit Dashboard
```

---

## 1. Data Quality & Preparation

Before analysis, the datasets are audited for:

- Missing values
- Duplicate records
- Data types
- Order status
- Key relationships between tables

Missing values are handled according to their business meaning rather than automatically removing or imputing them.

For example, delivery timestamps are not filled artificially because an unavailable delivery date can indicate an order that was not completed.

Date columns are converted into datetime format to support time-based and delivery analysis.

---

## 2. Sales Performance Analysis

Sales performance is analyzed using order and payment data.

### Main metrics

- Total transaction value
- Total orders
- Customer count
- Average order value
- Monthly revenue
- Monthly orders
- Monthly AOV

Because the payment table can contain multiple records for the same order, payment values are first aggregated at the order level before being combined with order information.

For this project, `payment_value` is used as a **transaction value proxy** rather than accounting revenue.

### Core Sales Period

The dataset contains very small partial months at the beginning and end of the observation period.

To avoid misleading month-to-month comparisons, the main sales analysis focuses on months with at least **1,000 orders**, resulting in a core period from:

**February 2017 – August 2018**

### Example finding

November 2017 recorded the highest revenue in the core period:

- Revenue: **1.19M**
- Orders: **7,544**
- AOV: **158.39**

The analysis also compares revenue with order volume and AOV to distinguish between growth driven by transaction volume and growth driven by order value.

---

## 3. Customer Experience Analysis

Customer experience is evaluated by combining delivery information with review scores.

### Metrics

- Delivery days
- Estimated delivery date
- Late delivery flag
- Average review score

Only orders with an actual customer delivery date are used for delivery-time analysis.

### Key finding

| Delivery Status | Average Review Score |
|---|---:|
| On Time | **4.29** |
| Late | **2.57** |

Late orders received substantially lower average review scores than orders delivered on time.

This indicates a strong **association** between delivery performance and customer satisfaction in the dataset. The analysis does not claim that late delivery alone causes lower ratings.

---

## 4. RFM Customer Segmentation

RFM analysis is used to understand customer purchasing behavior.

### RFM Metrics

**Recency**  
How recently the customer made a purchase.

**Frequency**  
How many orders the customer has made.

**Monetary**  
The total payment value associated with the customer's delivered orders.

The analysis uses `customer_unique_id` to identify customers across multiple orders.

### Customer Segments

Customers are grouped into five business-oriented segments:

| Segment | Business Meaning |
|---|---|
| **Champions** | Repeat customers who are relatively recent and have high monetary value |
| **Loyal Customers** | Customers who have made multiple purchases |
| **At Risk** | Higher-value customers who have not purchased recently |
| **New / Potential** | Relatively recent customers who have not yet become repeat buyers |
| **Hibernating** | Customers with low recent activity and lower spending |

### Key findings

- **New / Potential:** 45,252 customers and **47.45%** of customer revenue
- **At Risk:** 21,783 customers and **37.24%** of customer revenue
- **Champions:** 989 customers with an average frequency of **2.18** and average monetary value of **372.35**
- **Loyal Customers:** 1,812 customers with an average frequency of **2.08**

The results highlight two major opportunities:

1. Convert **New / Potential** customers into repeat buyers.
2. Reactivate higher-value **At Risk** customers.

Champions and Loyal Customers should be prioritized for retention initiatives.

---

## 5. Product Performance

Product-level analysis combines order item and product information with category translation.

The analysis identifies:

- Orders by category
- Items sold
- Transaction value by category

### Top categories by transaction value

| Product Category | Transaction Value |
|---|---:|
| bed_bath_table | **1.71M** |
| health_beauty | **1.66M** |
| computers_accessories | **1.59M** |
| furniture_decor | **1.43M** |
| watches_gifts | **1.43M** |

These results help identify product categories that contribute strongly to the business and may deserve greater commercial attention.

---

## 6. Seller Performance

Seller performance is analyzed using order item data.

Metrics include:

- Orders
- Items sold
- Seller transaction value

Seller transaction value is based on the `price` recorded in `order_items` rather than total payment value, since customer payments can also include freight and other payment components.

---

## 7. Geographic Analysis

Customer location is used to understand regional performance.

Metrics include:

- Orders
- Customers
- Transaction value
- Revenue share

This analysis helps identify regions with a larger customer base and stronger commercial contribution.

---

# Executive Insights

The analysis highlights several business signals:

### Customer retention is a major opportunity

Most customers in the dataset made only one purchase. A large share of transaction value comes from customers who have not yet become repeat buyers or have become inactive.

### High-value inactive customers deserve attention

The At Risk segment contributes a significant share of customer revenue while showing relatively high recency values.

This makes reactivation a potentially valuable retention strategy.

### Delivery performance is strongly associated with satisfaction

Late orders have a much lower average review score than on-time orders.

Improving delivery reliability may therefore be an important area for customer experience improvement.

### Revenue is driven by more than order volume

High-revenue months do not always have the highest AOV.

Monitoring both **order volume** and **average order value** provides a better view of sales performance.

---

# Business Recommendations

Based on the analysis, several actions can be considered:

### 1. Increase Repeat Purchases

Develop post-purchase engagement for New / Potential customers to encourage a second transaction.

### 2. Reactivate High-Value Customers

Identify At Risk customers with high historical spending and target them with personalized reactivation campaigns.

### 3. Retain High-Value Repeat Customers

Maintain engagement with Champions and Loyal Customers through loyalty benefits, relevant offers, and personalized communication.

### 4. Improve Delivery Reliability

Monitor sellers and regions with higher delivery delays and prioritize operational improvements.

### 5. Focus on High-Contributing Categories

Use product-category performance to support inventory, promotion, and commercial planning.

---

# Interactive Dashboard

The project includes a Streamlit dashboard designed to provide a management-oriented view of the analysis.

### Dashboard Sections

**Executive Overview**
- Revenue
- Orders
- Customers
- Average Order Value
- Sales trends
- Key business signals

**Customer & Experience**
- RFM segmentation
- Customer value
- Delivery performance
- Review analysis

**Product & Geography**
- Product category performance
- Seller performance
- Geographic performance

### Interactivity

The dashboard includes filters for:

- Sales period
- Customer segment
- Customer state
- Top-N categories / sellers / states

The dashboard uses processed analytical datasets generated from the main notebook.

---

# Project Structure

```text
ecommerce-growth-customer-analytics/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── *.csv
│   │
│   └── processed/
│       ├── sales_monthly.csv
│       ├── customer_rfm.csv
│       ├── customer_segments.csv
│       ├── delivery_review.csv
│       ├── product_performance.csv
│       ├── seller_performance.csv
│       └── geographic_performance.csv
│
├── notebooks/
│   └── ecommerce_growth_customer_analytics.ipynb
│
├── dashboard/
│   ├── app.py
│   └── README.md
│
└── screenshots/
```

---

# Tools & Technologies

- Python
- Pandas
- NumPy
- SciPy
- Statsmodels
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook

---

# Skills Demonstrated

- Data Cleaning & Data Preparation
- Exploratory Data Analysis
- Business Analysis
- Sales Analytics
- Customer Analytics
- RFM Analysis
- Customer Segmentation
- Operational Analytics
- Product & Seller Analysis
- Geographic Analysis
- Data Visualization
- Dashboard Development
- Business Insight Generation

---

# How to Run

### 1. Clone the repository

```bash
git clone https://github.com/naufalfakhri14/ecommerce-growth-customer-analytics.git
cd ecommerce-growth-customer-analytics
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
python -m streamlit run dashboard/app.py
```

---

# Notes

This project uses the **Olist Brazilian E-Commerce Public Dataset** for portfolio and analytical purposes.

The analysis focuses on historical transactional data and is intended to demonstrate an end-to-end analytics workflow.

Several metrics use practical analytical definitions:

- `payment_value` is treated as a transaction value proxy.
- RFM Monetary is calculated from delivered orders with recorded payment values.
- Delivery and review analysis identifies association rather than causal impact.

The processed datasets used by the dashboard are generated from the main analysis notebook.
