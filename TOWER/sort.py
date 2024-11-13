import pandas as pd

# Function to process the CSV data
def process_sales_data(input_csv):
    # Step 1: Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)
    
    # Step 2: Ensure correct data types (e.g., COST should be numeric)
    df['COST'] = pd.to_numeric(df['COST'], errors='coerce')
    
    # Step 3: Group the data by DIVISION, MONTH, and TEAM, then sum COST for each group
    grouped_data = df.groupby(['DIVISION', 'MONTH', 'TEAM']).agg({'COST': 'sum'}).reset_index()
    
    # Step 4: Create a CSV file for each DIVISION
    divisions = grouped_data['DIVISION'].unique()
    
    for division in divisions:
        # Filter data for the current division
        division_data = grouped_data[grouped_data['DIVISION'] == division]
        
        # Pivot the data to get a TEAM x MONTH table, with COST values
        pivot_data = division_data.pivot_table(index=['TEAM'], columns=['MONTH'], values='COST', aggfunc='sum', fill_value=0)
        
        # Add a column for the total COST across all months for each team
        pivot_data['TOTAL'] = pivot_data.sum(axis=1)
        
	# Sort the rows by the 'TOTAL' column in descending order
        pivot_data = pivot_data.sort_values(by='TOTAL', ascending=False)

        # Save the data to a CSV file
        output_filename = f"{division}_team_monthly_totals.csv"
        pivot_data.to_csv(output_filename)
        print(f"File saved: {output_filename}")

# Main function to run the program
if __name__ == "__main__":
    # Specify the input CSV file
    input_csv = 'FAKEDATA.csv'  # Replace with the path to your CSV file
    
    # Process the data
    process_sales_data(input_csv)

