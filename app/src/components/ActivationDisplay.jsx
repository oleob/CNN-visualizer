import React from 'react';
import ActivationUnit from './ActivationUnit';
import { withStyles } from 'material-ui/styles';

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'flex-start',
  }
}

const ActvationDisplay = props => {
  const {classes} = props;
  return(
    <div className={classes.container}>
      {
        Object.entries(props.result).map((item, index) => (
          <ActivationUnit key={index} name={item[0]} {...item[1]} />
        ))
      }
    </div>
  )
}

export default withStyles(styles)(ActvationDisplay);
