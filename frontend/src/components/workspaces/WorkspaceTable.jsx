import React, { useState, useEffect } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";

export default function WorkspaceTable(props) {
  const { workspaceData, tagData, columns, filters } = props;

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
