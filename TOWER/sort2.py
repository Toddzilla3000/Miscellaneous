import pandas as pd

# Function to process the CSV data
def process_sales_data(input_csv):
    # Step 1: Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)
    
    # Step 2: Ensure correct data types (e.g., COST should be numeric)
    df['COST'] = pd.to_numeric(df['COST'], errors='coerce')
    
    # Step 3: Group the data by DIVISION, MONTH, and TEAM, then sum COST for each group
    grouped_data = df.groupby(['DIVISION', 'MONTH', 'TEAM']).agg({'COST': 'sum'}).reset_index()
    
    # Step 4: Create a list to hold DataFrames for each division
    all_data = []
    
    # Step 5: Process each division and store the results
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
        
	# Add a row for the sum across all teams
        total_row = pivot_data.sum(axis=0)
        total_row['TOTAL'] = total_row.sum()  # Sum of all teams' totals
        total_row.name = 'Total'  # Name the row as 'Total'
        
        # Append the total row to the data
        # pivot_data = pivot_data.append(total_row)
  
        # Concatenate the total row with the pivot data
        pivot_data = pd.concat([pivot_data, total_row.to_frame().T])  # to_frame().T converts Series to DataFrame
  
        # Add a column indicating the division for each row
        pivot_data['DIVISION'] = division
        
        # Append the pivoted data for the division to the list
        all_data.append(pivot_data)
        
        # Optionally save the division's file
        output_filename = f"{division}_team_monthly_totals.csv"
        pivot_data.to_csv(output_filename)
        print(f"File saved: {output_filename}")
    
    # Step 6: Concatenate all division DataFrames into one
    final_data = pd.concat(all_data)
    
    # Step 7: Save the final concatenated data to a single CSV file
    final_data.to_csv('all_divisions_team_monthly_totals.csv', index=True)
    print("Final concatenated file saved: all_divisions_team_monthly_totals.csv")

# Main function to run the program
if __name__ == "__main__":
    # Specify the input CSV file
    input_csv = 'FAKEDATA.csv'  # Replace with the path to your CSV file
    
    # Process the data
    process_sales_data(input_csv)

