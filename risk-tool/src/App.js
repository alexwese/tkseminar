import tklogo from "./Media/tksvg.svg";
import "./App.css";

import { Navbar, Container, Form, Row, Col, Image } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import MyGraph from "./Components/MyGraph";
import AppFooter from "./Components/AppFooter";
import { useState } from "react";
import { height } from "@mui/system";

function App() {
  const [user, setUser] = useState("User1");

  function handleChange(event) {
    setUser(event.target.value);
  }

  return (
    <div className="App">
      <header>
        <Navbar variant="dark" style={{ backgroundColor: "#0094d8" }}>
          <Container>
            <Navbar.Brand href="#home">
              <Image
                src={tklogo}
                style={{ height: "80px", marginRight: "8px" }}
                responsive
              ></Image>
              {/* <a style={{ color: "white" }}>thyssenkrupp</a>  */}
              <a style={{ marginLeft: "-280px", color: "white" }}>
                {" "}
                Risk Analysis Tool
              </a>
            </Navbar.Brand>
            <Navbar.Brand href="#home"></Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                <Row>
                  <Col style={{ marginTop: "7px", marginRight: "-15px" }}>
                    Signed in as:
                  </Col>
                  <Col>
                    <Form.Select
                      aria-label="Default select example"
                      onChange={handleChange}
                      value={user}
                    >
                      <option value="User1">User1</option>
                      <option value="User2">User2</option>
                    </Form.Select>
                  </Col>
                </Row>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        <Container id="body" fluid>
          <MyGraph props={user}></MyGraph>
        </Container>
        <AppFooter></AppFooter>
      </header>
    </div>
  );
}

export default App;
