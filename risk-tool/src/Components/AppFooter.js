import { Container, Navbar, NavbarBrand } from "react-bootstrap";

function AppFooter() {
  return (
    <div>
      <Navbar bg="dark" variant="dark">
        <Container>
          <NavbarBrand>Footer</NavbarBrand>
        </Container>
      </Navbar>
    </div>
  );
}
export default AppFooter;