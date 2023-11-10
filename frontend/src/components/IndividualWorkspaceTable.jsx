import React, { useState } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Container } from "@mui/material";
import { Row, Col, Button } from "react-bootstrap";

export default function IndividualWorkspaceTable(props) {
  const { data } = props;

  console.log(data);
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
  ];

  return (
    // Put back in filtmodel
    <Container
      disableGutters
      sx={{
        height: 400,
        marginTop: "2%",
        justifyContent: "left",
        alignSelf: "left",
        alignContent: "left",
      }}
    >
      {data.map((entry) => (
        <Row className="text-start mt-3">
          <Col sm={10}>
            <h6>Source ID: {entry.id}</h6>
            <Row>
              <h4>
                <b>Article Name : {entry.wsName}</b>
              </h4>
            </Row>
            <h6>
              <a href={entry.wsURL}> {entry.wsURL}</a>
            </h6>

            <Row>
              <Col sm={5}>
                <Button variant="outline-danger">Delete</Button>
                <Button variant="outline-primary">Edit</Button>
              </Col>
            </Row>
          </Col>
          {/* <Col>
              {entry.id}
              </Col>
              <Col>
              {entry.wsName}
              </Col>
              <Col>
              {entry.wsURL}
              </Col> */}
        </Row>
      ))}
    </Container>
  );
}
