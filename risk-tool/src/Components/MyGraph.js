import { Container } from "react-bootstrap";
import React from 'react';
import Tree from 'react-d3-tree';

const orgChart = {
  name: 'CEO',
  children: [
    {
      name: 'Manager',
      attributes: {
        department: 'Production',
      },
      children: [
        {
          name: 'Foreman',
          attributes: {
            department: 'Fabrication',
          },
          children: [
            {
              name: 'Worker',
            },
          ],
        },
        {
          name: 'Foreman',
          attributes: {
            department: 'Assembly',
          },
          children: [
            {
              name: 'Worker',
            },
          ],
        },
      ],
    },
  ],
};


function MyGraph(props) {
  return (
    <>
      <div className="text-center">
        <div id="treeWrapper" style={{ width: '50em', height: '20em' }}>
            <Tree data={orgChart} />
        </div>
      </div>
    </>
  );
}

export default MyGraph;