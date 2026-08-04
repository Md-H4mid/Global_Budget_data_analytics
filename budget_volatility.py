from sqlalchemy import create_engine
import pandas as pd

def analyze_budget_volatility(country_name):
    engine = create_engine("mysql+pymysql://root:H4MID@127.0.0.1:3306/global_budget_db")

    # extract historical spending sequence
    query = """
        SELECT b.year, b.total_budget_billions_usd AS total_budget_billion_usd
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s
        ORDER BY b.year ASC;
    """
    df = pd.read_sql_query(query, engine, params=(country_name,))

    if df.empty:
        print(f'No budget data found for {country_name}')
        return df

    # calculate a 10-year rolling mean and standard deviation using Pandas
    df['rolling_mean'] = df['total_budget_billion_usd'].rolling(window=10).mean()
    df['rolling_std'] = df['total_budget_billion_usd'].rolling(window=10).std()

    # calculate volatility index (coefficient of variation)
    df['volatility_index'] = (df['rolling_std'] / df['rolling_mean']) * 100
    print(f"\n---📈 Era Volatility index for {country_name} (sample)---")
    print(df.dropna().head(10))
    return df

if __name__ == "__main__":
    analyze_budget_volatility("USA")  # or your country
    
