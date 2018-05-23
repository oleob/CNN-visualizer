import React, { Component } from 'react';
import Paper from 'material-ui/Paper';
import { withStyles } from 'material-ui/styles';
import Typography from 'material-ui/Typography';
import { getRequest, postRequest } from '../utilities/apiCalls';
import { MenuItem } from 'material-ui/Menu';
import Select from 'material-ui/Select';
import { FormControl } from 'material-ui/Form';
import { InputLabel } from 'material-ui/Input';
import Button from 'material-ui/Button';
import { CircularProgress } from 'material-ui/Progress';
import TextField from 'material-ui/TextField';

import ActivationDisplay from './ActivationDisplay';
import DisplayNetwork from './network/DisplayNetwork';

const styles = {
  paper: {
    display: 'inline-block',
    padding: 20,
  },
  container: {
    textAlign: 'center',
    marginTop: 20,
  },
  formControl: {
    minWidth: 120,
  },
  buttonContainer: {
    marginTop: 15,
  }
};

class ActivationSettings extends Component {

  state = {
    layers: [],
    selectedLayer: {
      info: {},
    },
    loading: false,
    results: [],
    numActivations: 10,
  }

  componentDidMount() {
    this.setState(this.props.localState)
    getRequest('/layer_info').then((res) => {
      this.setState({
        layers: res.layers,
      });
    })
  }

  componentWillUnmount() {
    this.props.updateState(this.state)
  }

  changeSelectedLayer = layer => {
    this.setState({selectedLayer: layer})
  }

  handleChange = name => event => {
   this.setState({ [name]: event.target.value });
  };

  getActivations = () => {
    const body = {
      layer_name: this.state.selectedLayer.output,
      num_activations: this.state.numActivations,
    };
    this.setState({
      loading: true,
    })
    postRequest('/activations', body).then((res) => {
      this.setState(prevState => {
        const r = {
          info: prevState.selectedLayer.info,
          images: res.result,
        }
        prevState.results.unshift(r)
        return({
          results: prevState.results,
          loading: false,
        })
      })
    })
  }

  render() {
    const { classes } = this.props;
    return(
      <div className={classes.container}>
        <Paper className={classes.paper}>
          <Typography variant="headline" component="h3">
            Settings
          </Typography>
          <DisplayNetwork layers={this.state.layers} selectedLayer={this.state.selectedLayer} changeSelectedLayer={this.changeSelectedLayer}/>
          <TextField
            id="number"
            label="Number of activations"
            value={this.state.numActivations}
            onChange={this.handleChange('numActivations')}
            type="number"
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            margin="normal"
          />
          <div className={classes.buttonContainer}>
            {!this.state.loading &&
              <Button className={classes.saveButton} disabled={(Object.keys(this.state.selectedLayer.info).length === 0)} onClick={this.getActivations} variant="raised">
                Get Activations
              </Button>
            }
            {this.state.loading &&
              <CircularProgress size={68} className={classes.loadingIcon}/>
            }
          </div>
        </Paper>
        <ActivationDisplay results={this.state.results}/>
      </div>
    )
  }
}

export default withStyles(styles)(ActivationSettings);
