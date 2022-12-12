import React, { useState, useEffect, useRef } from "react";
import Tree from "react-d3-tree";

import axios from "axios";

import { useCenteredTree } from "./myGraphHelpers";
import "./myGraph.css";

import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";

import NodeInput from "./NodeInput";

import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";

const url = `http://localhost:8080`;

const renderForeignObjectNode = ({
  nodeDatum,
  toggleNode,
  foreignObjectProps,
  myGraphCallback,
}) => {
  const handleCallback = (data) => {
    myGraphCallback(data);
  };
  return (
    <g>
      {/* `foreignObject` requires width & height to be explicitly set. */}
      <foreignObject {...foreignObjectProps}>
        <Card
          style={{
            width: "18rem",
            borderRadius: "40px",
            backgroundColor: "#0094d8",
            color: "white",
            borderColor: "white",
          }}
        >
          <ListGroup variant="flush">
            <ListGroup.Item style={{ backgroundColor: "transparent" }}>
              <h4>{nodeDatum.name}</h4>
            </ListGroup.Item>
            <NodeInput attributes={nodeDatum} parentCallback={handleCallback} />
            <ListGroup.Item style={{ backgroundColor: "transparent" }}>
              {nodeDatum.hasOwnProperty("children") ? (
                <Button id="collapsable" onClick={toggleNode}>
                  {nodeDatum.__rd3t.collapsed ? <AddIcon /> : <RemoveIcon />}
                </Button>
              ) : (
                <Button
                  style={{ backgroundColor: "#003c7d86" }}
                  id="collapsable"
                  onClick={toggleNode}
                  disabled
                >
                  {nodeDatum.__rd3t.collapsed ? <AddIcon /> : <RemoveIcon />}
                </Button>
              )}
            </ListGroup.Item>
          </ListGroup>
        </Card>
      </foreignObject>
    </g>
  );
};

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
        const response = await axios.get(url + "/get_basenetwork");
        setGraph(response.data);
      } catch (e) {
        console.log(e);
      }
    };
    getGraph();
  }, [props]);

  //Loading screen
  if (!graph) {
    return <div>Loading...</div>;
  }

  //Update Network after changes
  function handleCallback(data) {
    setGraph(data);
  }

  //Display Tree
  return (
    <>
      <div className="text-center">
        <div id="treeWrapper" style={{ width: "100%", height: "90vh" }}>
          <Tree
            data={graph}
            translate={translate}
            nodeSize={nodeSize}
            renderCustomNodeElement={(rd3tProps) =>
              renderForeignObjectNode({
                ...rd3tProps,
                foreignObjectProps,
                myGraphCallback: handleCallback,
              })
            }
            orientation="horizontal"
          />
        </div>
      </div>
    </>
  );
};

export default MyGraph;
