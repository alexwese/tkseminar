import React from "react";
import Tree from "react-d3-tree";

import orgChartJson from "../data/risk_data.json";
import { useCenteredTree } from "./myGraphHelpers";
import "./myGraph.css";

//Bootstrap
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";

const renderForeignObjectNode = ({
  nodeDatum,
  toggleNode,
  foreignObjectProps,
}) => (
  <g>
    <circle r={15}></circle>
    {/* `foreignObject` requires width & height to be explicitly set. */}
    <foreignObject {...foreignObjectProps}>
      <Card style={{ width: "18rem" }}>
        <ListGroup variant="flush">
          <ListGroup.Item>
            <h4>{nodeDatum.name}</h4>
          </ListGroup.Item>
          <ListGroup.Item>Base Value: </ListGroup.Item>
          <ListGroup.Item>
            <InputGroup className="mb-3">
              <InputGroup.Text id="inputGroup-sizing-default">
                Default
              </InputGroup.Text>
              <Form.Control
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
              />
            </InputGroup>
          </ListGroup.Item>
        </ListGroup>
      </Card>

      {/* <div style={{ border: "1px solid black", backgroundColor: "#dedede" }}>
        <h3 style={{ textAlign: "center" }}>{nodeDatum.name}</h3>
        {nodeDatum.children && (
          <button style={{ width: "100%" }} onClick={toggleNode}>
            {nodeDatum.__rd3t.collapsed ? "Expand" : "Collapse"}
          </button>
        )}
      </div> */}
    </foreignObject>
  </g>
);

function MyGraph(props) {
  const [translate, containerRef] = useCenteredTree();
  const nodeSize = { x: 500, y: 500 };
  const foreignObjectProps = { width: nodeSize.x, height: nodeSize.y, x: 20 };
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
