import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Neo4jProvider, createDriver } from 'use-neo4j';
import './index.css';

const driver = createDriver('neo4j', 'localhost', 7474, 'neo4j', 'test')

ReactDOM.render(
  <React.StrictMode>
    <Neo4jProvider driver={driver}>
      <App />
    </Neo4jProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
