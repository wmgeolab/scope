import React, { useState, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";

export default function WorkspaceTable(props) {
  const { workspaceData, tagData, columns, filters, updateSelection} = props;

  const [tempFilters, setTempFilters] = useState(filters);
  const [data, setData] = useState(workspaceData);

  useEffect(() => {
    setTempFilters(filters);
  }, [filters]);
  
  useEffect(() => {
    mergeData();
  }, [workspaceData]);

  // merging the data for the workspaces and the corresponding tags
  const mergeData = () => {
    console.log("workspace data", workspaceData);
    if (Object.values(workspaceData)[0] != null) {
      let newData = workspaceData.map((t1) => ({
        ...t1,
        ...tagData.find((t2) => t2.id === t1.id),
      }));
      setData(newData);
    }
  };

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
