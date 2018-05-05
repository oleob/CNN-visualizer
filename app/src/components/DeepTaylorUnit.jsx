import React, { Component } from 'react';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Typography from 'material-ui/Typography'
import Card, { CardActions, CardContent, CardMedia } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import Collapse from 'material-ui/transitions/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
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
        <Typography gutterBottom variant="headline" component="h2">
          name here
        </Typography>
        <Typography component="p">
          {this.props.name}
        </Typography>
      </CardContent>
      <CardActions>
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
