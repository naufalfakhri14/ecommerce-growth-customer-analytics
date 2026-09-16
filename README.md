# E-Commerce Growth & Customer Analytics

An end-to-end analytics project focused on understanding **sales performance, customer value, customer experience, product performance, and geographic patterns** in an e-commerce business.

The project combines data preparation, exploratory analysis, customer segmentation, business analysis, and an interactive Streamlit dashboard to turn transaction data into business-oriented insights.

> **Dataset:** Olist Brazilian E-Commerce Public Dataset  
> **Analysis period:** September 2016 – October 2018  
> **Core sales analysis period:** February 2017 – August 2018  
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
How are transaction value, order volume, and average order value changing over time?

### 2. Customer Experience
Is delivery performance associated with customer review scores?

### 3. Customer Value
Which customer segments are the most valuable, and which groups should be prioritized for retention or reactivation?

### 4. Product & Seller Performance
Which product categories and sellers contribute the most to transaction value and order volume?

### 5. Geographic Performance
Which customer states contribute the most to orders and transaction value?

---

# Dataset

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

# 1. Data Quality & Preparation

Before analysis, the datasets are audited for:

- Missing values
- Duplicate records
- Data types
- Order status
- Key relationships between tables

### Data quality findings

The main missing values were concentrated in:

| Dataset | Column | Missing |
|---|---|---:|
| Orders | `order_approved_at` | 160 |
| Orders | `order_delivered_carrier_date` | 1,783 |
| Orders | `order_delivered_customer_date` | 2,965 |
| Reviews | `review_comment_title` | 87,656 |
| Reviews | `review_comment_message` | 58,247 |
| Products | `product_category_name` | 610 |

The geolocation table contains **261,831 duplicate rows**, so it is treated carefully rather than being used blindly in joins.

Missing values are handled according to their business meaning rather than automatically removing or imputing them.

For example, delivery timestamps are not filled artificially because their absence can reflect orders that were not completed or had not reached the customer.

All order timestamp columns used in the analysis were converted to `datetime64[ns]`.

---

# 2. Sales Performance Analysis

Sales performance is analyzed using order and payment data.

### Main metrics

- Total transaction value
- Total orders
- Customer count
- Average order value
- Monthly transaction value
- Monthly orders
- Monthly AOV

Because the payment table can contain multiple records for the same order, payment values are first aggregated at the order level before being combined with order information.

For this project, `payment_value` is used as a **transaction value proxy**, not as accounting revenue.

## Core Sales Period

The dataset contains very small partial months at the beginning and end of the observation period.

For example:

- September 2016 contained only **4 orders**
- October 2018 contained only **4 orders**

Using these months for direct growth comparisons produced extreme percentages that were not useful from a business perspective.

Therefore, the core sales analysis focuses on months with at least **1,000 orders**:

**February 2017 – August 2018**

This gives **19 months** for the main sales comparison.

### Core period results

| Metric | Result |
|---|---:|
| Transaction value | **15.81M** |
| Orders | **98,292** |
| Average order value | **~161** |

### Top months by transaction value

| Month | Transaction Value | Orders | AOV |
|---|---:|---:|---:|
| **November 2017** | **1,194,882.80** | **7,544** | 158.39 |
| April 2018 | 1,160,785.48 | 6,939 | 167.28 |
| March 2018 | 1,159,652.12 | 7,211 | 160.82 |
| May 2018 | 1,153,982.15 | 6,873 | **167.90** |
| January 2018 | 1,115,004.18 | 7,269 | 153.39 |

### Highest AOV in the core period

April 2017 recorded the highest AOV:

**173.79**

This month had 2,404 orders and transaction value of 417,788.03.

The comparison shows that high transaction value and high AOV do not always occur in the same month. Both **order volume** and **value per order** should therefore be monitored.

---

# 3. Customer Experience Analysis

Customer experience is evaluated by combining delivery information with review scores.

### Metrics

- Delivery days
- Estimated delivery date
- Late delivery flag
- Average review score

Only orders with an actual customer delivery date are used for delivery-time analysis.

### Delivery results

The delivery analysis produced **96,359 orders** with both delivery information and a review score.

| Delivery Status | Average Review Score |
|---|---:|
| **On Time** | **4.29** |
| **Late** | **2.57** |

The difference is approximately **1.73 review points**.

This indicates a strong **association** between delivery performance and customer satisfaction in the dataset. The analysis does not claim that late delivery alone causes lower ratings.

### Business implication

Delivery reliability is an important operational area to monitor. Sellers or regions with repeated delivery delays can be investigated further as potential contributors to lower customer satisfaction.

---

# 4. RFM Customer Segmentation

RFM analysis is used to understand customer purchasing behavior.

### RFM Metrics

**Recency**  
How recently the customer made a purchase.

**Frequency**  
How many delivered orders the customer has made.

**Monetary**  
The total payment value associated with the customer's delivered orders.

The analysis uses `customer_unique_id` to identify customers across multiple orders.

### Customer base

The RFM dataset contains:

**93,357 unique customers**

The repeat-purchase check found:

- **2,801 customers** with more than one order
- Maximum observed orders for one customer: **15**
- Average frequency: **1.03 orders/customer**

This shows that most customers in the dataset made only one purchase, while a smaller group generated repeat transactions.

---

## Customer Segments

Customers are grouped into five business-oriented segments:

