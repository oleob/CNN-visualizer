import React, { Component } from 'react';
import DeepTaylorUnit from './DeepTaylorUnit';
import { withStyles } from 'material-ui/styles';

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'flex-start',
  }
}

const DeepTaylorDisplay = props => {
  const {classes} = props;
  return(
    <div className={classes.container}>
      {
        Object.entries(props.result).map((item, index) => (
          <DeepTaylorUnit key={index} name={item[0]} {...item[1]} />
        ))
      }
    </div>
  )
}

export default withStyles(styles)(DeepTaylorDisplay);
