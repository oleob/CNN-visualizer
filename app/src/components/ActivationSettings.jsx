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
    layerNames: [],
    selectedLayer: '',
    loading: false,
    result: {},
    numActivations: 10,
  }

  componentDidMount() {
    this.setState(this.props.localState)
    getRequest('/layer_names').then((res) => {
      this.setState({
        layerNames: res.names,
      });
    })
  }

  componentWillUnmount() {
    this.props.updateState(this.state)
  }

  handleChange = name => event => {
   this.setState({ [name]: event.target.value });
  };

  getActivations = () => {
    const body = {
      layer_name: this.state.selectedLayer,
      num_activations: this.state.numActivations,
    };
    this.setState({
      loading: true,
    })
    postRequest('/activations', body).then((res) => {
      this.setState({
        result: res.result,
        loading: false,
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
          <form autoComplete="off">
            <FormControl className={classes.formControl}>
              <InputLabel htmlFor="controlled-open-select">Layer Name</InputLabel>
              <Select value={this.state.selectedLayer} onChange={this.handleChange("selectedLayer")} inputProps={{ name: 'selectedLayer', id: 'controlled-open-select',}}>
                {
                  this.state.layerNames.map((name, i) => (
                    <MenuItem key={i} value={name.id}>{name.name}</MenuItem>
                  ))
                }
              </Select>
            </FormControl>
          </form>
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
              <Button className={classes.saveButton} disabled={(this.state.selectedLayer==='')} onClick={this.getActivations} variant="raised">
                Get Activations
              </Button>
            }
            {this.state.loading &&
              <CircularProgress size={68} className={classes.loadingIcon}/>
            }
          </div>
        </Paper>
        <ActivationDisplay result={this.state.result}/>
      </div>
    )
  }
}

export default withStyles(styles)(ActivationSettings);
