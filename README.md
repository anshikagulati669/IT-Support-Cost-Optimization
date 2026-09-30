# IT Support Cost Optimization Using Data Analysis

## 📌 Project Overview

This project analyzes customer IT support ticket data to understand support workload, unresolved tickets, customer satisfaction, ticket priorities, and support channels.

The main goal is to identify patterns in support operations and provide data-driven insights that can help organizations improve support efficiency and reduce unresolved workload.

An interactive dashboard has also been developed using **Streamlit** to explore the support data.

---

## 🎯 Objectives

- Analyze customer support ticket data
- Identify the most common types of support tickets
- Analyze ticket status and unresolved workload
- Understand ticket priority distribution
- Compare customer satisfaction across ticket types
- Analyze different support channels
- Identify ticket types with higher unresolved workload
- Build an interactive data analysis dashboard
- Provide business insights for improving support operations

---

## 📊 Dataset

The dataset contains customer support ticket information.

### Important Columns

| Column | Description |
|---|---|
| Ticket ID | Unique ticket identifier |
| Customer Age | Age of the customer |
| Customer Gender | Gender of the customer |
| Product Purchased | Product associated with the ticket |
| Date of Purchase | Date when the product was purchased |
| Ticket Type | Type of support request |
| Ticket Status | Current status of the ticket |
| Resolution | Resolution provided for the ticket |
| Ticket Priority | Priority level of the ticket |
| Ticket Channel | Channel used by the customer |
| First Response Time | First response timestamp |
| Time to Resolution | Resolution timestamp |
| Customer Satisfaction Rating | Customer satisfaction score |

---

## 🔍 Data Analysis Performed

The project performs the following analysis:

### 1. Missing Value Analysis
Identifies missing values in important columns and understands their relationship with ticket status.

### 2. Duplicate Analysis
Checks the dataset for duplicate records.

### 3. Ticket Status Analysis
Analyzes:

- Closed tickets
- Open tickets
- Pending tickets
- Unresolved tickets

### 4. Ticket Type Analysis
Analyzes different support request types such as:

- Refund request
- Technical issue
- Cancellation request
- Product inquiry
- Billing inquiry

### 5. Priority Analysis
Analyzes:

- Critical
- High
- Medium
- Low

### 6. Customer Satisfaction Analysis
Compares average customer satisfaction across:

- Ticket types
- Ticket priorities

### 7. Support Channel Analysis
Analyzes tickets received through:

- Email
- Phone
- Chat
- Social media

### 8. Ticket Type vs Status
Compares ticket types with their current status to identify workload patterns.

### 9. Priority vs Status
Analyzes whether high-priority tickets are being resolved or remain unresolved.

---

## 📈 Key Insights

Some important findings from the analysis include:

- The dataset contains **8,469 support tickets**.
- Around **67.3% of tickets are unresolved**, meaning they are either Open or Pending.
- Refund requests and technical issues are among the major support categories.
- Customer satisfaction varies across different ticket types and priorities.
- Different support channels have different ticket volumes.
- Medium and Low priority tickets contribute significantly to the unresolved workload.

These insights can help organizations identify areas where support resources and processes may need improvement.

---

## 📊 Visualizations

The project generates visualizations for:

- Tickets by Ticket Type
- Tickets by Priority
- Ticket Status Distribution
- Customer Satisfaction by Ticket Type
- Tickets by Support Channel
- Unresolved Tickets by Ticket Type

---

## 🖥️ Streamlit Dashboard

An interactive dashboard was created using **Streamlit**.

The dashboard provides:

- KPI cards
- Ticket type filters
- Ticket status filters
- Priority filters
- Channel filters
- Customer gender filters
- Interactive charts
- Business insights
- Filtered data preview

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter Notebook

---

## 📁 Project Structure

```text
IT-Support-Cost-Optimization/
│
├── data/
│   └── cleaned_customer_support_tickets.csv
│
├── output/
│   ├── tickets_by_type.png
│   ├── tickets_by_priority.png
│   ├── satisfaction_by_ticket_type.png
│   ├── ticket_status.png
│   ├── tickets_by_channel.png
│   └── unresolved_tickets_by_type.png
│
├── main.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
