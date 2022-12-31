import React from 'react';
import { useReadCypher } from 'use-neo4j';
import './App.css';
import { Graph } from 'graphology';

//import { Stage, Text } from "react-pixi-fiber/index.js";


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
      console.log(first)

      const count = records.length
      result = (<div>There are {count} nodes in the database.</div>)
      
      // Initialize and populate Graphology graph with data
      const graph = new Graph();
      records.forEach((record)=> {
        const pattern = record.get('ptrn')
        const node_id = pattern.properties.id
        
        graph.addNode(node_id, {
          group: pattern.properties.group,
          name: pattern.properties.name,
          headline: pattern.properties.headline
        })
      })
      
      // assign layout positions as `x`, `y` node attributes
      graph.forEachNode(node => {
        graph.setNodeAttribute(node, 'x', Math.random());
        graph.setNodeAttribute(node, 'y', Math.random());
      });

      // Print node attribtues to console
      graph.forEachNode(node => {
        console.log(graph.getNodeAttributes(node))
      });
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