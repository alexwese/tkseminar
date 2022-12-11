import React, { useState, useEffect, useRef } from "react";
import Tree from "react-d3-tree";

import axios from "axios";

import orgChartJson from "../data/risk_data.json";
import { useCenteredTree, getGraph, setUser } from "./myGraphHelpers";
import "./myGraph.css";

import NodeInput from "./NodeInput";

import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";

const url = `http://localhost:8080`;

const renderForeignObjectNode = ({
  nodeDatum,
  toggleNode,
  foreignObjectProps,
}) => (
  <g>
    {/* `foreignObject` requires width & height to be explicitly set. */}
    <foreignObject {...foreignObjectProps}>
      <Card style={{ width: "18rem" }}>
        <ListGroup variant="flush">
          <ListGroup.Item>
            <h4>{nodeDatum.name}</h4>
          </ListGroup.Item>
          <NodeInput attributes={nodeDatum} />
          <ListGroup.Item>
            {nodeDatum.hasOwnProperty("children") ? (
              <Button onClick={toggleNode}>
                {nodeDatum.__rd3t.collapsed ? "+" : "-"}
              </Button>
            ) : (
              <Button onClick={toggleNode} disabled>
                {nodeDatum.__rd3t.collapsed ? "+" : "-"}
              </Button>
            )}
          </ListGroup.Item>
        </ListGroup>
      </Card>
    </foreignObject>
  </g>
);

const MyGraph = (props) => {
  //Set variables
  const [translate, containerRef] = useCenteredTree();
  const [graph, setGraph] = useState(null);
  const nodeSize = { x: 500, y: 400 };
  const foreignObjectProps = {
    width: nodeSize.x,
    height: nodeSize.y,
    x: -150,
    y: -100,
  };

  //Get Initial Newtork from API
  useEffect(() => {
    const getGraph = async () => {
      try {
        const response = await axios.get(url + "/build_network");
        setGraph(response.data);
      } catch (e) {
        console.log(e);
      }
    };
    getGraph();
  }, [props]);

  // Update Network after changes
  // TODO

  //Display Tree
  return (
    <>
      <div className="text-center">
        <div id="treeWrapper" style={{ width: "100%", height: "90vh" }}>
          {graph && (
            <Tree
              data={graph}
              translate={translate}
              nodeSize={nodeSize}
              renderCustomNodeElement={(rd3tProps) =>
                renderForeignObjectNode({ ...rd3tProps, foreignObjectProps })
              }
              orientation="horizontal"
            />
          )}
        </div>
      </div>
    </>
  );
};

export default MyGraph;
