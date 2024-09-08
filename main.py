import pandas as pd


def group_transactions_by_date(
    csv_file, date_column, amount_column, name_column, exclusion_list
):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Build the regex pattern to match any string in the exclusion_list
    regex_pattern = "|".join(exclusion_list)

    # Remove rows where the "Name" column contains any of the strings in the exclusion list
    df = df[~df[name_column].str.contains(regex_pattern, case=False, na=False)]

    # Convert the date column to a datetime type (optional but recommended)
    df[date_column] = pd.to_datetime(df[date_column])

    # Group by the date column and aggregate both sum and list of transaction names
    grouped_df = (
        df.groupby(date_column)
        .agg(
            total_amount=(amount_column, "sum"),
            transaction_names=(name_column, lambda x: ", ".join(map(str, x))),
        )
        .reset_index()
    )

    # Return the grouped DataFrame with total amount and transaction list
    return grouped_df


# Example usage
csv_file = "statement.csv"

# List of strings to exclude from the "Name" column
exclusion_list = [
    "PENNYMAC",
    "WITHDRAWAL ATT",
    "SERVICE FINANCE",
    "MINT MOBILE",
    "AMERENMO",
    "STATE FARM",
    "ELECTRONIC WITHDRAWAL Spire",
    "OPENAI",
    '365 RETAIL'
]

grouped_transactions = group_transactions_by_date(
    csv_file, "Date", "Amount", "Name", exclusion_list
)

# Print the grouped transactions (without the excluded names)
print(grouped_transactions)

# Save the output to a new CSV file
output_csv_file = "grouped_transactions.csv"
grouped_transactions.to_csv(output_csv_file, index=False)

# Print confirmation message
print(f"Grouped transactions have been written to {output_csv_file}")
