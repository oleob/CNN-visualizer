import React, { Component } from 'react';
import Button from 'material-ui/Button';
import { FormControl, FormControlLabel } from 'material-ui/Form';
import Paper from 'material-ui/Paper';
import Checkbox from 'material-ui/Checkbox';
import Input from 'material-ui/Input';
import TextField from 'material-ui/TextField';

import { postRequest } from '../utilities/apiCalls';
import {withStyles} from "material-ui/styles/index";


const styles = {
  mainSpan: {
    display: 'inline-block'
  },
  paperSettings: {
    display: 'inline-block',
    margin: 40,
    padding: 20,
    width: 550
  },

  paperImage: {
    display: 'inline-block',
    position: 'absolute',
    top: 105,
    padding: 20,
  },

  featureImage: {
    position: 'relative'
  },

  layerInput: {
    width: 400,
    marginRight: 30
  },
  paramInput: {
    marginTop: 10,
    marginRight: 20,
    width: 60

  },
  visButton: {

  },

};


class FeatureVis extends Component {
  constructor(props) {
    super(props);
    this.state = {
      img_paths: [],
      layer_name: 'InceptionV1/InceptionV1/Mixed_4c/concat:0',
      channel: 97,
      steps: 200,
      dim: 128,
      pad: 16,
      jitter: 8,
      rotation: 5,
      scale: 0.2
    };
  }

  handleInputChange = (event) => {
    const target = event.target;
    const name = event.target.name;
    const value = target.value;
    this.setState({
      [name]: value
    });
  };

  visualizeFeature = (event) => {

    const api_key = 'dc6zaTOxFJmzC';
    const url = `http://api.giphy.com/v1/gifs/search?q=${'cat'}&api_key=${api_key}`;
    let cat_index = Math.floor(Math.random() * 24);
    fetch(url)
      .then(response => response.json())
      .then(data => this.setState({ img_paths: [data.data[cat_index].images.fixed_height.url] }));

    const body = {
      layer_name: this.state.layer_name,
      channel: this.state.channel,
      steps: this.state.steps,
      dim: this.state.dim,
      pad: this.state.pad,
      jitter: this.state.jitter,
      rotation: this.state.rotation
    };

    postRequest('/visualize', body).then((res) => {
      console.log(res);
      this.setState({
        img_paths: res.filepaths
      })
    })
  };




  render() {
    const { classes } = this.props;
    return (
      <span className={classes.mainSpan}>
        <Paper className={classes.paperSettings}>
          <form>
            <FormControl>
              <h2>Feature Inversion</h2>
              <span>
                <TextField className={classes.layerInput} label="Layer Name:" name="layer_name" value={this.state.layer_name} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Channel:" name="channel" value={this.state.channel} onChange={this.handleInputChange} />
              </span>
              <span>
                <TextField className={classes.paramInput} label="Steps:" name="steps" value={this.state.steps} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Size:" name="dim" value={this.state.dim} onChange={this.handleInputChange} />
              </span>
              <span>
                <TextField className={classes.paramInput} label="Padding:" name="pad" value={this.state.pad} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Jitter:" name="jitter" value={this.state.jitter} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Rotation:" name="rotation" value={this.state.rotation} onChange={this.handleInputChange}/>
                <TextField className={classes.paramInput} label="Scale:" name="scale" value={this.state.scale} onChange={this.handleInputChange}/>
                <FormControlLabel control={<Checkbox/>} label="naive"/>
              </span>
            </FormControl>
          </form>
          <Button variant="raised" className={classes.visButton} onClick={this.visualizeFeature}>Visualize !</Button>
        </Paper>
        <Paper className={classes.paperImage}>
          <img className={classes.featureImage} src={this.state.img} alt={this.state.term} />
          {this.state.img_paths.map((filepath, index)=>(
              <img key={index} alt={this.state.layer} src={filepath} />
          ))}
        </Paper>
      </span>
    );
  }
}

export default withStyles(styles)(FeatureVis);
