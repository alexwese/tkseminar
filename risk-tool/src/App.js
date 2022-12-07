import logo from "./logo.svg";
import "./App.css";

import { Button, Navbar, Container } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

import MyGraph from "./Components/MyGraph";

function App() {
  return (
    <div className="App">
      <header>
        <Navbar bg="dark" variant="dark">
          <Container>
            <Navbar.Brand href="#home">Risk Tool</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                Signed in as: <a href="#login">User</a>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
        {/* <MyGraph /> */}
      </header>
    </div>
  );
}

export default App;
