import React, { useState } from "react";

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

export default function NodeInput(nodeDatum) {
  // console.log(JSON.stringify(nodeDatum.attributes.attributes.absolute_val));

  const [open, setOpen] = useState(false);
  const [expChange, setExpChange] = useState(
    nodeDatum.attributes.attributes.expected_change
  );
  const [expValue, setExpValue] = useState(
    nodeDatum.attributes.attributes.absolute_val
  );

  const [baseValue, setBaseValue] = useState(
    nodeDatum.attributes.attributes.base_val
  );

  //HTTP Connectionvar
  var url = "https://reqbin.com/echo/post/json";
  var xhr = new XMLHttpRequest();

  const handleChange = (event) => {
    // Get input value from "event"
    setExpChange(event.target.value);
    // if (event.target.value != null) {
    //   setExpValue(parseFloat(event.target.value) + parseFloat(baseValue));
    // }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("do validate");
    console.log("new change", { expChange });
    xhr.open("POST", url);

    xhr.setRequestHeader(
      "Authorization",
      "Bearer mt0dgHmLJMVQhvjpNXDyA83vA_PxH23Y"
    );
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        console.log(xhr.status);
        console.log(xhr.responseText);
      }
    };

    var dataObject = {
      id: nodeDatum.attributes.name,
      expChange: expChange,
    };

    console.log(JSON.stringify(dataObject));

    xhr.send(dataObject);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <>
      <ListGroup.Item>
        <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
          <Form.Label column sm="4">
            Expected Value
          </Form.Label>
          <Col sm="6">
            <Form.Control plaintext readOnly type="number" value={expValue} />
          </Col>
          <Col sm="2">
            <Button
              id="edit"
              onClick={() => setOpen(!open)}
              aria-controls="example-collapse-text"
              aria-expanded={open}
            >
              <EditIcon id="pencil" />
            </Button>
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
              <Form.Label column sm="4">
                Expected Change
              </Form.Label>
              <Col sm="6">
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
