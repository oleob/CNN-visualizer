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
import { CircularProgress } from 'material-ui/Progress';

import DisplayNetwork from './network/DisplayNetwork';

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
    width: 350
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
  channelInput: {
    marginTop: 10,
    marginRight: 20,
    width: 300

  },
  visButton: {
    marginTop: 10,
    marginRight: 20,
  },

  addButton: {
    width: 30
  },

  previewImage: {
    width: 300,
    marginBottom: 10,
  }

};


class FeatureVis extends Component {
  constructor(props) {
    super(props);
    this.state = {
      img_paths: [],
      channel: 134,
      steps: 200,
      lr: 0.01,
      dim: 300,
      pad: 16,
      jitter: 8,
      rotation: 5,
      scale: 0.0,

      loading: false,
      loading_img: false,

      decorrelate: true,

      all_layers: [],

      layers: [],
      selectedLayer: {
        info: {},
      },
    };
  }

  componentDidMount() {
    this.setState(this.props.localState);
    getRequest('/layer_info').then((res) => {
      this.setState({
        layers: res.layers,
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
      this.setState({lr: 3.0})
    } else if (value === 'laplacian') {
      this.setState({lr: 0.1})
    }
  };

  handleCheckbox = (event) => {
    this.setState({decorrelate: !this.state.decorrelate})
  };

  dreamImage = (event) => {

    this.setState({loading: true});

    const body = {
      layer_name: this.state.selectedLayer.output,
      channel: this.state.channel,
      steps: this.state.steps,
      lr: this.state.lr,
      dim: this.state.dim,
      pad: this.state.pad,
      jitter: this.state.jitter,
      rotation: this.state.rotation,
      scale: this.state.scale,

      decorrelate: this.state.decorrelate,
    };

    postRequest('/deep_dream', body).then((res) => {
      console.log(res);
      this.setState({
        img_paths: res.filepaths,
        loading: false,
      })
    })
  };

  changeSelectedLayer = layer => {
    this.setState({selectedLayer: layer})
  };

  uploadFile = event => {
      let file = event.target.files[0];
      if (file) {
        let data = new FormData();
        data.append('image', file);
        this.setState({
          loading_img: true,
        });
        postRequest('/upload_image', data).then((res) => {
          if (res.status==='ok'){
            this.setState({
              loading_img: false,
            });
            this.props.updateGlobalState({imagePath: res.image_path})
          }
        });
      }
  };




  render() {
    const { classes } = this.props;
    return (
      <span className={classes.mainSpan}>
        <Paper className={classes.paperSettings}>
          <form>
            <FormControl>
              <h2>Deep Dream</h2>
              <span>
                {(this.props.globalState.imagePath !== '') &&
                  <div>
                    <img alt="current" className={classes.previewImage} src={this.props.globalState.imagePath}/>
                  </div>
                }
                <input accept="image/*" id="raised-button-file" onChange={this.uploadFile} type="file" style={{"display" : "none"}}/>
                <label className={classes.button} htmlFor="raised-button-file">
                  {!this.state.loading_img &&
                    <Button variant="raised" component="span" >
                      Upload image
                    </Button>
                  }
            {this.state.loading_img && <CircularProgress size={68} />}
          </label>
                <DisplayNetwork layers={this.state.layers} selectedLayer={this.state.selectedLayer} changeSelectedLayer={this.changeSelectedLayer}/>
                <TextField className={classes.channelInput} label="Channel(s):" name="channel" value={this.state.channel} onChange={this.handleInputChange} />
                {/*<Button variant="raised" className={classes.addButton} onClick={this.visualizeFeature}>add</Button>*/}

              </span>
                <FormControlLabel control={<Checkbox/>} checked={this.state.decorrelate}
                                  onChange={this.handleCheckbox} value={this.state.decorrelate}
                                  name="decorrelate" label="Decorrelate Colors"/>
              <span>
                <TextField className={classes.paramInput} label="Steps:" name="steps" value={this.state.steps} onChange={this.handleInputChange} />
                <TextField className={classes.paramInput} label="Width:" name="dim" value={this.state.dim} onChange={this.handleInputChange} />
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
            <Button variant="raised" className={classes.visButton} onClick={this.dreamImage}>Deep Dream</Button>
          </span>
        </Paper>
        <Paper className={classes.paperImage}>
          {this.state.loading ? <h4>Dreaming, please wait.. <br /><CircularProgress size={68} className={classes.loadingIcon}/></h4> : ''}
          {this.state.img_paths.map((filepath, index)=>(
              <img key={index} alt={this.state.layer} src={filepath} />
          ))}
        </Paper>
      </span>
    );
  }
}

export default withStyles(styles)(FeatureVis);
