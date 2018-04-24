import React,  { Component } from 'react';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Tabs, { Tab } from 'material-ui/Tabs';
import { withStyles } from 'material-ui/styles';
import Toolbar from 'material-ui/Toolbar';

import SettingsDrawer from '../components/SettingsDrawer';

const styles = {
  root: {
    flexGrow: 1,
  },
  flex: {
    flex: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  tabs: {

  }
};

class Header extends Component {
  state = {
    showDrawer: false,
    pageIndex: 0
  }

  toggleDrawer = () => {
    this.setState({
      showDrawer: !this.state.showDrawer
    });
  };

  handleChange = (event, value) => {
    this.setState({pageIndex: value});
  }

  render(){
    const {classes} = this.props;
    return (
      <div className="header">
        <div className={classes.root}>
          <AppBar position="static">
            <Toolbar>
              <IconButton color="inherit" aria-label="Menu">
                <MenuIcon onClick={this.toggleDrawer}/>
              </IconButton>
              <Tabs className={classes.tabs} value={this.state.pageIndex} onChange={this.handleChange} indicatorColor="secondary" textColor="secondary" centered>
                <Tab label="Item One" />
                <Tab label="Item Two" />
                <Tab label="Item Three" />
              </Tabs>
            </Toolbar>
          </AppBar>
          <SettingsDrawer toggleDrawer={this.toggleDrawer} showDrawer={this.state.showDrawer} />
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(Header);
