import pandas as pd
import numpy as np
import os

def clean_and_prepare_data(input_path, excel_output_path, csv_output_path):
    print("=" * 60)
    print("STARTING DATA CLEANING & PREPARATION PIPELINE")
    print("=" * 60)
    
    # 1. Load Raw Dataset
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
        
    df = pd.read_excel(input_path)
    initial_rows, initial_cols = df.shape
    print(f"Loaded raw dataset: {initial_rows} rows, {initial_cols} columns.")
    
    # 2. Audit Missing Values Before Cleaning
    print("\n--- Step 1: Missing Value Audit & Handling ---")
    missing_before = df.isnull().sum()
    print("Missing values before cleaning:")
    print(missing_before[missing_before > 0] if missing_before.sum() > 0 else "No missing values!")
    
    # Fill missing CouponCode with 'NO_COUPON'
    df['CouponCode'] = df['CouponCode'].fillna('NO_COUPON')
    
    missing_after = df.isnull().sum().sum()
    print(f"Missing values after handling: {missing_after} nulls.")
    
    # 3. Duplicate Handling & Verification
    print("\n--- Step 2: Duplicate Audit & Removal ---")
    exact_dups = df.duplicated().sum()
    orderid_dups = df.duplicated(subset=['OrderID']).sum()
    print(f"Exact duplicate rows found: {exact_dups}")
    print(f"Duplicate OrderIDs found: {orderid_dups}")
    
    if exact_dups > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Removed {exact_dups} duplicate rows.")
    else:
        print("No duplicate rows to remove.")
        
    # 4. Text & String Standardization
    print("\n--- Step 3: Text & String Formatting ---")
    text_columns = ['OrderID', 'CustomerID', 'Product', 'ShippingAddress', 
                    'PaymentMethod', 'OrderStatus', 'TrackingNumber', 
                    'CouponCode', 'ReferralSource']
    
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    print(f"Standardized {len(text_columns)} text columns (whitespace stripped).")

    # 5. Date Formatting & Temporal Decomposition
    print("\n--- Step 4: Date Formatting & Temporal Feature Engineering ---")
    df['Date'] = pd.to_datetime(df['Date'])
    df['FormattedDate'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['OrderYear'] = df['Date'].dt.year
    df['OrderMonth'] = df['Date'].dt.month
    df['OrderMonthName'] = df['Date'].dt.strftime('%B')
    df['OrderDay'] = df['Date'].dt.day
    df['DayOfWeek'] = df['Date'].dt.strftime('%A')
    df['IsWeekend'] = df['Date'].dt.dayofweek.isin([5, 6]).astype(int)
    print("Added temporal columns: FormattedDate, OrderYear, OrderMonth, OrderMonthName, OrderDay, DayOfWeek, IsWeekend.")

    # 6. Numeric & Financial Formatting + Business Calculation
    print("\n--- Step 5: Financial Formatting & Discount Feature Engineering ---")
    df['Quantity'] = df['Quantity'].astype(int)
    df['ItemsInCart'] = df['ItemsInCart'].astype(int)
    df['UnitPrice'] = df['UnitPrice'].round(2)
    df['GrossAmount'] = (df['Quantity'] * df['UnitPrice']).round(2)
    
    # Calculate discount percentages based on CouponCode
    coupon_discount_map = {
        'SAVE10': 0.10,
        'WINTER15': 0.15,
        'FREESHIP': 0.00,
        'NO_COUPON': 0.00
    }
    df['DiscountPercent'] = df['CouponCode'].map(coupon_discount_map).fillna(0.0)
    df['DiscountAmount'] = (df['GrossAmount'] * df['DiscountPercent']).round(2)
    df['NetAmount'] = (df['GrossAmount'] - df['DiscountAmount']).round(2)
    df['TotalPrice'] = df['GrossAmount'] # Ensure TotalPrice matches Gross Amount
    
    print("Calculated financial fields: GrossAmount, DiscountPercent, DiscountAmount, NetAmount.")

    # 7. Quality Assurance Assertions
    print("\n--- Step 6: Quality Assurance Verification ---")
    assert df.isnull().sum().sum() == 0, "Error: Null values detected after cleaning!"
    assert len(df) == initial_rows, f"Error: Row count changed from {initial_rows} to {len(df)}"
    assert (df['Quantity'] > 0).all(), "Error: Negative or zero quantities detected!"
    assert (df['UnitPrice'] > 0).all(), "Error: Negative or zero prices detected!"
    print("[OK] ALL QUALITY ASSERTIONS PASSED SUCCESSFULLY!")

    # 8. Reorder Columns for Optimal Readability
    ordered_cols = [
        'OrderID', 'FormattedDate', 'CustomerID', 'Product', 'Quantity', 
        'UnitPrice', 'GrossAmount', 'CouponCode', 'DiscountPercent', 
        'DiscountAmount', 'NetAmount', 'TotalPrice', 'ShippingAddress', 
        'PaymentMethod', 'OrderStatus', 'TrackingNumber', 'ItemsInCart', 
        'ReferralSource', 'OrderYear', 'OrderMonth', 'OrderMonthName', 
        'OrderDay', 'DayOfWeek', 'IsWeekend'
    ]
    df_cleaned = df[ordered_cols].copy()
    df_cleaned.rename(columns={'FormattedDate': 'Date'}, inplace=True)

    # 9. Export Production Datasets
    print("\n--- Step 7: Exporting Cleaned Datasets ---")
    df_cleaned.to_excel(excel_output_path, index=False)
    df_cleaned.to_csv(csv_output_path, index=False)
    
    print(f"[OK] Saved cleaned Excel dataset to: {excel_output_path}")
    print(f"[OK] Saved cleaned CSV dataset to: {csv_output_path}")
    
    print("\n" + "=" * 60)
    print("DATA CLEANING & PREPARATION COMPLETE!")
    print("=" * 60)
    return df_cleaned

if __name__ == "__main__":
    raw_file = "Dataset for Data Analytics.xlsx"
    excel_out = "Cleaned_Dataset_for_Data_Analytics.xlsx"
    csv_out = "Cleaned_Dataset_for_Data_Analytics.csv"
    clean_and_prepare_data(raw_file, excel_out, csv_out)
