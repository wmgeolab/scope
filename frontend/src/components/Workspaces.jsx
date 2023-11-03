import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Row, Col } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/css/workspace.css";
import { DataGrid } from "@mui/x-data-grid";
import { Container, Box } from "@mui/material";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Form from "react-bootstrap/Form";
import { Button } from "react-bootstrap";
import InputGroup from "react-bootstrap/InputGroup";
import { Search } from "react-bootstrap-icons";
import { GridToolbar } from "@mui/x-data-grid";
import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import Modal from "react-bootstrap/Modal";
import UnauthorizedView from "./UnauthorizedView";
import WorkspaceTable from "./WorkspaceTable";
import WorkspaceCreateModal from "./WorkspaceCreateModal";
import WorkspaceJoinModal from "./WorkspaceJoinModal";
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

  const { loggedIn } = props;

  useEffect(() => {
    // CREATION API CALL HERE.
    // May need to use axios? 
    console.log("TO DO: IMPLEMENT API CALL TO CREATE WORKSPACE HERE.");
  }, [triggerCreateApiCall]);

  useEffect(() => {
    // JOIN API CALL HERE.
    console.log("TO DO: IMPLEMENT API CALL TO JOIN WORKSPACE HERE!");
  }, [triggerJoinApiCall]);
  const handleShowJoin = () => {
    setShowJoinModal(true);
  }
  const handleShowCreate = () => {
    setShowCreateModal(true);
  }
  const handleExitCreateModal = () => {
    setShowCreateModal(false);
  }
  const handleExitJoinModal = () => {
    setShowJoinModal(false);
  }





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
    textInput.current = value;
    let tempValue = dropDownValueSearch.toLowerCase();
    setFilt([
      {
        columnField: tempValue,
        operatorValue: "contains",
        value: textInput.current,
      },
    ]);
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
        console.log(tag_list.formattedValue);
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
          <Col sm={5}>
            <Form onSubmit={onSubmitSearch}>
              <InputGroup>
                <InputGroup.Text>
                  <Search />
                </InputGroup.Text>
                <Form.Control
                  placeholder={"Search by Workspace " + dropDownValueSearch}
                  onChange={(value) => handleKeywordChange(value.target.value)}
                  type="text"
                />
              </InputGroup>
            </Form>
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
