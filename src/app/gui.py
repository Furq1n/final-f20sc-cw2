import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import streamlit.components.v1 as components

# Get the directory of the current file (src/app/)
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory (src/)
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from analysis.geoDataAnalyzer import GeoDataAnalyzer
from analysis.data_handler import DataHandler
from analysis.browserDataAnalyzer import BrowserDataAnalyzer
from analysis.viewerDataAnalyzer import ViewerDataAnalyzer
from analysis.alsoLikesAnalyzer import AlsoLikesAnalyzer


class StreamlitApp:

    def __init__(self):
        self.df = None
        self.setup_page()

    def setup_page(self):
        st.set_page_config(page_title="Document Viewer Analysis", layout="wide")
        st.title("📊 Document Viewer Analysis")
        st.markdown("---")

    def upload_data(self):
        with st.sidebar:
            st.header("📁 Data Upload")
            uploaded_file = st.file_uploader("Choose a JSON file", type="json")
            if uploaded_file is not None:
                self.df = DataHandler.load_data(uploaded_file)
            return uploaded_file

    def display_file_info(self, df):
            """Display initial information about the uploaded file."""
            st.write("## File Overview")
            st.write("Here's a quick overview of the uploaded file:")
            st.dataframe(df.head())  # Show the first few rows of the dataframe
            st.write(f"**Total rows: {len(df)}**")  # Display the total number of rows in the dataframe

    def input_fields(self):
        with st.sidebar:
            document_uuid = st.text_input("Document UUID",
                                          placeholder="Enter Document UUID or leave blank",
                                          help="Enter the UUID of the document you want to analyze. "
                                               "Leave this field blank to analyze all documents.")
            visitor_uuid_input = st.text_input("Visitor UUID",
                                               placeholder="Enter Visitor UUID",
                                               help="Enter the UUID of the visitor for more detailed analysis. "
                                                    "This field is required for generating the graph.")

            return document_uuid, visitor_uuid_input

    def analysis_options(self):
        with st.sidebar:
            st.markdown("---")
            st.header("📈 Analysis Options")
            show_country = st.button('Views by Country')
            show_continent = st.button('Views by Continent')
            show_detailed_browser = st.button('Views by Detailed Browser Data')
            show_main_browser = st.button('Views by Main Browser Data')
            show_top_readers = st.button('Top Reader Profiles')
            show_also_likes = st.button('Recommended Documents')
            show_graph = st.button('Recommended Documents Graph')
            return show_country, show_continent, show_detailed_browser, show_main_browser, show_top_readers, show_also_likes, show_graph
        
    def display_country_analysis(self, filtered_df):

        """Display the analysis for views by country with a descriptive markdown."""
        st.markdown("""
            ## Distribution of Views by Country
            Below is a bar chart representing the number of views per country. Hover over the bars to see the exact number of views.
        """, unsafe_allow_html=True)

        country_count = GeoDataAnalyzer.get_country_counts(filtered_df)
        fig = GeoDataAnalyzer.create_analysis_by_country(country_count)
        
        # Optionally customize the Plotly figure with a theme or layout adjustments
        fig.update_layout(
            title='Document Views by Country',
            title_x=0.5,
            xaxis_title='Country',
            yaxis_title='Number of Views',
            template='plotly_white',  # Choose a template that fits your aesthetic needs
            # other layout options...
        )

        st.plotly_chart(fig, use_container_width=True)
    
    

    def display_continent_analysis(self, data):
        """Display the analysis for views by continent with a descriptive markdown."""
        st.markdown("""
            ## Distribution of Views by Continent
            The bar chart below illustrates the number of document views categorized by continent.
            Hover over the bars to see detailed counts for each continent.
        """, unsafe_allow_html=True)

        continent_count = GeoDataAnalyzer.get_continent_counts(data)
        fig = GeoDataAnalyzer.create_analysis_by_continent(continent_count)
        
        # Customize the Plotly figure with a theme or layout adjustments
        fig.update_layout(
            title='Document Views by Continent',
            title_x=0.5,
            xaxis_title='Continent',
            yaxis_title='Number of Views',
            hovermode='closest',
            template='plotly_white',

        )

        # Add hover data to the figure
        fig.update_traces(
            hoverinfo='y+x',
        )

        st.plotly_chart(fig, use_container_width=True)

    def display_main_browser_analysis(self, data):
        """Display the analysis for main browser categories with a descriptive markdown."""
        st.markdown("""
            ## Browser Usage Distribution
            The bar chart below illustrates the distribution of views across different main browser categories.
            Hover over each segment to view the number of views associated with each browser.
        """, unsafe_allow_html=True)

        # Process the browser data (assumes this returns a Series with browser counts)
        browser_data = BrowserDataAnalyzer.process_browser_data(data, detailed=False)
        
        # Use the new function to create the chart
        fig = BrowserDataAnalyzer.create_analysis_by_main_browser(browser_data)

        # Customize the Plotly figure with a theme or layout adjustments
        fig.update_layout(
            title='Document Views by Main Browser',
            title_x=0.5,
            xaxis_title='Browser',
            yaxis_title='Number of Views',
            hovermode='closest',
            template='plotly_white',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def display_browser_analysis(self, data):
        """Display the analysis for main browser categories with a descriptive markdown."""
        st.markdown("""
            ## Browser Usage Distribution
            The bar chart below illustrates the distribution of views across different browser categories.
            Hover over each segment to view the number of views associated with each browser.
        """, unsafe_allow_html=True)

        # Process the browser data (assumes this returns a Series with browser counts)
        browser_data = BrowserDataAnalyzer.process_browser_data(data, detailed=True)
        
        # Use the new function to create the chart
        fig = BrowserDataAnalyzer.create_analysis_by_main_browser(browser_data)

        # Customize the Plotly figure with a theme or layout adjustments
        fig.update_layout(
            title='Document Views by Browsers',
            title_x=0.5,
            xaxis_title='  ',
            yaxis_title='Number of Views',
            hovermode='closest',
            template='plotly_white',
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_top_readers(self, data):
        """Display the top readers in a formatted table with a title and description."""
        st.markdown("""
            ## Top Readers by Read Time
            The table below lists the top 10 readers by total read time in  milliseconds.
            This information provides insights into the most engaged users.
        """, unsafe_allow_html=True)

        top_readers =  ViewerDataAnalyzer.calculate_reading_times(data) # Replace with your actual method call
        if top_readers is not None and not top_readers.empty:
            # Convert the Series to a DataFrame for displaying as a table
            top_readers_df = top_readers.reset_index()
            top_readers_df.columns = ['Visitor UUID', 'Total Read Time (Milliseconds)']
            st.table(top_readers_df)
        else:
            st.write("No top readers found.")

    def display_also_likes(self, mainData, document_uuid):
        """Display the top liked documents in a tabular format within Streamlit."""
        st.markdown(f"""
            ## Recommended Documents       
            
            **Documents also liked by readers of Document ID: {document_uuid}**

            The table below lists documents that readers of the specified document also liked.
        """, unsafe_allow_html=True)

        analytics = AlsoLikesAnalyzer(mainData)
        top_liked_docs = analytics.get_top_10_also_likes(document_uuid)
        
        if top_liked_docs.empty:
            st.write("No top liked documents found.")
        else:
            # Convert the Series to a DataFrame for display
            top_liked_docs_df = top_liked_docs.reset_index()
            top_liked_docs_df.columns = ['Document UUID', 'Read Count']
            st.table(top_liked_docs_df)

    # Assuming 'graph' is a Graphviz dot object
    def display_graphviz(self,mainData, document_uuid, user_uuid):

        st.markdown(f"""
            ## Recommended Documents Graph       
            
            **Graph of documents also liked by readers of Document ID: {document_uuid}**

            The graph below maps documents that readers of the specified document also liked.
        """, unsafe_allow_html=True)

        analytics = AlsoLikesAnalyzer(mainData)
        top_liked_docs = analytics.get_top_10_also_likes(document_uuid)
        graph = analytics.create_also_likes_graph(document_uuid, user_uuid, top_liked_docs)

        svg = graph.pipe(format='svg').decode('utf-8')

       # Estimate height: 100 pixels for each node or row of nodes
        estimated_height_per_node = 25
        number_of_nodes = len(graph.body)  # Simplistic estimation; customize as needed
        dynamic_height = estimated_height_per_node * number_of_nodes

        # Custom CSS to center the graph
        css = """
        <style>
            .graphviz-container {
                display: flex;
                justify-content: center;
            }
        </style>
        """

        # Use the components module to render raw HTML with the custom CSS and dynamic height
        components.html(f"{css}<div class='graphviz-container'>{svg}</div>", height=dynamic_height)

    def display_analysis(self, document_uuid, visitor_uuid_input, options):
        show_country, show_continent, show_detailed_browser, show_main_browser, show_top_readers, show_also_likes, show_graph = options

        mainData = self.df

        if document_uuid:

            data = self.df[self.df['subject_doc_id'] == document_uuid]

        else:

            data = self.df

        if show_country:

            self.display_country_analysis(data)

        if show_continent:
                
             self.display_continent_analysis(data)

        if show_detailed_browser:
                
            self.display_browser_analysis(data)

            # detailed_browser_data = process_browser_data(filtered_df, detailed=True)
            # detailed_fig = plot_browser_histogram(detailed_browser_data, "Views by Detailed Browser Info")
            # st.plotly_chart(detailed_fig, use_container_width=True)
        
        if show_main_browser:
                
            self.display_main_browser_analysis(data)

        if show_top_readers:

             self.display_top_readers(data)

        if show_also_likes and document_uuid:

            self.display_also_likes(mainData,document_uuid)

        elif show_also_likes:
            st.warning("Please enter a Document UUID to view the list of recommended documents.")
        
        if show_graph and document_uuid and visitor_uuid_input:
                
            self.display_graphviz(mainData,document_uuid,visitor_uuid_input)

        elif show_graph:
            st.warning("Please enter a Document UUID and Visitor UUID to view the list of recommended documents.")

    def run(self):
        uploaded_file = self.upload_data()

        if uploaded_file is not None:

            document_uuid, visitor_uuid_input = self.input_fields()
            options = self.analysis_options()

            # Check if any analysis option has been selected
            if any(options):

                self.display_analysis(document_uuid, visitor_uuid_input, options)

            else:

                # If no option is selected, display the file info
                self.display_file_info(self.df)

        else:
            st.info("Please upload a file to begin analysis.")

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()