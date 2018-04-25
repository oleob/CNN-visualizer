import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import { CircularProgress } from 'material-ui/Progress';

import {predict} from '../utilities/apiCalls';
import Scoreboard from './Scoreboard';

const styles={
  imageForm: {
  },
  button: {
    marginTop: 20,
    display: 'inline-block',
    minWidth: 0,
  },
  buttonContainer: {
    display: 'block',
    textAlign: 'center',
  },
  scoreboardContainer: {
    display: 'block',
    textAlign: 'center',
  }
};

class ImageForm extends Component {
  constructor(props) {
    super(props)

    this.state={
      results: [],
      loading: false,
    }

    this.uploadFile = this.uploadFile.bind(this);
  }

  uploadFile(event) {
      let file = event.target.files[0];
      if (file) {
        let data = new FormData();
        data.append('image', file);
        this.setState({
          loading: true,
          results: [],
        });
        predict(data).then((results)=>{
          this.setState({
            results,
            loading: false,
          })
        })
      }
  }

  render() {
    const {classes} = this.props;
    return (
      <div className={classes.imageForm}>
        <input accept="image/*" id="raised-button-file" onChange={this.uploadFile} type="file" style={{"display" : "none"}}/>
        <div className={classes.buttonContainer}>
          <label className={classes.button} htmlFor="raised-button-file">
            {!this.state.loading &&
              <Button variant="raised" component="span" >
                Upload image
              </Button>
            }
            {this.state.loading && <CircularProgress size={68} />}
          </label>
        </div>
        <div className={classes.scoreboardContainer}>
          <Scoreboard results={this.state.results} />
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(ImageForm)
