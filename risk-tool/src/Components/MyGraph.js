import React, { useState } from "react";
import Tree from "react-d3-tree";

import orgChartJson from "../data/risk_data.json";
import { useCenteredTree } from "./myGraphHelpers";
import "./myGraph.css";

import NodeInput from "./NodeInput";

import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";

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
          <NodeInput attributes={nodeDatum.attributes} />
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

function MyGraph(props) {
  const [translate, containerRef] = useCenteredTree();
  const nodeSize = { x: 500, y: 500 };
  const foreignObjectProps = {
    width: nodeSize.x,
    height: nodeSize.y,
    x: -150,
    y: -100,
  };
  return (
    <>
      <div className="text-center">
        <div id="treeWrapper" style={{ width: "100%", height: "90vh" }}>
          <Tree
            data={orgChartJson}
            translate={translate}
            nodeSize={nodeSize}
            renderCustomNodeElement={(rd3tProps) =>
              renderForeignObjectNode({ ...rd3tProps, foreignObjectProps })
            }
            orientation="horizontal"
          />
        </div>
      </div>
    </>
  );
}

export default MyGraph;
