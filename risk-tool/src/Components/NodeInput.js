import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

import "./nodeInput.css";

//Bootstrap
import Form from "react-bootstrap/Form";
import ListGroup from "react-bootstrap/ListGroup";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Collapse from "react-bootstrap/Collapse";

import EditIcon from "@mui/icons-material/Edit";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

const url = `http://localhost:8080`;

export default function NodeInput(props) {
  const [open, setOpen] = useState(false);

  const [expChange, setExpChange] = useState(
    props.attributes.attributes.expected_change
  );

  const [expValue, setExpValue] = useState(
    props.attributes.attributes.new_expected_value
  );

  const [baseValue, setBaseValue] = useState(
    props.attributes.attributes.initial_regression_value
  );

  useEffect(() => {
    setExpChange(props.attributes.attributes.expected_change);
    setExpValue(props.attributes.attributes.new_expected_value);
    setBaseValue(props.attributes.attributes.initial_regression_value);
  }, [props]);

  const handleChange = (event) => {
    console.log(event.target.value);
    setExpChange(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    var dataObject = {
      id: props.attributes.attributes.node_id,
      expChange: expChange,
    };

    axios.post(url + "/change_network", dataObject).then((res) => {
      props.parentCallback(res.data);
    });
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSubmit();
    }
  };
  return (
    <>
      <ListGroup.Item style={{ backgroundColor: "transparent" }}>
        <Form.Group
          as={Row}
          className="mb-3"
          controlId="formPlaintextEmail"
          style={{
            color: "white",
          }}
        >
          <Form.Label column sm="5">
            Expected Value
          </Form.Label>
          <Col sm="5">
            <Form.Control
              style={{ marginTop: "12px", color: "white" }}
              plaintext
              readOnly
              type="number"
              value={expValue}
            />
          </Col>
          <Col sm="2">
            {props.attributes.name !== "Aluminium price" && (
              <Button
                id="edit"
                onClick={() => setOpen(!open)}
                aria-controls="example-collapse-text"
                aria-expanded={open}
              >
                <EditIcon id="pencil" />
              </Button>
            )}
          </Col>
        </Form.Group>
      </ListGroup.Item>
      <Collapse in={open}>
        <div id="example-collapse-text">
          <form onSubmit={handleSubmit}>
            <Form.Group
              as={Row}
              className="mb-3"
              controlId="formPlaintextPassword"
            >
              <Form.Label column sm="5">
                Expected Change
              </Form.Label>
              <Col sm="5">
                <Form.Control
                  type="number"
                  value={expChange}
                  style={{ marginTop: "16px" }}
                  onChange={handleChange}
                  onKeyDown={handleKeyDown}
                />
              </Col>
              <Col sm="2">
                <Button id="submit" type="submit">
                  <ArrowForwardIosIcon id="pencil" />
                </Button>
              </Col>
            </Form.Group>

            <Form.Group as={Row} className="mb-3">
              <Form.Label column sm="5">
                Base Value
              </Form.Label>
              <Col sm="7">
                <Form.Control
                  style={{ color: "white" }}
                  plaintext
                  readOnly
                  type="number"
                  value={baseValue}
                />
              </Col>
            </Form.Group>
          </form>
        </div>
      </Collapse>
    </>
  );
}