| Segment | Business Meaning |
|---|---|
| **Champions** | Repeat customers who are relatively recent and have high monetary value |
| **Loyal Customers** | Customers who have made multiple purchases |
| **At Risk** | Higher-value customers who have not purchased recently |
| **New / Potential** | Relatively recent customers who have not yet become repeat buyers |
| **Hibernating** | Customers with low recent activity and lower spending |

### Segment results

| Segment | Customers | Avg. Recency | Avg. Frequency | Avg. Monetary | Revenue Share |
|---|---:|---:|---:|---:|---:|
| **New / Potential** | **45,252** | 161.18 | 1.00 | 161.70 | **47.45%** |
| **At Risk** | **21,783** | 413.77 | 1.00 | 263.64 | **37.24%** |
| **Hibernating** | **23,521** | 414.15 | 1.00 | 63.68 | **9.71%** |
| **Loyal Customers** | **1,812** | 341.25 | 2.08 | 273.79 | **3.22%** |
| **Champions** | **989** | 137.90 | **2.18** | **372.35** | **2.39%** |

### Key customer findings

**New / Potential** is the largest segment with **45,252 customers**, contributing **47.45%** of customer revenue.

**At Risk** contains **21,783 customers** and contributes **37.24%** of customer revenue. Its average monetary value is relatively high at **263.64**, despite customers having a much higher average recency.

**Champions** is the smallest high-value segment, with **989 customers**, but has the highest average frequency (**2.18**) and average monetary value (**372.35**) among the five segments.

These results suggest three different retention priorities:

1. Convert **New / Potential** customers into repeat buyers.
2. Reactivate higher-value **At Risk** customers.
3. Retain **Champions** and **Loyal Customers**.

---

# 5. Product Performance

Product-level analysis combines order item and product information with category translation.

The analysis identifies:

- Orders by category
- Items sold
- Transaction value by category

### Top categories in the current analysis output

| Product Category | Transaction Value |
|---|---:|
| **bed_bath_table** | **1,712,553.67** |
| **health_beauty** | **1,657,373.12** |
| **computers_accessories** | **1,585,330.45** |
| **furniture_decor** | **1,430,176.39** |
| **watches_gifts** | **1,429,216.68** |

`bed_bath_table` leads the category analysis with the highest transaction value in the current analytical output.

> Note: category values follow the calculation defined in the notebook and should be interpreted as analytical transaction-value measures rather than accounting revenue.

---

# 6. Seller Performance

Seller performance is analyzed using order item data.

Metrics include:

- Orders
- Items sold
- Seller transaction value

Seller transaction value is based on the `price` recorded in `order_items` rather than total payment value, since customer payments can also include freight and other payment components.

The detailed seller-level results are available in:

`data/processed/seller_performance.csv`

---

# 7. Geographic Analysis

Customer location is used to understand regional performance.

Metrics include:

- Orders
- Customers
- Transaction value
- Revenue share

The detailed state-level results are available in:

`data/processed/geographic_performance.csv`

This analysis is designed to help identify regions with larger customer bases and stronger commercial contribution.

---

# Executive Insights

The analysis highlights several business signals.

### 01 — Repeat purchase is still limited

The RFM analysis contains **93,357 unique customers**, but only **2,801** made more than one delivered order.

This indicates that customer activity is heavily concentrated in first-time purchases.

### 02 — New / Potential customers represent a large opportunity

The segment contains **45,252 customers** and contributes **47.45%** of customer revenue.

The main opportunity is to increase the likelihood of a second purchase.

### 03 — At Risk customers carry meaningful historical value

The At Risk segment contributes **37.24%** of customer revenue and has an average monetary value of **263.64**.

This group is relevant for reactivation analysis because these customers have not purchased recently but previously generated relatively high transaction value.

### 04 — Delivery performance is associated with satisfaction

On-time orders have an average review score of **4.29**, compared with **2.57** for late orders.

This makes delivery reliability an important operational metric to monitor alongside customer satisfaction.

### 05 — Sales performance has multiple drivers

November 2017 generated the highest transaction value in the core sales period at **1.19M**, while April 2017 recorded the highest AOV at **173.79**.

This shows why both volume and order value should be monitored when evaluating sales performance.

---

# Business Recommendations

The findings support several possible business actions.

### 1. Increase Repeat Purchases

Develop post-purchase engagement for **New / Potential** customers to encourage a second transaction.

### 2. Reactivate High-Value Customers

Prioritize **At Risk** customers with relatively high historical monetary value for targeted reactivation campaigns.

### 3. Retain Repeat Customers

Maintain engagement with **Champions** and **Loyal Customers** through loyalty benefits, relevant offers, and personalized communication.

### 4. Improve Delivery Reliability

Monitor sellers and regions with higher delivery delays and investigate operational bottlenecks that may affect customer satisfaction.

### 5. Support Category Planning

Use category-level performance to support inventory planning, promotion decisions, and commercial prioritization.

---

# Interactive Dashboard

The project includes a Streamlit dashboard designed to provide a management-oriented view of the analysis.

### Dashboard Sections

**Executive Overview**
- Transaction value
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

The dashboard reads the processed analytical datasets generated from the main notebook.

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
- The sales growth analysis excludes very low-volume partial months from the core comparison.
- Product-category transaction values follow the calculation implemented in the notebook and should not be interpreted as accounting revenue.

The processed datasets used by the dashboard are generated from the main analysis notebook.
