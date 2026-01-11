"""
Sales Data Generator
Generate realistic sample sales data for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_TRANSACTIONS = 10000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Product catalog
PRODUCTS = {
    'Electronics': [
        ('iPhone 15', 999, 1199),
        ('MacBook Pro', 1999, 2499),
        ('AirPods Pro', 199, 249),
        ('iPad Air', 599, 799),
        ('Apple Watch', 399, 499),
    ],
    'Clothing': [
        ('T-Shirt', 25, 45),
        ('Jeans', 50, 89),
        ('Sneakers', 80, 150),
        ('Jacket', 100, 200),
        ('Dress', 60, 120),
    ],
    'Home & Garden': [
        ('Coffee Maker', 50, 120),
        ('Vacuum Cleaner', 150, 300),
        ('Air Purifier', 100, 250),
        ('Blender', 40, 80),
        ('Lamp', 30, 70),
    ],
    'Books': [
        ('Fiction Novel', 12, 25),
        ('Tech Book', 35, 60),
        ('Cookbook', 20, 40),
        ('Self-Help', 15, 30),
        ('Children Book', 10, 20),
    ],
    'Sports': [
        ('Yoga Mat', 25, 50),
        ('Dumbbell Set', 50, 120),
        ('Running Shoes', 80, 150),
        ('Bicycle', 300, 800),
        ('Tennis Racket', 60, 150),
    ],
}

# Regions with weights (some regions sell more)
REGIONS = {
    'North': 0.25,
    'South': 0.30,
    'East': 0.20,
    'West': 0.25,
}

# Customer segments
CUSTOMER_TYPES = ['New', 'Returning', 'VIP']

# Payment methods
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'PayPal', 'Cash', 'Bank Transfer']


def generate_date():
    """Generate random date with seasonal patterns"""
    days_range = (END_DATE - START_DATE).days
    random_days = random.randint(0, days_range)
    date = START_DATE + timedelta(days=random_days)
    
    # Add seasonal weight (more sales in Q4)
    month = date.month
    if month in [11, 12]:  # Holiday season
        if random.random() > 0.3:  # 70% chance to keep Q4 dates
            return date
        else:
            return generate_date()
    return date


def generate_transaction():
    """Generate a single transaction"""
    # Select category and product
    category = random.choice(list(PRODUCTS.keys()))
    product_name, min_price, max_price = random.choice(PRODUCTS[category])
    
    # Price with some variation
    unit_price = round(random.uniform(min_price, max_price), 2)
    
    # Quantity (most orders are 1-3 items)
    quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
    
    # Calculate total
    total_amount = round(unit_price * quantity, 2)
    
    # Apply discount (20% of orders get discount)
    discount_pct = 0
    if random.random() < 0.2:
        discount_pct = random.choice([5, 10, 15, 20, 25])
    
    discount_amount = round(total_amount * discount_pct / 100, 2)
    final_amount = round(total_amount - discount_amount, 2)
    
    # Region selection (weighted)
    region = np.random.choice(
        list(REGIONS.keys()),
        p=list(REGIONS.values())
    )
    
    # Customer and payment info
    customer_type = np.random.choice(CUSTOMER_TYPES, p=[0.3, 0.5, 0.2])
    payment_method = random.choice(PAYMENT_METHODS)
    
    # Generate date
    transaction_date = generate_date()
    
    return {
        'transaction_id': None,  # Will be set later
        'date': transaction_date.strftime('%Y-%m-%d'),
        'year': transaction_date.year,
        'month': transaction_date.month,
        'day': transaction_date.day,
        'day_of_week': transaction_date.strftime('%A'),
        'category': category,
        'product_name': product_name,
        'unit_price': unit_price,
        'quantity': quantity,
        'total_amount': total_amount,
        'discount_percent': discount_pct,
        'discount_amount': discount_amount,
        'final_amount': final_amount,
        'region': region,
        'customer_type': customer_type,
        'payment_method': payment_method,
    }


def main():
    """Generate and save sales data"""
    print("🛒 Generating Sales Data...")
    
    # Generate transactions
    transactions = []
    for i in range(NUM_TRANSACTIONS):
        transaction = generate_transaction()
        transaction['transaction_id'] = f'TXN{str(i+1).zfill(6)}'
        transactions.append(transaction)
    
    # Create DataFrame
    df = pd.DataFrame(transactions)
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    # Save to CSV
    output_path = '/Users/tominhhaxinhdep/Downloads/DA_Project/sales_dashboard/data/sales_data.csv'
    df.to_csv(output_path, index=False)
    
    # Print summary
    print(f"✅ Generated {len(df)} transactions")
    print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"💰 Total revenue: ${df['final_amount'].sum():,.2f}")
    print(f"📁 Saved to: {output_path}")
    
    # Preview
    print("\n📊 Sample Data:")
    print(df.head(10).to_string())
    
    print("\n📈 Summary by Category:")
    summary = df.groupby('category').agg({
        'transaction_id': 'count',
        'final_amount': 'sum'
    }).rename(columns={'transaction_id': 'transactions', 'final_amount': 'revenue'})
    summary['revenue'] = summary['revenue'].apply(lambda x: f"${x:,.2f}")
    print(summary.to_string())


if __name__ == '__main__':
    main()
