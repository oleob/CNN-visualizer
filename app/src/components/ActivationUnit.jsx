import React from 'react';
import Paper from 'material-ui/Paper';
import { withStyles } from 'material-ui/styles';

const styles = {
  unit: {
    margin: 2,
  },
  image: {
    width: 50,
  },
}

const ActivationUnit = props => {
  const { classes } = props;
  return(
    <Paper className={classes.unit}>
      <img className={classes.image} alt="activation" src={props.image_path}/>

    </Paper>
  )
}

export default withStyles(styles)(ActivationUnit);
