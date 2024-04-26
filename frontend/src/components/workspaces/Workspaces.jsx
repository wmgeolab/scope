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
  const [tagData, setTagData] = useState({
    id: null,
    name: null,
  });

  // an array of objects to either be deleted or added
  const [saveData, setSaveData] = useState([]);

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

  async function deleteTag(id, tag) {
    let data = {
      workspace: id,
      tag: tag,
    };
    console.log(data, 'this is data');
    const response = await fetch("http://127.0.0.1:8000/api/tags/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });

    const response_text = await response.json();
    console.log(response_text);
    if (response_text.error) {
      setErrorMes(response_text.error);
    } else {
      setError(false);
    }
  }
  /**
   * This retrieves all the tags for each of the user's workspaces
   * @returns A JSON object with all the tags and their corresponding workspace ids
   */
  async function getTags() {
    // API request to backend
    const response = await fetch("http://127.0.0.1:8000/api/tags/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
    });
    // Await a response and return it if it exists
    // See Views.py for possible errors
    const response_text = await response.json();

    console.log("responseTets:", response_text);
    try {
      // gathering all the tags for each workspace by id
      const formattedResponse = response_text.results.reduce(
        (accumulator, result) => {
          const existingEntry = accumulator.find(
            (entry) => entry.id === result.workspace
          );

          if (existingEntry) {
            // If an entry with the same ID already exists, merge the tags
            existingEntry.tags.push(result.tag);
          } else {
            // If no entry with the same ID exists, create a new entry
            accumulator.push({
              id: result.workspace,
              tags: [result.tag],
            });
          }

          return accumulator;
        },
        []
      );
      if (formattedResponse) {
        setTagData(formattedResponse);
      }
    } catch (e) {
      console.log(e);
    }
  }

  /**
   * This sends tags to the backend for storage when created by a user
   * @returns any errors that occur with posting tags
   */
  async function sendTag(id, tag) {
    let data = {
      workspace: id,
      tag: tag,
    };
    // API request to backend
    const response = await fetch("http://127.0.0.1:8000/api/tags/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Token " + localStorage.getItem("user"),
      },
      body: JSON.stringify(data),
    });
    // Await a response and return it if it exists
    // See Views.py for possible errors
    const response_text = await response.json();
    console.log("sedning tag...");

    if (response_text.error) {
      console.log("error message with tags", response_text);
    }
  }

  useEffect(() => {
    gatherWorkspaces();
    getTags();
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

  // function to add and delete tags from the list
  const handleSaveTags = () => {
    if (saveData.length > 0) {
      saveData.forEach((cur) => {
        if (cur.method === "add") {
          sendTag(cur.id, cur.name); // might come across an issue adding multiple tags
        } else {
           deleteTag(cur.id, cur.name);
        }
      });
      setSaveData([]);
    }
  };

  const handleDeleteTags = (e, workspace_id, tag_name) => {
  
    let delete_item = {
      id: workspace_id,
      name: tag_name,
      method: "delete", // delete the tag
    };
    setSaveData((previous) => [...previous, delete_item]);
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
        // console.log("tag List", tag_list);
        // console.log("formattedValue", tag_list.formattedValue);
        var tags_to_display;
        if (
          tag_list.formattedValue === null ||
          tag_list.formattedValue === undefined
        ) {
          tags_to_display = [];
        } else {
          tags_to_display = tag_list.formattedValue;
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
                {...getTagProps({ index })}
                onMouseDown={(e) => handleDeleteTags(e, tag_list.id, option)}
                label={option}
                color="primary"
                />
              ))
            }
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                label=""
                placeholder="Add tags"
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    if (event.target.value !== "") {
                      // the new tag to be added
                      let adding = {
                        id: tag_list.id,
                        name: event.target.value,
                        method: "add", //if the tag is being added or deleted
                      };
                      setSaveData((previous) => [...previous, adding]);
                    }
                  }
                }}
                //put send tag here and it will add every letter
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
            workspaceData={workspaceData}
            tagData={tagData}
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
            <Col>
              <Button onClick={handleSaveTags}>Save Tags</Button>
            </Col>
            {/* <Col>
              <Button onClick={sendTag(55, "yellow")}>Save Tags</Button>
            </Col> */}
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
