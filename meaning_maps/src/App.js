import React from 'react';
import { useReadCypher } from 'use-neo4j';
import './App.css';
import { Graph } from 'graphology';
import { PixiGraph } from 'pixi-graph';


function App() {
  
  const { cypher, error, loading, first, records } = useReadCypher('MATCH (ptrn:Pattern) RETURN ptrn')  

  // Default to Loading Message
  let result = (<div className="ui active dimmer">Loading...</div>)

  // Was there an error om the query?
  if ( error ) {
    result = (<div className="ui negative message">{ error.message }</div>)
  }
  else if ( !loading ) {
    // Get the count
    if (first) {

      // console.log(records)
      console.log(first)

      const count = records.length

      const graph = new Graph();
      // populate Graphology graph with data
      // assign layout positions as `x`, `y` node attributes

      records.forEach((record)=> {
        const pattern = record.get('ptrn')
        const node_id = pattern.properties.id
        
        graph.addNode(node_id, {
          group: pattern.properties.group,
          name: pattern.properties.name,
          headline: pattern.properties.headline
        })
      })
      

      const style = {
        node: {
          color: '#00FF00',
          label: {
            content: node => node.name,
            fontFamily: 'HelveticaRegular',
          },
        },
        edge: {
          color: '#000000',
        },
      };

      graph.forEachNode(node => {
        graph.setNodeAttribute(node, 'x', Math.random());
        graph.setNodeAttribute(node, 'y', Math.random());
      });

      graph.forEachNode(node => {
        console.log(graph.getNodeAttributes(node))
      });

      const resources = [
        { name: 'HelveticaRegular', url: 'https://gist.githubusercontent.com/zakjan/b61c0a26d297edf0c09a066712680f37/raw/8cdda3c21ba3668c3dd022efac6d7f740c9f1e18/HelveticaRegular.fnt' },
      ];

      const pixiGraph = new PixiGraph({
        container: document.getElementById('graph'),
        graph,
        style,
        resources
      });

      result = (<div>There are {count} nodes in the database.</div>)
    }
  }

  return (
    <div className="App">
      <pre>{result}</pre>
      <div id='graph'></div>
    </div>
  );

}

export default App;