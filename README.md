# 🧹 Project 1: Data Cleaning & Preparation

![Data Quality](https://img.shields.io/badge/Data_Quality-100%25-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Library-Pandas-orange)
![License](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
This repository contains the complete **Data Cleaning & Preparation Pipeline** for **Project 1** of the Decode Labs Internship. The objective of this project is to sanitize, prepare, and enrich a raw e-commerce sales dataset (`Dataset for Data Analytics.xlsx`), ensuring data integrity, fixing missing values, removing potential duplicates, standardizing data types, and engineering features for downstream analytics.

---

## 🎯 Key Objectives & Requirements
- **Missing Value Handling**: Identify null/missing values across all columns and apply business-appropriate imputation.
- **Duplicate Removal**: Audit exact row duplicates and unique identifier (`OrderID`, `TrackingNumber`) overlaps.
- **Format Correction**: Standardize date formats (`YYYY-MM-DD`), round currency values to 2 decimal places, and strip whitespace from text fields.
- **Data Preparation & Feature Engineering**: Create derived financial and temporal features (`GrossAmount`, `DiscountAmount`, `NetAmount`, `OrderYear`, `OrderMonth`, `DayOfWeek`, `IsWeekend`).

---

## 📊 Dataset Summary

| Metric | Raw Dataset | Cleaned Dataset |
| :--- | :---: | :---: |
| **Total Rows** | 1,200 | 1,200 |
| **Total Columns** | 14 | 24 |
| **Missing Values** | 309 (`CouponCode`) | **0** |
| **Duplicate Rows** | 0 | **0** |
| **Data Quality Score** | ~74% | **100%** |

---

## 🛠️ Data Sanitation & Cleaning Steps Taken

### 1. Missing Value Imputation
- **Audit**: Identified 309 missing values (~25.75%) in `CouponCode`.
- **Action**: Imputed missing `CouponCode` entries with `'NO_COUPON'` to preserve order completeness while explicitly marking transactions without promotional discounts.

### 2. Duplicate Audit
- **Audit**: Checked exact row duplicates and primary key collisions on `OrderID` and `TrackingNumber`.
- **Result**: Verified 0 duplicate records. All 1,200 rows are unique.

### 3. Text & Numeric Standardization
- **Text Trimming**: Stripped leading/trailing whitespaces across string columns (`Product`, `ShippingAddress`, `PaymentMethod`, `OrderStatus`, etc.).
- **Date Formatting**: Converted raw datetime strings into ISO standard `YYYY-MM-DD` format.
- **Financial Precision**: Rounded `UnitPrice`, `GrossAmount`, `DiscountAmount`, `NetAmount`, and `TotalPrice` to 2 decimal places.

### 4. Feature Engineering
Derived **10 new analytical feature columns** to prepare the dataset for data analytics and visualization:
- `GrossAmount`: `Quantity * UnitPrice`
- `DiscountPercent`: Discount mapping (`SAVE10`: 10%, `WINTER15`: 15%, `FREESHIP`: 0%, `NO_COUPON`: 0%)
- `DiscountAmount`: `GrossAmount * DiscountPercent`
- `NetAmount`: `GrossAmount - DiscountAmount`
- `OrderYear`: Calendar year of order
- `OrderMonth`: Month number (1–12)
- `OrderMonthName`: Month name (e.g., `January`)
- `OrderDay`: Day of month
- `DayOfWeek`: Day name (e.g., `Monday`)
- `IsWeekend`: Binary indicator (`1` for Saturday/Sunday, `0` otherwise)

---

## 📁 Repository Structure

```
├── Dataset for Data Analytics.xlsx          # Raw input dataset
├── Cleaned_Dataset_for_Data_Analytics.xlsx    # Production cleaned Excel file
├── Cleaned_Dataset_for_Data_Analytics.csv     # Production cleaned CSV file
├── clean_data.py                            # Automated Python data cleaning script
├── README.md                                # Project documentation
└── .gitignore                               # Git ignore configuration
```

---

## 🚀 How to Run the Pipeline

### Prerequisites
Ensure Python 3.8+ is installed along with the required libraries:
```bash
pip install pandas openpyxl
```

### Execution
Run the automated cleaning pipeline script:
```bash
python clean_data.py
```

### Output
The script will perform all sanitation checks, apply feature engineering, run quality assertions, and output two cleaned production files:
- `Cleaned_Dataset_for_Data_Analytics.xlsx`
- `Cleaned_Dataset_for_Data_Analytics.csv`

---

## 📋 Cleaned Dataset Schema (24 Columns)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `OrderID` | `String` | Unique Order Identifier |
| `Date` | `Date (YYYY-MM-DD)` | Date of order placement |
| `CustomerID` | `String` | Unique Customer Identifier |
| `Product` | `String` | Purchased product name |
| `Quantity` | `Integer` | Units ordered |
| `UnitPrice` | `Float` | Unit price in USD ($) |
| `GrossAmount` | `Float` | `Quantity * UnitPrice` |
| `CouponCode` | `String` | Applied promo code (`SAVE10`, `WINTER15`, `FREESHIP`, `NO_COUPON`) |
| `DiscountPercent` | `Float` | Discount rate applied (0.00 - 0.15) |
| `DiscountAmount` | `Float` | Dollar value of discount |
| `NetAmount` | `Float` | Final order revenue after discount |
| `TotalPrice` | `Float` | Gross transaction total |
| `ShippingAddress` | `String` | Customer delivery address |
| `PaymentMethod` | `String` | Payment method (`Credit Card`, `Debit Card`, `Cash`, `Online`, `Gift Card`) |
| `OrderStatus` | `String` | Order state (`Delivered`, `Shipped`, `Pending`, `Returned`, `Cancelled`) |
| `TrackingNumber` | `String` | Shipment tracking code |
| `ItemsInCart` | `Integer` | Total items in cart at checkout |
| `ReferralSource` | `String` | Traffic channel (`Instagram`, `Facebook`, `Email`, `Google`, `Referral`) |
| `OrderYear` | `Integer` | Year of transaction |
| `OrderMonth` | `Integer` | Month of transaction (1-12) |
| `OrderMonthName` | `String` | Month name |
| `OrderDay` | `Integer` | Day of month |
| `DayOfWeek` | `String` | Day of week |
| `IsWeekend` | `Integer` | 1 if Weekend, 0 if Weekday |

---

## ⚙️ Verification & Data Quality Assurance

The pipeline enforces strict assertions upon execution:
- ✅ Zero remaining missing/null values across all columns.
- ✅ Row count preservation (exactly 1,200 rows).
- ✅ Non-negative numeric bounds verification (`Quantity > 0`, `UnitPrice > 0`).

---

## 🤝 Author & Acknowledgments
- **Project**: Decode Labs Internship — Task 1: Data Cleaning & Preparation
