import React, { Component } from 'react';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Typography from 'material-ui/Typography'
import Card, { CardActions, CardContent, CardMedia } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import Collapse from 'material-ui/transitions/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ContentCopy from '@material-ui/icons/ContentCopy';
import IconButton from 'material-ui/IconButton';
import classnames from 'classnames';

const styles = theme => ({
  card: {
    width: 200,
    margin: 10,
  },
  media: {
    height: 0,
    paddingTop: '100%',
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
});

class DeepTaylorUnit extends Component {
  state = { expanded: false };

  handleExpandClick = () => {
    this.setState({ expanded: !this.state.expanded });
  };

  copyIds = () => {
    const ids = [];
    this.props.filter_rankings.map((filter)=>{
      ids.push(filter.id)
    })

  const dummy = document.createElement("input");
  document.body.appendChild(dummy);
  dummy.setAttribute("id", "dummy_id");
  document.getElementById("dummy_id").value = ids.toString();
  dummy.select();
  document.execCommand("copy");
  document.body.removeChild(dummy);
}

  render() {
    const {classes} = this.props;
    return(
    <Card className={classes.card}>
      <CardMedia
        className={classes.media}
        image={this.props.image_path}
        title="relevance"
      />
      <CardContent>
        <Typography component="p">
          {this.props.name}
        </Typography>
      </CardContent>
      <CardActions>
        <IconButton aria-label="Copy Filter IDs" onClick={this.copyIds} variant="raised">
          <ContentCopy />
        </IconButton>
        <IconButton
          className={classnames(classes.expand, {
            [classes.expandOpen]: this.state.expanded,
          })}
          onClick={this.handleExpandClick}
          aria-expanded={this.state.expanded}
          aria-label="Show more"
        >
          <ExpandMoreIcon />
      </IconButton>
      </CardActions>
      <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell numeric>Id</TableCell>
              <TableCell numeric>Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {
              this.props.filter_rankings.map((filter) =>(
                <TableRow key={filter.id}>
                  <TableCell>{filter.id}</TableCell>
                  <TableCell>{Math.round(filter.score * 1000) / 1000}</TableCell>
                </TableRow>
              ))
            }
          </TableBody>
        </Table>
      </Collapse>
    </Card>
    );
  }
}

export default withStyles(styles)(DeepTaylorUnit);
