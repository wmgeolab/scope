import React, { useState, useRef, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "../../assets/css/workspace.css";
import { Container } from "@mui/material";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Form from "react-bootstrap/Form";
import { Button } from "react-bootstrap";
import InputGroup from "react-bootstrap/InputGroup";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import UnauthorizedView from "../UnauthorizedView";
import WorkspaceTable from "./WorkspaceTable";
import WorkspaceCreateModal from "./WorkspaceCreateModal";
import WorkspaceJoinModal from "./WorkspaceJoinModal";

const Workspaces = (props) => {
  const [filt, setFilt] = useState([]);
  const [dropDownValueSearch, setDropDownValueSearch] = useState("Name");
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const textInput = useRef("");
  const [errorMes, setErrorMes] = useState("");
  const [error, setError] = useState(true);

  const { loggedIn } = props;
  const [workspaceData, setWorkspaceData] = useState({
    id: null,
    name: null,
  });

  async function gatherWorkspaces() {
    const response = await fetch("http://127.0.0.1:8000/api/workspaces/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });
    const response_text = await response.json();
    try {
      const formattedResponse = response_text.results.map((result) => {
        return {
          id: result.workspace.id,
          name: result.workspace.name,
        };
      });
      if (formattedResponse) {
        setWorkspaceData(formattedResponse);
      }
    } catch (e) {
      console.log(e);
    }
  }

  useEffect(() => {
    gatherWorkspaces();
  }, []);

  async function triggerCreation(name, password) {
    let data = {
      name: name,
      password: password,
    };

    const response = await fetch("http://127.0.0.1:8000/api/workspaces/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });

    const response_text = await response.json();
    if (response_text.error) {
      // TODO: ADD UI ELEMENTS FOR SPECIFIC ERRORS.
      // E.G name already exists, ect...
      setErrorMes(response_text.error);
    } else setError(false);
  }

  async function triggerJoin(name, password) {
    let data = {
      name: name,
      password: password,
    };
    console.log(JSON.stringify(data), "in join");
    const response = await fetch("http://127.0.0.1:8000/api/workspaces/join/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });
    const response_text = await response.json();
    console.log(response_text);
    if (response_text.error) {
      // I don't think there should be any specific errors here
      // But if so..UI time.
      setErrorMes(response_text.error);
    } else setError(false);
  }

  const handleShowJoin = () => {
    setShowJoinModal(true);
  };
  const handleShowCreate = () => {
    setShowCreateModal(true);
  };
  const handleExitCreateModal = () => {
    setErrorMes("");
    setShowCreateModal(false);
  };
  const handleExitJoinModal = () => {
    setErrorMes("");
    setShowJoinModal(false);
  };

  const onSubmitSearch = (e) => {
    e.preventDefault();
    setFilt([
      {
        columnField: "name",
        operatorValue: "contains",
        value: textInput.current,
      },
    ]);
  };

  const handleKeywordChange = (value) => {
    textInput.current = value.target.value;
  };

  //TODO: Look into moving this into its own Component...
  const workspaceColumns = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "name",
      headerName: "Name",
      width: 250,

      renderCell: (cellValue) => {
        return (
          <a
            href={
              "/workspace/" + cellValue.formattedValue + "/id/" + cellValue.id
            }
          >
            {cellValue.formattedValue}
          </a>
        );
      },
    },
    {
      field: "tags",
      headerName: "Tags",
      flex: 1,
      renderCell: (tag_list) => {
        var tags_to_display;
        if (
          tag_list.formattedValue === null ||
          tag_list.formattedValue === undefined
        ) {
          tags_to_display = [];
        } else {
          tags_to_display = tag_list.formattedValue.split(",");
        }
        return (
          <Autocomplete
            multiple
            id="tags-filled"
            options={[]}
            defaultValue={tags_to_display}
            freeSolo
            fullWidth
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  label={option}
                  color="primary"
                  {...getTagProps({ index })}
                />
              ))
            }
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                label=""
                placeholder="Add tags"
              />
            )}
          />
        );
      },
    },
  ];

  if (loggedIn === false) {
    return <UnauthorizedView />;
  } else {
    return (
      <Container>
        <Row className="mt-5">
          <Col sm={6} />
          <Col sm={1}>
            <DropdownButton
              id="dropdown-basic-button"
              title={dropDownValueSearch}
              style={{ float: "right", marginLeft: "10px" }}
            >
              <Dropdown.Item
                onClick={(e) => setDropDownValueSearch(e.target.text)}
              >
                Name
              </Dropdown.Item>
              <Dropdown.Item
                onClick={(e) => setDropDownValueSearch(e.target.text)}
              >
                Tags
              </Dropdown.Item>
            </DropdownButton>
          </Col>
          <Col sm={5}>
            <Form onSubmit={onSubmitSearch}>
              <InputGroup>
                <Button aria-label="Search" onClick={onSubmitSearch}>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    className="bi bi-search"
                    viewBox="0 0 16 16"
                  >
                    <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                  </svg>
                </Button>
                {/* <Search onClick={handleKeywordChange}/> */}
                <Form.Control
                  placeholder={"Search by Workspace " + dropDownValueSearch}
                  onChange={(value) => handleKeywordChange(value)}
                  type="text"
                />
              </InputGroup>
            </Form>
          </Col>
          <WorkspaceTable
            data={workspaceData}
            columns={workspaceColumns}
            filters={filt}
          />
          <Row className="mt-4">
            <Col />
            <Col>
              <Button onClick={handleShowJoin}>Join Existing Workspace</Button>
            </Col>
            <Col>
              <Button onClick={handleShowCreate}>Create New Workspace</Button>
            </Col>
            <Col />
          </Row>
        </Row>
        <WorkspaceCreateModal
          showModal={showCreateModal}
          handleExitCreateModal={handleExitCreateModal}
          triggerCreation={triggerCreation}
          errorMes={errorMes}
          error={error}
        />
        <WorkspaceJoinModal
          showModal={showJoinModal}
          handleExitJoinModal={handleExitJoinModal}
          triggerJoin={triggerJoin}
          errorMes={errorMes}
          error={error}
        />
      </Container>
    );
  }
};
export default Workspaces;
