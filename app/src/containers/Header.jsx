import React,  { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import MenuIcon from '@material-ui/icons/Menu';

import SettingsDrawer from '../components/SettingsDrawer';

class Header extends Component {
  state = {
    showDrawer: false,
  }

  toggleDrawer = () => {
    this.setState({
      showDrawer: !this.state.showDrawer
    });
  };

  render(){
    return (
      <div className="header">
        <AppBar>
          <IconButton color="inherit" aria-label="Menu">
            <MenuIcon onClick={this.toggleDrawer}/>
          </IconButton>
        </AppBar>
        <SettingsDrawer toggleDrawer={this.toggleDrawer} showDrawer={this.state.showDrawer} />
      </div>
    );
  }
}

export default Header;
