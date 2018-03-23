import React, { Component } from 'react';
import { Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn,} from 'material-ui/Table';
import Paper from 'material-ui/Paper';

class Scoreboard extends Component {
  render(){
    return(
      <Paper className="scoreboard">
        <Table selectable={false}>
          <TableHeader displaySelectAll={false} adjustForCheckbox={false}>
            <TableRow>
              <TableHeaderColumn>Class</TableHeaderColumn>
              <TableHeaderColumn>Confidence</TableHeaderColumn>
            </TableRow>
          </TableHeader>
          <TableBody displayRowCheckbox={false}>
            {
              this.props.results.map((result, i) =>(
                <TableRow key={i}>
                  <TableRowColumn>{result.name}</TableRowColumn>
                  <TableRowColumn>{result.value}</TableRowColumn>
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
