import logo from "./logo.svg";
import "./App.css";

import { Button, Navbar, Container } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import MyGraph from "./Components/MyGraph";
import AppFooter from "./Components/AppFooter";
import { useState } from "react";

function App() {
  const [user, setUser] = useState("User1");
  return (
    <div className="App">
      <header>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand href="#home">Risk Tool</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                Signed in as: <a href="#login">{user}</a>
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
