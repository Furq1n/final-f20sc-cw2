import plotly.express as px
import plotly.io as pio
import pycountry_convert as pc

class GeoDataAnalyzer:

    # Convert country code to continent name
    def country_to_continent(country_code):

        try:

            continent_code = pc.country_alpha2_to_continent_code(country_code)
            return pc.convert_continent_code_to_continent_name(continent_code)
        
        except KeyError:
            return "Unknown"

    @staticmethod
    def get_country_counts(df):

        return df['visitor_country'].value_counts()
    
    @staticmethod
    def get_continent_counts(df):

        return df['visitor_country'].apply(GeoDataAnalyzer.country_to_continent).value_counts()
    
    @staticmethod
    def create_analysis_by_country(country_counts):

        # Create the bar chart
        fig = px.bar(country_counts, 
                     x=country_counts.index, 
                     y=country_counts.values, 
                     title='Views by Country',
                     labels={'x': 'Country', 'y': 'Number of Views'})

        # Customize the layout
        fig.update_layout(
            title={'text': 'Views by Country', 'x': 0.5, 'xanchor': 'center'},
            xaxis_title='Country',
            yaxis_title='Number of Views',
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            font=dict(family='Arial, sans-serif', size=12, color='black'),
            xaxis=dict(showgrid=False),  # Hide the x-axis gridlines
            yaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Light grey y-axis gridlines
        )

        # Customize the bar colors
        fig.update_traces(marker_color='rgb(67, 162, 202)', marker_line_color='rgb(27,120,55)',
                        marker_line_width=1.5, opacity=0.8)

        # Add hover template for more information on hover
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Views: %{y}")

        return fig
    
    @staticmethod
    def create_analysis_by_continent(continent_counts):

        # Create the bar chart
        fig = px.bar(continent_counts, 
                    x=continent_counts.index, 
                    y=continent_counts.values, 
                    title='Views by Continent',
                    labels={'x': 'Continent', 'y': 'Number of Views'})

        # Customize the layout
        fig.update_layout(
            title={'text': 'Views by Continent', 'x': 0.5, 'xanchor': 'center'},
            xaxis_title='Continent',
            yaxis_title='Number of Views',
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
            font=dict(family='Arial, sans-serif', size=12, color='black'),
            xaxis=dict(showgrid=False),  # Hide the x-axis gridlines
            yaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Light grey y-axis gridlines
        )

        # Customize the bar colors
        fig.update_traces(marker_color='rgb(67, 162, 202)', marker_line_color='rgb(27,120,55)',
                        marker_line_width=1.5, opacity=0.8)

        # Add hover template for more information on hover
        fig.update_traces(hovertemplate="<b>%{x}</b><br>Views: %{y}")

        return fig

    @staticmethod
    def saveAnalysisByCountry(country_counts, output_folder="output"):
        fig = GeoDataAnalyzer.create_analysis_by_country(country_counts)
        filename = f"{output_folder}/country_distribution.png"
        pio.write_image(fig, filename)
        print(f"\nCountry distribution plot saved as {filename}")

    def saveAnalysisByContinent(continent_counts, output_folder="output"):
        fig = GeoDataAnalyzer.create_analysis_by_continent(continent_counts)
        filename = f"{output_folder}/continent_distribution.png"
        pio.write_image(fig, filename)
        print(f"\nContinent distribution plot saved as {filename}")
