from tabulate import tabulate

class ViewerDataAnalyzer:

    @staticmethod
    def calculate_reading_times(df):
       
        df = df[df['event_type'] == 'pagereadtime']
        read_time_per_user = df.groupby('visitor_uuid')['event_readtime'].sum()
        top_readers = read_time_per_user.sort_values(ascending=False).head(10)
        return top_readers
    
    def print_top_readers(top_readers):
        if top_readers is not None and not top_readers.empty:
            print("\nTop 10 Readers (UUID and Total Read Time in Milliseconds):\n")

            # Convert the Series to a DataFrame for pretty printing as a table
            top_readers_df = top_readers.reset_index()
            top_readers_df.columns = ['Visitor UUID', 'Total Read Time (Milliseconds)']

            # Use the tabulate library to print the DataFrame with grid lines
            print(tabulate(top_readers_df, headers='keys', tablefmt='grid', showindex=False))
        else:
            print("No top readers found.")
