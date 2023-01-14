from neo4j import GraphDatabase
import pandas as pd
import numpy as np

import argparse
parser = argparse.ArgumentParser(prog = 'python dataLoad.py',
                    description = 'Seed Neo4j database',
                    epilog = 'Meaning++Maps')
parser.add_argument("-p", "--process", required=True)
args = parser.parse_args()

try:
    PROCESS = int(args.process)
    if PROCESS not in [0,1]:
        raise ValueError
except:
    raise ValueError(f'input supplied to --process should be 0 or 1, not {args.process}')

####
##  Database management
####

# List databases
# Switch active database
# Empty out a target database

####
##  Seed databases for Pattern Language / Wittgenstein / Free Association game
####

# A Pattern Language
patterns = pd.read_excel('A Pattern Language.xlsx', index_col='id').reset_index()
print(patterns.columns)
print(patterns.head())

# Hardcode a list of images
images = {
    'img1': {
        's3_link': {},
        'is_example_of': {} # list of pattern id's
    }

}


# Note: This way of assigning IDs does not prevent id conflict...
class Pattern:
    def __init__(self, id, name, headline, group):
        self.id = id
        self.name = self.escape_quotes(name)
        self.headline = self.escape_quotes(headline)
        self.group = group

    def escape_quotes(self, txt):
        return txt.replace("'", "\\'")

    def create_node_cypher(self):
        return f"CREATE(a: Pattern {{id: {self.id}, name: '{self.name}', headline: '{self.headline}', group: {self.group}}})"

class Image:
    def __init__(self, id, s3_link):
        self.id = id
        self.s3_link = s3_link

    def create_node_cypher(self):
        return f"CREATE(a: Image {{id: {self.id}, s3_link: {self.s3_link}}})"


# This doesn't account for structure in the desired set of relationships yet
class Connection:
    def __init__(self, node_type1, node_type2, node_id1, node_id2, relationship_type):
        self.node_type1 = node_type1
        self.node_type2 = node_type2
        self.node_id1 = node_id1
        self.node_id2 = node_id2
        self.relationship_type = relationship_type

    def create_edge_cypher(self):
        try:
            return f'''
                MATCH
                  (a:{self.node_type1}),
                  (b:{self.node_type2})
                WHERE a.id  = {int(self.node_id1)} AND b.id = {int(self.node_id2)}
                CREATE (a)-[r:{self.relationship_type}]->(b)
            '''.replace('\n', '').strip()
        except:
            return ''

def create_pattern_nodes(row):
    pttrn = Pattern(row.id, row['Pattern Name'], row.Headline, row.Group)
    return pttrn.create_node_cypher()

def create_pattern_edges(row, relationship_type):
    node_id1 = row.id
    if relationship_type == 'contains':
        node_id2s = str(row['Smaller Patterns']).split(',')
    elif relationship_type == 'contained_by':
        node_id2s = str(row['Bigger Patterns']).split(',')
    else:
        raise ValueError('Unknown relationship type between patterns')

    def craft_edge_cypher(node_id2):
        cnnx = Connection('Pattern', 'Pattern', node_id1, node_id2, relationship_type)
        return cnnx.create_edge_cypher()

    edge_cyphers = map(craft_edge_cypher, node_id2s)
    return list(edge_cyphers)

patterns['node_cypher'] = patterns.apply(create_pattern_nodes, axis=1)
patterns['contains_relationships'] = patterns.apply(lambda row: create_pattern_edges(row, 'contains'), axis=1)
patterns['contained_by_relationships'] = patterns.apply(lambda row: create_pattern_edges(row, 'contained_by'), axis=1)

# Pattern information, number of rows is number of nodes
print(patterns)

# Number of edges to creategit
patterns['contains_count'] = patterns['Smaller Patterns'].apply(lambda val: len(str(val).split(',')) if val not in ('', None, np.nan) else 0)
patterns['contained_by_count'] = patterns['Bigger Patterns'].apply(lambda val: len(str(val).split(',')) if val not in ('', None, np.nan) else 0)
print("total relationships", patterns['contains_count'].sum() + patterns['contained_by_count'].sum())

# To do: update this to be controlled by a command line arg
if PROCESS:
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri) # , auth=("neo4j", "testpassword")

    with driver.session() as session:
        def try_sesh(session, txt):
            try:
                session.run(txt)
            except BaseException as e:
                print("Error on processing", txt, e)

        def try_sesh_list(session, txt_list):
            for txt in txt_list:
                try_sesh(session, txt)

        # Clear all existing nodes and relationships
        session.run('MATCH (n) DETACH DELETE n')
        # Todo: Is there a way to run a list of queries at the same time? Will this optimize?
        patterns['node_cypher'].apply(lambda txt: try_sesh(session, txt))
        patterns['contains_relationships'].apply(lambda txt: try_sesh_list(session, txt))
        patterns['contained_by_relationships'].apply(lambda txt: try_sesh_list(session, txt))

    driver.close()


####
##  Sample connection
####
#
# uri = "neo4j://localhost:7687"
# driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))
#
# def create_person(tx, name):
#     tx.run("CREATE (a:Person {name: $name})", name=name)
#
# def create_friend_of(tx, name, friend):
#     tx.run("MATCH (a:Person) WHERE a.name = $name "
#            "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
#            name=name, friend=friend)
#
# with driver.session() as session:
#     session.execute_write(create_person, "Alice")
#     session.execute_write(create_friend_of, "Alice", "Bob")
#     session.execute_write(create_friend_of, "Alice", "Carl")
#
# driver.close()