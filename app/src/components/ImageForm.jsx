import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import { CircularProgress } from 'material-ui/Progress';

import {getRequest, postRequest} from '../utilities/apiCalls';
import Scoreboard from './Scoreboard';

const styles={
  imageForm: {
    marginTop: 20,
    overflow:'hidden',
  },
  button: {
    marginTop: 5,
    marginBottom: 5,
    display: 'inline-block',
    minWidth: 0,
  },
  buttonContainer: {
    display: 'block',
    textAlign: 'center',
  },
  scoreboardContainer: {
    marginTop: 5,
    display: 'block',
    textAlign: 'center',
  },
  previewImage: {
    maxHeight: 400,
    maxWidth: 400,
  },
};

class ImageForm extends Component {

  state={
    results: [],
    loading: false,
  }

  componentDidMount() {
    this.setState(this.props.localState)
  }

  componentWillUnmount() {
    this.props.updateState(this.state)
  }

  uploadFile = event => {
      let file = event.target.files[0];
      if (file) {
        let data = new FormData();
        data.append('image', file);
        this.setState({
          loading: true,
          results: [],
        });
        postRequest('/upload_image', data).then((res) => {
          if (res.status==='ok'){
            this.setState({
              loading: false,
            });
            this.props.updateGlobalState({imagePath: res.image_path})
          }
        });
      }
  }

  predict = () => {
    this.setState({loading: true})
    getRequest('predict').then((results) => {
      this.setState({
        results,
        loading: false,
      });
    });
  }

  render() {
    console.log(this.props)
    const {classes} = this.props;
    return (
      <div className={classes.imageForm}>
        {(this.props.globalState.imagePath !== '') &&
          <div className={classes.buttonContainer}>
            <img className={classes.previewImage} src={this.props.globalState.imagePath}/>
          </div>
        }
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
          <div className={classes.buttonContainer}>
            {!this.state.loading &&
              <Button className={classes.button} variant="raised"  onClick={this.predict} >
                Predict
              </Button>
            }
          </div>
        </div>
        <div className={classes.scoreboardContainer}>
          <Scoreboard results={this.state.results} />
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(ImageForm)
