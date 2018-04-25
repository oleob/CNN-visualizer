import React, { Component } from 'react';
import Drawer from 'material-ui/Drawer';
import Button from 'material-ui/Button';
import { MenuItem } from 'material-ui/Menu';
import Select from 'material-ui/Select';
import { FormControl } from 'material-ui/Form';
import { InputLabel } from 'material-ui/Input';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

import {postRequest} from '../utilities/apiCalls';

const networkNames = ['InceptionV1', 'vgg_16'];

const styles = theme => ({
  networkName: {
    width: 'auto',
    marginLeft: 20,
    marginRight: 20,
    marginTop: 30,
  },
  saveButton: {
    marginLeft: 20,
    marginRight: 20,
    marginTop: 15,
  },
  buttonContainer: {
    textAlign: 'center',
  },
  loadingIcon: {
    marginTop: 15,
  },
});

class SettingsDrawer extends Component {

  state = {
     networkName: networkNames[0],
     loading: false,
   };

  handleChange = event => {
   this.setState({ [event.target.name]: event.target.value });
  };

  saveChanges = event => {
    this.setState({loading: true});
    const settings = {
      network_name: this.state.networkName,
    };

    postRequest('/change_settings', settings).then((res)=>{
      this.setState({loading: false})
    });
  }

  render(){
    const { classes } = this.props;

    return (
      <Drawer className={classes.drawer} open={this.props.showDrawer} onClose={this.props.toggleDrawer}>
        <form autoComplete="off">
          <FormControl className={classes.networkName} >
            <InputLabel htmlFor="controlled-open-select">Model</InputLabel>
            <Select value={this.state.networkName} onChange={this.handleChange} inputProps={{ name: 'networkName', id: 'controlled-open-select',}}>
              {
                networkNames.map((name, i) => (
                  <MenuItem key={i} value={name}>{name}</MenuItem>
                ))
              }
            </Select>
          </FormControl>
        </form>
        <div className={classes.buttonContainer}>
          {!this.state.loading &&
            <Button className={classes.saveButton} onClick={this.saveChanges} variant="raised">
              Save changes
            </Button>
          }
          {this.state.loading &&
            <CircularProgress size={68} className={classes.loadingIcon}/>
          }
        </div>
      </Drawer>
    );
  }

}


export default withStyles(styles)(SettingsDrawer);
