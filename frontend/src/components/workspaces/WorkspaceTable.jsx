import React, { useState, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";

export default function WorkspaceTable(props) {
  const { data, columns, filters, updateSelection} = props;
  
  const [tempFilters, setTempFilters] = useState(filters);

  useEffect(() => {
    setTempFilters(filters);
  }, [filters]);
  
  function handleData(data){
    if (Object.is( data.id, null )){
        return [];
    } else {
      return data;
    }
  } 


  function handleRowSelect(selected_row_ids){
    updateSelection(data.filter(obj => selected_row_ids.includes(obj.id)));
  }

  return (
    <Container disableGutters sx={{ height: 400, marginTop: "2%" }}>
      <DataGrid
        rows={handleData(data)}
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
        onSelectionModelChange={handleRowSelect}
        experimentalFeatures={{ newEditingApi: true }}
        components={{ Toolbar: GridToolbar }}
        filterModel={{
          items: tempFilters,
        }}
      />
    </Container>
  );
}
