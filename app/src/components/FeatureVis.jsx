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
  paper: {
    display: 'inline-block',
    padding: 20,
  },
  formControl:{
    minWidth: 300
  },
  img: {
    hspace: "10px",
    vspace:"10px"
  },
  input: {
    width: "500px"
  },
  Button: {
    padding: "15px"
  }

};


class FeatureVis extends Component {
  constructor(props) {
    super(props);
    this.state = {
      img_paths: [],
      layer_name: 'InceptionV1/InceptionV1/Mixed_4c/concat:0',
      channel: 58,
      steps: 200,
      dim: 128,
      pad: 16,
      jitter: 8,
      rotation: 5
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
    return (
      <div>
        <Paper>
          <form>
            <FormControl>
              <TextField label="Layer Name:" name="layer_name" value={this.state.layer_name} onChange={this.handleInputChange} />
              <TextField label="Channel:" name="channel" value={this.state.channel} onChange={this.handleInputChange} />
              <TextField label="Steps:" name="steps" value={this.state.steps} onChange={this.handleInputChange} />
              <TextField label="Size(px):" name="dim" value={this.state.dim} onChange={this.handleInputChange} />
              <h4>Transforms:</h4>
              <TextField label="Padding:" name="pad" value={this.state.pad} onChange={this.handleInputChange} />
              <TextField label="Jitter:" name="jitter" value={this.state.jitter} onChange={this.handleInputChange} />
              <TextField label="Rotation (0 - 180):" name="rotation" value={this.state.rotation} onChange={this.handleInputChange}/>
              <FormControlLabel control={<Checkbox/>} label="scale"/>
              <FormControlLabel control={<Checkbox/>} label="naive"/>
            </FormControl>
          </form>
          <br/>
          <Button onClick={this.visualizeFeature}>Visualize!</Button>
        </Paper>
          <img src={this.state.img} alt={this.state.term} />
          {this.state.img_paths.map((filepath, index)=>(
              <img key={index} alt={this.state.layer} src={filepath} />
          ))}
      </div>
    );
  }
}

export default withStyles(styles)(FeatureVis);
