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
    result: {}
  }

  componentDidMount() {
    getRequest('/layer_names').then((res) => {
      this.setState({
        layerNames: res.names,
      });
    })
  }

  handleChange = event => {
   this.setState({ [event.target.name]: event.target.value });
  };

  getActivations = () => {
    const body = {
      layer_name: this.state.selectedLayer,
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
    console.log(this.state)
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
              <Select value={this.state.selectedLayer} onChange={this.handleChange} inputProps={{ name: 'selectedLayer', id: 'controlled-open-select',}}>
                {
                  this.state.layerNames.map((name, i) => (
                    <MenuItem key={i} value={name.id}>{name.name}</MenuItem>
                  ))
                }
              </Select>
            </FormControl>
          </form>
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
