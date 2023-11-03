import React, { useState, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from '@mui/material';
import { Button } from "react-bootstrap";

export default function WorkspaceTable(props) {
  const { data, columns, filters } = props;

  const [tempFilters, setTempFilters] = useState(filters);

  console.log(filters);
  useEffect(() => {
    setTempFilters(filters);
  }, [filters]);
  return (
    
  
    <Container disableGutters sx={{ height: 400, marginTop: "2%"}}>
        <DataGrid
          rows={data}
          columns={columns}
          rowsPerPageOptions={[5]}
          checkboxSelection
          disableColumnFilter
          disableColumnMenu
          disableDensitySelector
          disableColumnSelector
          disableSelectionOnClick
          hideFooterPagination
          hideFooterSelectedRowCount
          experimentalFeatures={{ newEditingApi: true }}
          components={{ Toolbar: GridToolbar }}
          filterModel={{
            items: tempFilters,
          }}
        />
    </Container>
  );
}
