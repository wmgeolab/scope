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
import { Search } from "react-bootstrap-icons";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import UnauthorizedView from "../UnauthorizedView";
import WorkspaceTable from "./WorkspaceTable";
import WorkspaceCreateModal from "./WorkspaceCreateModal";
import WorkspaceJoinModal from "./WorkspaceJoinModal";
import { useNavigate } from "react-router-dom";

// Workspaces is the parent page of all workspace related components
const Workspaces = (props) => {
  // This is set in onSubmitSearch and is passed to WorkspaceTable
  // Puts the keyword based filter (stored in textInput) in a filter format for MUI DataGrid
  const [filt, setFilt] = useState([]);
  // This controls that when a keyword search is done, 
  // what field/columnis specifically being searched
  const [dropDownValueSearch, setDropDownValueSearch] = useState("Name");
  // These control modal visibility
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  // Holds the keyword input a user inputs for search
  const textInput = useRef("");
  // Passed to modal inputs to display request feedback
  const [errorMes, setErrorMes] = useState("");
  // Keeps track of currently selected rows
  const [selectedRows, setSelectedRows] = useState([]);
  // If user logged in
  const { loggedIn } = props;
  // Holds all data for table, retrieved from gatherWorkspaces 
  const [workspaceData, setWorkspaceData] = useState({
    id: null,
    name: null,
  });

  /**
   * This retrieves all the workspaces a user is part of
   * @returns The formatted data with the id, name and password keys
   */
  async function gatherWorkspaces() {
    // API request to backend
    const response = await fetch("http://127.0.0.1:8000/api/workspaces/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });
    // Await a response and return it if it exists
    // See Views.py for possible errors
    const response_text = await response.json();
    const formattedResponse = response_text.results.map((result) => {
      return {
        id: result.workspace.id,
        name: result.workspace.name,
        password: result.workspace.password,
      };
    });
    if (formattedResponse) {
      setWorkspaceData(formattedResponse);
    }
  }
  // Automatically trigger gathering of workspaces
  // https://dev.to/csituma/why-we-use-empty-array-with-useeffect-iok
  useEffect(() => {
    gatherWorkspaces();
  }, []);

    /**
   * 
   * @param {str} name requested workspace name
   * @param {str} password requested password
   * @returns If the request is successful, true else false
   * Fetch request to trigger the creation of a workspace
   */
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
    // If the request failed, set the error message
    // This message is prop passed to the modals
    // See the backend views.py for the possible error msgs
    const response_text = await response.json();
    if (!response.ok) {
      setErrorMes(response_text);
      return false;
    } else {
      setErrorMes("");
      return true;
    }
  }
  /**
   * 
   * @param {str} name the name of the workspace 
   * @param {str} password the password of the workspace
   * @returns true if successful, false if not
   * Triggers a request to join the backend
   */
  async function triggerJoin(name, password) {
    let data = {
      name: name,
      password: password,
    };

    const response = await fetch("http://127.0.0.1:8000/api/workspaces/join/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });
    // See Views.py for possible error messages
    // Communicating error msgs to props
    const response_text = await response.json();
    if (!response.ok) {
      setErrorMes(response_text);
      return false;
    } else {
      setErrorMes("");
      return true;
    }
  }

    /**
   * With the currently selected workspaces held in selected rows, delete them.
   * TODO: Convert this to hiding versus deleting.
   */
  async function handleDeleteWorkspace() {
    for (let i = 0; i < selectedRows.length; i++) {
      let data = {
        name: selectedRows[i].name,
        password: selectedRows[i].password,
      };
      const response = await fetch("http://127.0.0.1:8000/api/workspaces/", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
        body: JSON.stringify(data),
      });

      const response_text = await response.json();
    }
    setSelectedRows([]);
    gatherWorkspaces();
  }


  const handleExitCreateModal = () => {
    setErrorMes("");
    setShowCreateModal(false);
  };
  const handleExitJoinModal = () => {
    setErrorMes("");
    setShowJoinModal(false);
  };

  // Puts UI filter into Datagrid friendly package
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

  // Whenever user types something into keyword box, update it.
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
          <Col sm={6}>
            <Button
              className="float-start me-2"
              variant="danger"
              onClick={handleDeleteWorkspace}
            >
              Delete Workspace
            </Button>
          </Col>
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
            updateSelection={setSelectedRows}
          />
        </Row>
        <Row className="mt-4">
          <Col />
          <Col>
            <Button onClick={() => setShowJoinModal(true)}>Join Existing Workspace</Button>
          </Col>
          <Col>
            <Button onClick={() => setShowCreateModal(true)}>Create New Workspace</Button>
          </Col>
          <Col />
        </Row>
        <WorkspaceCreateModal
          showModal={showCreateModal}
          handleExitCreateModal={handleExitCreateModal}
          triggerCreation={triggerCreation}
          errorMes={errorMes}
        />
        <WorkspaceJoinModal
          showModal={showJoinModal}
          handleExitJoinModal={handleExitJoinModal}
          triggerJoin={triggerJoin}
          errorMes={errorMes}
        />
      </Container>
    );
  }
};
export default Workspaces;