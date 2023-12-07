from graphviz import Digraph
import pandas as pd
from tabulate import tabulate
import os

class AlsoLikesAnalyzer:

    def __init__(self, df):
        self.df = df

    """ Function 5(a) """
    """ Return unique reader UUIDs for a given document. """
    def get_reader_uuids_for_document(self, document_uuid):
        
        return self.df[self.df['subject_doc_id'] == document_uuid]['visitor_uuid'].unique()

    """ Function (b) """
    """ Return unique document UUIDs read by a given visitor. """
    def get_document_uuids_read_by_visitor(self, visitor_uuid):
       
        return self.df[self.df['visitor_uuid'] == visitor_uuid]['subject_doc_id'].unique()

    """ Function (c) """
    """ Calculate documents also liked by the readers of a particular document. """
    def also_likes(self, document_uuid):
        
        reader_uuids = self.get_reader_uuids_for_document(document_uuid)

        liked_docs_list = []
        for uuid in reader_uuids:

            docs_read_by_visitor = self.get_document_uuids_read_by_visitor(uuid)

            liked_docs_list.extend(docs_read_by_visitor)
           
        liked_docs = pd.Series(liked_docs_list).value_counts()
        return liked_docs

    def get_top_10_also_likes(self, document_uuid):
        """ Retrieve the top 10 also liked documents. """
        liked_docs = self.also_likes(document_uuid)[:10]
        return liked_docs
    
    def print_top_liked_docs(self, top_liked_docs, document_uuid):
        """ Print the top liked documents in a tabular format for a specific document. """
        print(f"\nDocuments also liked by readers of doc id: {document_uuid}\n")
        
        if top_liked_docs.empty:
            print("No top liked documents found.")
            return
        
        # Convert the Series to a DataFrame for display
        top_liked_docs_df = top_liked_docs.reset_index()
        top_liked_docs_df.columns = ['Document UUID', 'Read Count']
        
        # Convert DataFrame to a table string using tabulate
        table = tabulate(top_liked_docs_df, headers='keys', tablefmt='grid', showindex=True)
        print(table)

    def create_also_likes_graph(self, document_uuid, visitor_uuid, top_liked_docs):
        """ Create a graph visualization for the top also liked documents. """
        graph = Digraph('Top10AlsoLikes', format='png')
        graph.attr(rankdir='LR')
        reader_uuids = self.get_reader_uuids_for_document(document_uuid)
 
        doc_list = top_liked_docs.index.tolist()
 
        # for doc_uuid, _ in top_liked_docs.iteritems():
        for doc_uuid in doc_list:
            label = doc_uuid[-4:]
            doc_color = 'green' if doc_uuid == document_uuid else 'lightblue'
            graph.node(doc_uuid, label=label, shape='box', style='filled', color=doc_color)
           
            users = self.get_reader_uuids_for_document(doc_uuid)
            for user in users:
                if user in reader_uuids:
                    user_color = 'green' if user == visitor_uuid else 'lightpink'
                    edge_color = 'green' if user == visitor_uuid else 'black'
                    labelv = user[-4:]
                    graph.node(user, label=labelv, shape='ellipse', style='filled', color=user_color)
                    graph.edge(user, doc_uuid, label='Likes', color=edge_color)
       
        return graph
    
    def save_graph(self, graph, document_uuid, output_dir='output'):
        """ Save the graph to a file in the specified output directory. """
        # Create the output directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Specify the filename for the graph
        filename = os.path.join(output_dir, f"also_likes_graph_{document_uuid}.png")

        # Render and save the graph
        graph.render(filename=filename, format='png', cleanup=True)
        print(f"Graph saved as {filename}")