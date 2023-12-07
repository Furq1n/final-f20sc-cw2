# importing necessary libraries and classes
import argparse
import sys
import subprocess
from src.analysis.data_handler import DataHandler 
from src.analysis.geoDataAnalyzer import GeoDataAnalyzer
from src.analysis.browserDataAnalyzer import BrowserDataAnalyzer
from src.analysis.viewerDataAnalyzer import ViewerDataAnalyzer
from src.analysis.alsoLikesAnalyzer import AlsoLikesAnalyzer

class CLIHandler:

    def __init__(self, args):
        self.args = args
    

    # Method to parse the command-line arguements
    def handle_task(self): 

        if not self.args.file_name: # checks if the user provided a file to analyze
               
            print("Error: file_name is required for all tasks except task 7") # if not we print an error
            sys.exit(1)

        mainData = DataHandler.load_data(self.args.file_name)

        if self.args.doc_uuid:

            data = DataHandler.filter_data(self.args.file_name, self.args.doc_uuid)

        else:

            # Load the data
            data = DataHandler.load_data(self.args.file_name)

        
        if self.args.task_id == '2a':

            country_count = GeoDataAnalyzer.get_country_counts(data)
            GeoDataAnalyzer.saveAnalysisByCountry(country_count)

        elif self.args.task_id == '2b':

            continent_count = GeoDataAnalyzer.get_continent_counts(data)
            GeoDataAnalyzer.saveAnalysisByContinent(continent_count)
            
        elif self.args.task_id == '3a':

            detailed_browser_data = BrowserDataAnalyzer.process_browser_data(data, detailed=True)
            BrowserDataAnalyzer.saveAnalysisByBrowser(detailed_browser_data,"detailed_browser_distribution")

        elif self.args.task_id == '3b':

            detailed_browser_data = BrowserDataAnalyzer.process_browser_data(data, detailed=False)
            BrowserDataAnalyzer.saveAnalysisByBrowser(detailed_browser_data,"browser_distribution",detailed=False)
            
        elif self.args.task_id == '4':
                
            top_readers = ViewerDataAnalyzer.calculate_reading_times(data)
            ViewerDataAnalyzer.print_top_readers(top_readers)

        elif self.args.task_id == '5d':
        
            if self.args.doc_uuid: #self.args.user_uuid and 

                analytics = AlsoLikesAnalyzer(mainData)
                top_liked_docs = analytics.get_top_10_also_likes(self.args.doc_uuid)
                analytics.print_top_liked_docs(top_liked_docs, self.args.doc_uuid)
                
            else:

                print("Error: doc_uuid is required for task 5d")
                sys.exit(1)

        elif self.args.task_id == '6':
            if self.args.user_uuid and self.args.doc_uuid:

                analytics = AlsoLikesAnalyzer(mainData)
                top_liked_docs = analytics.get_top_10_also_likes(self.args.doc_uuid)
                graph = analytics.create_also_likes_graph(self.args.doc_uuid, self.args.user_uuid, top_liked_docs)
                analytics.save_graph(graph, self.args.doc_uuid)

            else:
                print("Error: doc_uuid and visitor_uuid is required for task 6")
                sys.exit(1)
        
        elif self.args.task_id == '7':

            if self.args.user_uuid and self.args.doc_uuid:

                analytics = AlsoLikesAnalyzer(mainData)
                top_liked_docs = analytics.get_top_10_also_likes(self.args.doc_uuid)
                graph = analytics.create_also_likes_graph(self.args.doc_uuid, self.args.user_uuid, top_liked_docs)
                analytics.save_graph(graph, self.args.doc_uuid)

            else:
                print("Error: doc_uuid and visitor_uuid is required")
                sys.exit(1)

            try:
                
                subprocess.run(["streamlit", "run", "src/app/gui.py"], check=True)

            except subprocess.CalledProcessError as e:

                print("Failed to launch Streamlit app:", e)
                sys.exit(1)

    @staticmethod
    def parseCLI():

        parser = argparse.ArgumentParser(description="Document Analyzer CLI Interface")

        # Arguments to parse
        parser.add_argument('-u', '--user_uuid', type=str, help='This parameter takes in the user UUID for analysis')
        parser.add_argument('-d', '--doc_uuid', type=str, help='This parameter takes in the document UUID for analysis')
        parser.add_argument('-t', '--task_id', type=str, required=True, help='This parameter takes in the Task ID, to execute a particular task')
        parser.add_argument('-f', '--file_name', type=str, help='This parameter takes in the JSON file with input data')
        args, unknown = parser.parse_known_args()

        # Handle CLI logic based on arguments inputted
        if unknown:
            print(f"Unknown argument(s): {unknown}")
            parser.print_help()
            sys.exit(1)

        return args  # Return the parsed arguments
