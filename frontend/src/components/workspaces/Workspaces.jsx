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
import { TailSpin } from "react-loader-spinner";
import Box from "@mui/material/Box";
import { Search } from "react-bootstrap-icons";
import { API } from "../../api/api";

const Workspaces = (props) => {
  const [filt, setFilt] = useState([]);
  const [dropDownValueSearch, setDropDownValueSearch] = useState("Name");
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const textInput = useRef("");
  const [errorMes, setErrorMes] = useState("");
  const [error, setError] = useState(true);
  const [loading, setLoading] = useState(true); // State to track loading status

  const { loggedIn } = props;
  const [workspaceData, setWorkspaceData] = useState({
    id: null,
    name: null,
  });

  async function gatherWorkspaces() {
    setLoading(true); // Set loading to true when fetching data
    const response = await fetch(API.url('/api/workspaces/'), {
      method: "GET",
      headers: API.getAuthHeaders(),
    });
    const response_text = await response.json();

    // JUST FOR TEXTING
    console.log("Raw Workspaces Response:\n");
    console.log(response_text);

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
      setLoading(false); // Set loading to false after data is fetched
    } catch (e) {
      console.log(e);
      setLoading(false); // Set loading to false if there's an error
    }
  }

  useEffect(() => {
    gatherWorkspaces();
  }, []);

  async function triggerCreation(name, password) {
    setLoading(true); // Set loading to true when triggering creation
    let data = {
      name: name,
      password: password,
    };

    const response = await fetch(API.url('/api/workspaces/'), {
      method: "POST",
      headers: API.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    const response_text = await response.json();
    if (response_text.error) {
      setErrorMes(response_text.error);
    } else setError(false);
    setLoading(false); // Set loading to false after creation is triggered
  }

  async function triggerJoin(name, password) {
    setLoading(true); // Set loading to true when triggering join
    let data = {
      name: name,
      password: password,
    };
    console.log(JSON.stringify(data), "in join");
    const response = await fetch(API.url('/api/workspaces/join/'), {
      method: "POST",
      headers: API.getAuthHeaders(),
      body: JSON.stringify(data),
    });
    const response_text = await response.json();
    console.log(response_text);
    if (response_text.error) {
      setErrorMes(response_text.error);
    } else setError(false);
    setLoading(false); // Set loading to false after join is triggered
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
      <div>
        <title>SCOPE</title>
        <meta charSet="utf-8" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, user-scalable=no"
        />
        <Container>
          <div className="customRowContainer">
              <h2 style={{ paddingTop: "2%", paddingBottom: "2%", fontWeight: "bold " }}>Workspaces</h2>
          </div>
          <Row>
            <div className="customRowContainer">
                
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
                
                <div className= "workspaceSearch">
                  <Form onSubmit={onSubmitSearch}>
                    <InputGroup>
                      {/* <Button aria-label="Search" onClick={onSubmitSearch}> */}
                        <InputGroup.Text>
                            <Search
                            className="search-bar">
                            </Search>
                        </InputGroup.Text>
                      <Form.Control
                        placeholder={"Search by Workspace " + dropDownValueSearch}
                        ref={textInput}
                        onChange={(value) => handleKeywordChange(value)}
                        type="text"
                      />
                    </InputGroup>
                  </Form>
                </div>
              </div>
            
          </Row>     

               


          <Row>           
            <Col>
              {/* Conditionally render loading spinner */}
            <Box sx={{ height: 400, width: "100%" }}>
              {loading ? (
                <div className="loader-container d-flex justify-content-center align--center"> {/* Center the loader vertically and horizontally */}
                  <TailSpin
                    
                    color="#00BFFF"
                    height={100}
                    width={100}
                  />
                  
                </div>
              ) : (
                // Render workspace table when loading is complete
                <WorkspaceTable
                  data={workspaceData}
                  columns={workspaceColumns}
                  filters={filt}
                />
              )}
            </Box>
            </Col>
          </Row>


          <div className="workspaceButtons">
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
          </div>
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
      </div>
    );
  }
};
export default Workspaces;
