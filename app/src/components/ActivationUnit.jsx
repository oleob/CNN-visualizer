import React from 'react';
import Paper from 'material-ui/Paper';
import { withStyles } from 'material-ui/styles';

const styles = {
  unit: {
    margin: 10,
  },
  image: {
    width: 200,
  },
}

const ActivationUnit = props => {
  const { classes } = props;
  return(
    <Paper className={classes.unit}>
      <img className={classes.image} alt="activation" src={props.image_path}/>
      <p>Filter ID: {props.name}</p>
    </Paper>
  )
}

export default withStyles(styles)(ActivationUnit);
