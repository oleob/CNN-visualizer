import React, { Component } from 'react';
import Button from 'material-ui/Button';
import { FormLabel, FormControl, FormControlLabel } from 'material-ui/Form';
import Paper from 'material-ui/Paper';
import Checkbox from 'material-ui/Checkbox';
import Radio, { RadioGroup } from 'material-ui/Radio';
import TextField from 'material-ui/TextField';
import { MenuItem } from 'material-ui/Menu';
import Select from 'material-ui/Select';
import { InputLabel } from 'material-ui/Input';

import {getRequest, postRequest} from '../utilities/apiCalls';
import {withStyles} from "material-ui/styles/index";


const styles = {
  mainSpan: {
    display: 'flex',
    alignItems: 'flex-start'
  },
  paperSettings: {
    display: 'inline-block',
    margin: 40,
    padding: 20,
    width: 550
  },

  paperImage: {
    marginTop:40,
    marginBottom: 40,
    padding: 20
  },

  featureImage: {
    position: 'relative'
  },

  layerInput: {
    width: 300,
    marginRight: 30
  },
  paramInput: {
    marginTop: 10,
    marginRight: 20,
    width: 60

  },
  visButton: {
    marginTop: 10,
    marginRight: 20,
  },

  addButton: {
    width: 30
  },

};


class FeatureVis extends Component {
  constructor(props) {
    super(props);
    this.state = {
      img_paths: [],
      layer_name: 'InceptionV1/InceptionV1/Mixed_4c/concat:0',
      channel: 134,
      steps: 200,
      lr: 0.06,
      dim: 128,
      pad: 16,
      jitter: 8,
      rotation: 5,
      scale: 0.2,

      param_space: 'fourier',

      mix: false,

      loading: false,
      loading_imagenet: false,

      all_layers: [],

      imagenet_paths: [],
    };
    this.mixFeature = this.mixFeature.bind(this);
  }

  componentDidMount() {
    this.setState(this.props.localState)
    getRequest('/layer_names').then((res) => {
      this.setState({
        all_layers: res.names,
      });
    })
  }

  componentWillUnmount() {
    this.props.updateState(this.state)
  }

  handleInputChange = (event) => {
    const target = event.target;
    const name = event.target.name;
    const value = target.value;
    this.setState({
      [name]: value
    });

    if (value === 'naive') {
      this.setState({lr: 3.0})
    } else if (value === 'fourier') {
      this.setState({lr: 0.06})
    }
  };

  visualizeFeature = (event) => {

    this.setState({loading: true});

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
      lr: this.state.lr,
      dim: this.state.dim,
      pad: this.state.pad,
      jitter: this.state.jitter,
      rotation: this.state.rotation,

      param_space: this.state.param_space,

      mix: this.state.mix,
    };

    postRequest('/visualize', body).then((res) => {
      console.log(res);
      this.setState({
        img_paths: res.filepaths,
        loading: false,
        mix: false
      })
    })
  };

  mixFeature = (event) => {

    this.setState({mix: true}, () => {this.visualizeFeature();});

  };

  getImagenetExamples = (event) => {

    this.setState({loading_imagenet: true});

    const api_key = 'dc6zaTOxFJmzC';
    const url = `http://api.giphy.com/v1/gifs/search?q=${'kanye'}&api_key=${api_key}`;
    let kanye_index = Math.floor(Math.random() * 24);
    fetch(url)
      .then(response => response.json())
      .then(data => this.setState({ imagenet_paths: [data.data[kanye_index].images.fixed_height.url] }));

    const body = {
      layer_name: this.state.layer_name,
      channel: this.state.channel,
    };

    postRequest('/predict_multiple', body).then((res) => {
      console.log(res);
      this.setState({
        imagenet_paths: res.filepaths,
        loading_imagenet: false
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
                <Select className={classes.layerInput} value={this.state.layer_name} onChange={this.handleInputChange} inputProps={{ name: 'layer_name',}}>
                {
                  this.state.all_layers.map((name, i) => (
                    <MenuItem key={i} value={name.id}>{name.name}</MenuItem>
                  ))
                }
                </Select>
                <TextField className={classes.paramInput} label="Channel(s):" name="channel" value={this.state.channel} onChange={this.handleInputChange} />
                {/*<Button variant="raised" className={classes.addButton} onClick={this.visualizeFeature}>add</Button>*/}

              </span>
              <FormLabel component="legend" style={{marginBottom: 0, marginTop: 10}}>Input Parameterization:</FormLabel>
              <span>
                <FormControlLabel control={<Radio/>} checked={this.state.param_space === 'naive'}
                                  onChange={this.handleInputChange} value={'naive'}
                                  name="param_space" label="Naive"/>
                <FormControlLabel control={<Radio/>} checked={this.state.param_space === 'fourier'}
                                  onChange={this.handleInputChange} value={'fourier'}
                                  name="param_space" label="Fourier"/>
                <FormControlLabel control={<Radio/>} checked={this.state.param_space === ''}
                                  onChange={this.handleInputChange} value={''}
                                  name="param_space" label="Option 3"/>
              </span>
              <span>
                <TextField className={classes.paramInput} label="Steps:" name="steps" value={this.state.steps} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Size:" name="dim" value={this.state.dim} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="LearningRate:" name="lr" value={this.state.lr} onChange={this.handleInputChange} />
              </span>
              <span>
                <TextField className={classes.paramInput} label="Padding:" name="pad" value={this.state.pad} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Jitter:" name="jitter" value={this.state.jitter} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Rotation:" name="rotation" value={this.state.rotation} onChange={this.handleInputChange}/>
                <TextField className={classes.paramInput} label="Scale:" name="scale" value={this.state.scale} onChange={this.handleInputChange}/>
              </span>
            </FormControl>
          </form>
          <span>
            <Button variant="raised" className={classes.visButton} onClick={this.visualizeFeature}>Visualize !</Button>
            <Button variant="raised" className={classes.visButton} onClick={this.mixFeature}>Mix</Button>
            <Button variant="raised" className={classes.visButton} onClick={this.getImagenetExamples}>find image examples</Button>
          </span>
        </Paper>
        <div>
          <Paper className={classes.paperImage}>
            {this.state.loading ? <h4>Visualizing, please wait.. <br />Todo: replace random cat gif with load bar</h4> : ''}
            {this.state.img_paths.map((filepath, index)=>(
                <img key={index} alt={this.state.layer} src={filepath} />
            ))}
          </Paper>
          <Paper className={classes.paperImage}>
            {this.state.loading_imagenet ? <p>Finding examples, please wait.. <br />Todo: replace random kanye gif with load bar</p> : ''}
            {this.state.imagenet_paths.map((filepath, index)=>(
                <img key={index} alt={index} src={filepath} />
            ))}
          </Paper>
        </div>
      </span>
    );
  }
}

export default withStyles(styles)(FeatureVis);
