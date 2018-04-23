import React, { Component } from 'react';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';

class Scoreboard extends Component {
  render(){
    return(
      <Paper className="scoreboard">
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Class</TableCell>
              <TableCell numeric>Confidence</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {
              this.props.results.map((result, i) =>(
                <TableRow key={i}>
                  <TableCell>{result.name}</TableCell>
                  <TableCell>{result.value}</TableCell>
                </TableRow>
              ))
            }
          </TableBody>
        </Table>
      </Paper>
    )
  }
}

export default Scoreboard;
