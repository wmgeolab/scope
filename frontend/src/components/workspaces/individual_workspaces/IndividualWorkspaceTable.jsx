import React, { useState } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container, Button, Modal, Box } from "@mui/material";
import { API } from "../../../api/api";


export default function IndividualWorkspaceTable({data, filt, workspace_id}){

    const [open, setOpen] = useState(false);
    const [selectedSource, setSelectedSource] = useState(null);
    const [selectedResponses, setSelectedResponses] = useState([])
    const [selectedQuestions, setSelectedQuestions] = useState([])
    //const [test, setTest] = useState([])

    const handleOpen = async (source) => {
      setSelectedSource(source);
      const responses = await obtainResponses(source.id);
      setSelectedResponses(responses); // Store responses in state
      const questions = await obtainQuestions(workspace_id);
      setSelectedQuestions(questions);

      //const test = workspace_id;
      //setTest(test);

      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
      setSelectedSource(null);
      setSelectedResponses([]);
    };

    // Copied from IndividualWorkspacePage.jsx
    // Probably not a good idea to have repeated code that may need to be changed
    async function obtainQuestions() {
        const param = new URLSearchParams({
          workspace: workspace_id
        })
    
        let allResults = [];
        let nextUrl = API.url(`/api/questions/?${param}`);
    
        while(nextUrl) {
          // hacky way to fix the nextUrl to use HTTPS as opposed to HTTP which is automatically included by django
          let fixedUrl = nextUrl.startsWith("http://") ? nextUrl.replace("http://", "https://") : nextUrl;
    
          console.log("nextUrl value: ", fixedUrl);
          // const response = await fetch(nextUrl, {
          //   method: "GET",
          //   headers: {
          //     "Content-Type": "application/json",
          //     Authorization: "Token " + localStorage.getItem("user"),
          //   },
          // });
          const response = await fetch(fixedUrl, {
            method: "GET",
            headers: API.getAuthHeaders(),
          });
    
          const response_text = await response.json();
    
          // JUST FOR TESTING
          console.log("Raw Questions Response: ", response_text);
    
          const formattedResponse = response_text.results.map(result => {
            return {
              id: result.id,
              question: result.question,
            }
          });
    
          allResults = [...allResults, ...formattedResponse];
          nextUrl = response_text.next;
        }
    
        return allResults
    }


    async function obtainResponses(source_id) {
      const param = new URLSearchParams({
        workspace: workspace_id,
        source: source_id
      })

      console.log("Fetching responses with params:", param.toString());

      const response = await fetch(API.url(`/api/ai_responses/?${param}`), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Token " + localStorage.getItem("user"),
        },
      });
  
      const response_text = await response.json();
  
      // JUST FOR TESTING
      console.log("Raw Responses:\n");
      console.log(response_text);
  
      const formattedResponse = response_text.results.map(result => {
        return {
          id: result.id,
          summary: result.summary,
          workspace_id: result.workspace,
          source_id: result.source,
        }
      });
  
      return formattedResponse;
    }

    const columns = [
      { field: "id", headerName: "ID" },

      {
        field: "wsName",
        headerName: "Name",
        flex: 1,
      },

      {
        field: "wsURL",
        headerName: "URL",
        flex: 3,
        renderCell: (cellValue) => {
          return (
            <a href={cellValue.formattedValue}>{cellValue.formattedValue}</a>
          );
        },
      },

      {
        field: "actions",
        headerName: "Actions",
        flex: 1,
        sortable: false,
        filterable: false,
        renderCell: (params) => (
          <Button
              variant="contained"
              color="primary"
              onClick={() => handleOpen(params.row)}
          >
              View Responses
          </Button>
        ),
      },
    ];

    return(
        <Container disableGutters sx={{ height: 400, marginTop: "2%"}}>
            <DataGrid
            rows={data}
            columns={columns}
            pageSize={5}
            rowsPerPageOptions={[5]}
            checkboxSelection
            disableColumnFilter
            disableColumnMenu
            disableDensitySelector
            disableColumnSelector
            disableSelectionOnClick
            experimentalFeatures={{ newEditingApi: true }}
            components={{ Toolbar: GridToolbar }}
            filterModel={{
              items: filt,
            }}
      />

          {/* Modal for Viewing Responses */}
          <Modal open={open} onClose={handleClose}>
            <Box sx={{ padding: 4, backgroundColor: "white", margin: "auto", marginTop: "1%", width: 1000, 
                borderRadius: 2, maxHeight: "80vh", overflow: "auto"}}>
              <h2>Responses for {selectedSource?.wsName}</h2>
              
              {/* TODO - all questions are displayed before all responses and there is no link between question and response */}
              {selectedResponses.length > 0 ? (
                  <ul>
                    <h3>
                      {selectedQuestions.map((quest) => (
                          <li key={quest.id}>{quest.question}</li>
                      ))}
                    </h3>
                      {selectedResponses.map((resp) => (
                          <li key={resp.id}>{resp.summary}</li>
                      ))}
                  </ul>
              ) : (
                  <p>No responses available.</p>
              )}
              <Button variant="contained" onClick={handleClose}>
                Close
              </Button>
              {/* TODO - download button */}
              <Button variant="contained" onClick={handleClose}>
                Download
              </Button>
            </Box>
          </Modal>
        </Container>
    );
}