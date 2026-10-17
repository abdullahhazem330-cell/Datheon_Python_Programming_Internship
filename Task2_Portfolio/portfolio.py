import csv
import os


def load_stock_prices(filename="constituents.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    stock_prices = {}

    if not os.path.exists(file_path):
        print(f"[!] Warning: '{filename}' not found at {file_path}.")
        return stock_prices

    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row.get("Symbol") or row.get("symbol") or row.get("ticker") or row.get("Ticker")
            if symbol:
                symbol_clean = symbol.strip().upper()
                # If price is provided in dataset, parse it; otherwise set dummy default market price
                price_str = row.get("Price") or row.get("price") or row.get("current_price") or "100.0"
                try:
                    stock_prices[symbol_clean] = float(price_str)
                except ValueError:
                    stock_prices[symbol_clean] = 100.0

    return stock_prices


def calculate_portfolio(portfolio_items, stock_prices):
    summary = []
    total_invested = 0.0
    total_market_value = 0.0

    for item in portfolio_items:
        ticker = item["ticker"]
        shares = item["shares"]
        buy_price = item["buy_price"]

        invested = shares * buy_price
        current_price = stock_prices.get(ticker, buy_price)
        market_value = shares * current_price
        gain_loss = market_value - invested
        gain_loss_pct = (gain_loss / invested * 100) if invested > 0 else 0.0

        total_invested += invested
        total_market_value += market_value

        summary.append({
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested": invested,
            "market_value": market_value,
            "gain_loss": gain_loss,
            "gain_loss_pct": gain_loss_pct
        })

    total_gain_loss = total_market_value - total_invested
    total_gain_loss_pct = (total_gain_loss / total_invested * 100) if total_invested > 0 else 0.0

    return summary, total_invested, total_market_value, total_gain_loss, total_gain_loss_pct


def save_summary_to_csv(summary, filename="portfolio_summary.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    fieldnames = [
        "Ticker", "Shares", "Buy Price ($)", "Current Price ($)",
        "Invested ($)", "Market Value ($)", "Gain/Loss ($)", "Gain/Loss (%)"
    ]

    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for item in summary:
            writer.writerow([
                item["ticker"],
                item["shares"],
                f"{item['buy_price']:.2f}",
                f"{item['current_price']:.2f}",
                f"{item['invested']:.2f}",
                f"{item['market_value']:.2f}",
                f"{item['gain_loss']:.2f}",
                f"{item['gain_loss_pct']:.2f}%"
            ])

    print(f"\n[✓] Portfolio summary successfully saved to '{file_path}'.")


def main():
    stock_prices = load_stock_prices("constituents.csv")

    print("=" * 65)
    print("📊 Stock Portfolio Performance Tracker")
    print("=" * 65)

    portfolio_items = []

    while True:
        ticker = input("\nEnter Stock Ticker (or type 'done' to calculate): ").strip().upper()
        if ticker in ["DONE", "EXIT", "QUIT"]:
            break

        if not ticker:
            continue

        try:
            shares = float(input(f"Enter number of shares for {ticker}: "))
            buy_price = float(input(f"Enter buy price per share for {ticker} ($): "))
            if shares <= 0 or buy_price <= 0:
                print("[!] Shares and buy price must be positive numbers.")
                continue
        except ValueError:
            print("[!] Invalid numeric input. Please enter valid numbers.")
            continue

        portfolio_items.append({
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price
        })

    if not portfolio_items:
        print("\nNo portfolio items entered. Exiting.")
        return

    summary, total_invested, total_market_value, total_gain_loss, total_gain_loss_pct = calculate_portfolio(
        portfolio_items, stock_prices
    )

    print("\n" + "=" * 80)
    print(
        f"{'Ticker':<10} {'Shares':<10} {'Buy Price':<12} {'Current':<12} {'Invested':<12} {'Market Val':<12} {'Gain/Loss':<10}")
    print("=" * 80)

    for row in summary:
        print(
            f"{row['ticker']:<10} {row['shares']:<10.2f} ${row['buy_price']:<11.2f} ${row['current_price']:<11.2f} ${row['invested']:<11.2f} ${row['market_value']:<11.2f} {row['gain_loss_pct']:+.2f}%")

    print("=" * 80)
    print(f"Total Invested Capital : ${total_invested:.2f}")
    print(f"Total Portfolio Value  : ${total_market_value:.2f}")
    print(f"Overall Gain / Loss    : ${total_gain_loss:+.2f} ({total_gain_loss_pct:+.2f}%)")
    print("=" * 80)

    save_summary_to_csv(summary)


if __name__ == "__main__":
    main()