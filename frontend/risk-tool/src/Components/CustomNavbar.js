import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";

function CustomNavbar() {
  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="#home">React Bootstrap</Navbar.Brand>
        </Container>
      </Navbar>
    </>
  );
}

export default CustomNavbar;
