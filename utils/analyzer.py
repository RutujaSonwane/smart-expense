import pandas as pd

def analyze_expenses(file_path):
    df = pd.read_csv(file_path)
    result = {}

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    if 'date' not in df.columns or 'amount' not in df.columns:
        result['error'] = "CSV must contain 'Date' and 'Amount' columns."
        return result

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date', 'amount'], inplace=True)

    result['total_spent'] = round(df['amount'].sum(), 2)
    result['avg_spent'] = round(df['amount'].mean(), 2)

    monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
    monthly['date'] = monthly['date'].astype(str)
    result['monthly_spend'] = monthly.to_dict(orient='records')

    if 'category' in df.columns:
        result['category_spend'] = df.groupby('category')['amount'].sum().reset_index().to_dict(orient='records')

    return result