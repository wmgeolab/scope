import React, { useState, useRef, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/workspace.css";
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
import UnauthorizedView from "./UnauthorizedView";
import WorkspaceTable from "./WorkspaceTable";
import WorkspaceCreateModal from "./WorkspaceCreateModal";
import WorkspaceJoinModal from "./WorkspaceJoinModal";
import { useNavigate } from "react-router-dom";

const Workspaces = (props) => {
  const [filt, setFilt] = useState([]);
  const [dropDownValue, setValue] = useState("All Workspaces");
  const [dropDownValueSearch, setDropDownValueSearch] = useState("Owner");
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [workspaceName, setWorkspaceName] = useState("");
  const [workspacePassword, setWorkspacePassword] = useState("");
  const [triggerCreateApiCall, setTriggerCreateApiCall] = useState(false);
  const [triggerJoinApiCall, setTriggerJoinApiCall] = useState(false);
  const textInput = useRef("");
  const navigate = useNavigate();

  const { loggedIn } = props;

  var data = {
    name: workspaceName,
    password: workspacePassword
  }
  console.log(data)

  useEffect(() => {
    // CREATE API CALL HERE
    // TODO: fix this
    if(triggerCreateApiCall) {
      fetch("http://127.0.0.1:8000/api/workspaces/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
        body: JSON.stringify(data),
      }).then(
        (result)=>console.log(result)
      );
      navigate("/workspaces/");
      // setTriggerCreateApiCall(false);
    }
    // return () => {}
  }, [triggerCreateApiCall]);

  useEffect(() => {
    // JOIN API CALL HERE.
    // TODO: fix this too
    if(triggerJoinApiCall) {
      fetch("http://127.0.0.1:8000/api/workspaces/join/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
        body: JSON.stringify(data),
      }).then(
        (result)=>console.log(result)
      );
      navigate("/workspaces/");
      // setTriggerJoinApiCall(false);
    }
    // return () => {}
  }, [triggerJoinApiCall]);
  const handleShowJoin = () => {
    setShowJoinModal(true);
  };
  const handleShowCreate = () => {
    setShowCreateModal(true);
  };
  const handleExitCreateModal = () => {
    setShowCreateModal(false);
  };
  const handleExitJoinModal = () => {
    setShowJoinModal(false);
  };

  const onSubmitSearch = () => {
    setFilt([
      {
        columnField: "owner",
        operatorValue: "contains",
        value: textInput.current,
      },
    ]);
  };

  const handleKeywordChange = (value) => {
    textInput.current = value.target.value;
    let tempValue = dropDownValueSearch.toLowerCase();
  };

  const fake_data = [
    {
      id: 0,
      owner: "user1",
      name: "My Workspace 1",
      tags: "Argentina",
    },
    {
      id: 1,
      owner: "user2",
      name: "My Workspace 2",
    },
    {
      id: 2,
      owner: "user3",
      name: "My Workspace 3",
      tags: "Ohio, Train",
    },
    {
      id: 3,
      owner: "user4",
      name: "My Workspace 4",
      tags: "Ukraine",
    },
  ];

  //TODO: Look into moving this into its own Component...
  const workspaceColumns = [
    { field: "id", headerName: "ID", width: 90 },
    { field: "owner", headerName: "Owner", width: 150 },
    {
      field: "name",
      headerName: "Name",
      width: 250,

      renderCell: (cellValue) => {
        return (
          <a href={"/workspace/" + cellValue.formattedValue}>
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
                placeholder="add Tags"
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
          <Col sm={4}>
            <DropdownButton
              id="dropdown-basic-button"
              title={dropDownValue}
              style={{ float: "left", marginLeft: "0px" }}
            >
              <Dropdown.Item onClick={(e) => setValue(e.target.text)}>
                Workspaces Owned by Me
              </Dropdown.Item>
              <Dropdown.Item onClick={(e) => setValue(e.target.text)}>
                Workspaces Not Owned by Me
              </Dropdown.Item>
              <Dropdown.Item onClick={(e) => setValue(e.target.text)}>
                All Workspaces
              </Dropdown.Item>
            </DropdownButton>
          </Col>
          <Col sm={2} />
          <Col sm={1}>
            <DropdownButton
              id="dropdown-basic-button"
              title={dropDownValueSearch}
              style={{ float: "right", marginLeft: "10px" }}
            >
              <Dropdown.Item
                onClick={(e) => setDropDownValueSearch(e.target.text)}
              >
                Owner
              </Dropdown.Item>
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
                    class="bi bi-search"
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
            data={fake_data}
            columns={workspaceColumns}
            filters={filt}
          />
          <Row>
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
          setWorkspaceName={setWorkspaceName}
          setWorkspacePassword={setWorkspacePassword}
          handleExitCreateModal={handleExitCreateModal}
          setTriggerCreateApiCall={setTriggerCreateApiCall}
        />
        <WorkspaceJoinModal
          showModal={showJoinModal}
          setWorkspaceName={setWorkspaceName}
          setWorkspacePassword={setWorkspacePassword}
          handleExitJoinModal={handleExitJoinModal}
          setTriggerJoinApiCall={setTriggerCreateApiCall}
        />
      </Container>
    );
  }
};
export default Workspaces;
