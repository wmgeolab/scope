import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";
import { Row, Col, Button } from "react-bootstrap";

export default function IndividualWorkspaceTable({ data, filt }) {
  const { workspace_name, workspace_id } = useParams();
  const columns = [
    { field: "id", headerName: "ID", width: 90 },

    {
      field: "wsName",
      headerName: "Name",
      width: 150,
    },

    {
      field: "wsURL",
      headerName: "URL",
      width: 150,
      flex: 1,
      renderCell: (cellValue) => {
        return (
          <a href={cellValue.formattedValue}>{cellValue.formattedValue}</a>
        );
      },
    },
    {
      field: "wsGenerate",
      headerName: "Generate AI Summary",
      width: 100,
      flex: 1,
      renderCell: (params) => {
        return (
          // <Button class="btn btn-primary btn-sm" href="/questions">
          //   Generate
          // </Button>
          <form action={"/questions/" + workspace_name}>
            <button className="wsButton" type="submit">
              Generate
            </button>
          </form>
        );
      },
    },
  ];

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
    </Container>
  );
}
