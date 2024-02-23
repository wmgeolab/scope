import React, { useState } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container, Button } from "@mui/material";
import { Row, Col } from "react-bootstrap";


export default function IndividualWorkspaceTable({data, filt}){
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
            return <a href={cellValue.formattedValue}>{cellValue.formattedValue}</a>;
          },
        },
        {field: "wsGenerate",
        headerName: "Generate AI Summary",
        width:100,
        flex:1,
        renderCell: (params) => {
          return (
            <Button variant="contained">Generate</Button>
          )
        },
      }
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
        </Container>
    );


}