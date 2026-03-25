# 🏦 DADV MINI PROJECT  
### Banking Transaction Analytics Dashboard

An interactive data visualization dashboard built using **Python, Dash, and Plotly** to analyze banking transactions and uncover insights from financial data.

---

## 📊 Project Overview

This project focuses on **Exploratory Data Analysis (EDA)** and **interactive visualization** of banking transactions. The dashboard allows users to:

- Analyze transaction trends over time  
- Compare credit vs debit behavior  
- Understand spending patterns  
- Explore financial distributions visually  

---

## 📁 Dataset

The dataset used is:  
`bank_transactions.csv`

### 🔹 Features

- `Customer_ID` – Unique identifier  
- `Gender` – Male / Female  
- `Age` – Customer age  
- `Occupation` – Profession  
- `Transaction_Type` – Deposit / Withdrawal / Transfer  
- `Amount` – Transaction value  
- `Date` – Timestamp of transaction  

---

## ⚙️ Tech Stack

- **Python**
- **Pandas** – Data processing  
- **Dash** – Web framework  
- **Plotly** – Interactive visualizations  

---

## 🚀 Features of Dashboard

### 📌 KPI Cards
- Total Amount  
- Total Credit  
- Total Debit  
- Net Balance  

### 📈 Visualizations
- Donut Chart → Credit vs Debit distribution  
- Line Chart → Monthly transaction trends  
- Box Plot → Transaction distribution  
- Heatmap → Transaction intensity  

### 🎛️ Filters
- Year-wise filtering  
- Dynamic chart selection  

---

## 🧠 Data Processing Steps

- Removed missing values  
- Converted `Date` to datetime format  
- Extracted:
  - Year  
  - Month  
  - Month number (for proper sorting)  

---
