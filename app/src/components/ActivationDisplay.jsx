import React from 'react';
import ActivationUnit from './ActivationUnit';
import { withStyles } from 'material-ui/styles';
import Paper from 'material-ui/Paper';


const styles = {
  innerContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'flex-start',
  },
  outerContainer: {
    marginTop: 10,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  }
}

const ActvationDisplay = props => {
  const {classes} = props;
  return(
    <div className={classes.outerContainer}>
      {
        props.results.map((result, ind) => (
          <div key={ind}>
            <p>{result.info.name}</p>
            <Paper className={classes.innerContainer}>
            {
              Object.entries(result.images).map((item, index) => (
                <ActivationUnit key={index} name={item[0]} {...item[1]} />
              ))
            }
          </Paper>
          </div>
        ))
      }
    </div>
  )
}

export default withStyles(styles)(ActvationDisplay);
