from user_agents import parse
import plotly.express as px
import plotly.io as pio

class BrowserDataAnalyzer:

    def process_browser_data(df, detailed = False):

        if detailed:
            df['browser'] = df['visitor_useragent'].astype(str)
        else:
            df['browser'] = df['visitor_useragent'].apply(lambda ua: parse(ua).browser.family if ua else "Unknown")
        return df['browser'].value_counts()
    
    def create_analysis_by_main_browser(browser_data):

        # Create the bar chart
        fig = px.bar(browser_data, 
                     x=browser_data.index, 
                     y=browser_data.values, 
                     title='Document Views by Browsers',
                     labels={'x': ' ', 'y': 'Number of Views'})

        # Customize the layout
        fig.update_layout(
            title={'text': 'Views by Browser', 'x': 0.5, 'xanchor': 'center'},
            xaxis_title=' ',
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

    def create_bar_chart_browser(data, title, detailed=False):

        # showlabel= False if detailed else True
        showlabel = True
        fig = px.bar(data, x=data.index, y=data.values, title=title,
                 labels={'x':'Browser', 'y': 'Counts'})
        
        fig.update_layout(
        title={'text': title, 'x': 0.5, 'xanchor': 'center'},
        #xaxis_title="Browser",
        yaxis_title="Counts",
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        font=dict(family='Arial, sans-serif', size=12, color='black'),
        xaxis=dict(showgrid=False, showticklabels=showlabel),  # Hide the x-axis gridlines
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Light grey y-axis gridlines
        )


        fig.update_traces(marker_color='rgb(29, 105, 150)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8)

        # Add hover template for more information on hover
        fig.update_traces(hovertemplate=f"<b>%{data.index}</b><br>counts: %{{y}}")
        return fig
    
    def saveAnalysisByBrowser(browser_counts, file_name, output_folder="output",detailed=False):
        fig = BrowserDataAnalyzer.create_bar_chart_browser(browser_counts,"Views by Browser",detailed)
        filename = f"{output_folder}/{file_name}.png"
        pio.write_image(fig, filename)
        print(f"Browser distribution plot saved as {filename}")