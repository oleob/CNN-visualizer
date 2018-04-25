import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';

const styles = {
  scoreboard: {
    width: 500,
    display: 'inline-block',
  }
}

class Scoreboard extends Component {
  render(){
    const {classes} = this.props;

    return(
      <Paper className={classes.scoreboard}>
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

export default withStyles(styles)(Scoreboard);
