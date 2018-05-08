import React, { Component } from 'react';
import Paper from 'material-ui/Paper';
import { withStyles } from 'material-ui/styles';
import Typography from 'material-ui/Typography';
import { postRequest } from '../utilities/apiCalls';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import { CircularProgress } from 'material-ui/Progress';

import DeepTaylorDisplay from './DeepTaylorDisplay';

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

class DeepTaylorSettings extends Component {

  state = {
    loading: false,
    numFilters: 10,
    result: {},
  }

  componentDidMount() {
    this.setState(this.props.localState)
  }

  componentWillUnmount() {
    this.props.updateState(this.state)
  }

  handleChange = name => event => {
   this.setState({ [name]: event.target.value });
  };

  getDecomposition = () => {

    this.setState({loading: true});

    const body = {
      num_filters: this.state.numFilters,
    };

    postRequest('/deep_taylor', body).then((res)=>{
      this.setState({
        result: res.results,
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
            <TextField
              id="number"
              label="Number of ranked filters"
              value={this.state.numFilters}
              onChange={this.handleChange('numFilters')}
              type="number"
              className={classes.textField}
              InputLabelProps={{
                shrink: true,
              }}
              margin="normal"
            />
          </form>
          <div className={classes.buttonContainer}>
            {!this.state.loading &&
              <Button className={classes.saveButton} onClick={this.getDecomposition} variant="raised">
                Get Decomposition
              </Button>
            }
            {this.state.loading &&
              <CircularProgress size={68} className={classes.loadingIcon}/>
            }
          </div>
        </Paper>
        <DeepTaylorDisplay result={this.state.result}/>
      </div>
    )
  }
}

export default withStyles(styles)(DeepTaylorSettings);
