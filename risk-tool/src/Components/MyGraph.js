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
  user,
  myGraphCallback,
}) => {
  const handleCallback = (data) => {
    myGraphCallback(data);
  };

  if (nodeDatum.attributes.lvl === 0) {
    const colorhex = "#0094D8";
  } else if (nodeDatum.attributes.lvl === 1) {
    const colorhex = "#007DB8";
  } else {
    const colorhex = "#00628F";
  }

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
              <div>{nodeDatum.attributes.lvl}</div>
            </ListGroup.Item>
            <NodeInput
              attributes={{ nodeDatum, user }}
              parentCallback={handleCallback}
            />
            <ListGroup.Item style={{ backgroundColor: "transparent" }}>
              {nodeDatum.children.length === 0 ? (
                <Button
                  style={{ backgroundColor: "#003c7d20" }}
                  id="collapsable"
                  onClick={toggleNode}
                  disabled
                >
                  {nodeDatum.__rd3t.collapsed ? <AddIcon /> : <RemoveIcon />}
                </Button>
              ) : (
                <Button id="collapsable" onClick={toggleNode}>
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
  const [user, setUser] = useState(props.props);
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
        const response = await axios.get(url + "/get_usernetwork", {
          params: { username: props.props },
        });
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
    data.username = props.props;
    console.log(data);
    axios.post(url + "/change_network", data).then((res) => {
      console.log(res.data);
      setGraph(res.data);
    });
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
                user,
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
