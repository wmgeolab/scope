import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container, Button } from "@mui/material";
import Snackbar from "@mui/material/Snackbar";

export default function IndividualWorkspaceTable({ data, filt }) {
  const { workspace_name, workspace_id } = useParams();
  const [toastGenerate, setToastGenerate] = React.useState(false);
  const [message, setMessage] = React.useState(
    "Triggering article generation!"
  );

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
      field: "wsGenerate",
      headerName: "Generate AI Summary",
      flex: 1,
      renderCell: (params) => {
        return (
          // <Button class="btn btn-primary btn-sm" href="/questions">
          //   Generate
          // </Button>
          <Button
            variant="contained"
            style={{
              textTransform: "capitalize",
              width: "60%",
              alignContent: "right",
            }}
            onClick={() => handleGenerateBtnClick(params.id)}
          >
            Generate
          </Button>
        );
      },
    },
    {
      field: "wsView",
      headerName: "View AI Summary",
      flex: 1,
      renderCell: (params) => {
        return (
          <Button
            variant="contained"
            style={{
              textTransform: "capitalize",
              width: "60%",
              alignContent: "right",
            }}
            type="submit"
            href={"/questions/" + workspace_name}
          >
            View
          </Button>
        );
      },
    },
  ];

  console.log(data);

  const handleGenerateBtnClick = (article_id) => {
    let article_string =
      "Requesting AI generation for article with ID: " + article_id;
    setMessage(article_string);
    setToastGenerate(true);
  };

  const handleGenerateBtnClose = () => {
    setToastGenerate(false);
  };

  return (
    <Container disableGutters sx={{ height: 400, marginTop: "2%" }}>
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
      <Snackbar
        open={toastGenerate}
        onClose={handleGenerateBtnClose}
        autoHideDuration={3000}
        message={message}
      ></Snackbar>
    </Container>
  );
}
