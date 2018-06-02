import React,  { Component } from 'react';
import { Link } from 'react-router-dom';
import AppBar from 'material-ui/AppBar';
import IconButton from 'material-ui/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Tabs, { Tab } from 'material-ui/Tabs';
import { withStyles } from 'material-ui/styles';
import {withRouter} from 'react-router-dom';
import Toolbar from 'material-ui/Toolbar';

import SettingsDrawer from '../components/SettingsDrawer';

const HomeLink = props => <Link to="/" style={{ textDecoration: 'none' }} {...props}/>
const PredictLink = props => <Link to="/predict" style={{ textDecoration: 'none' }} {...props}/>
const VisualizeLink = props => <Link to="/visualize" style={{ textDecoration: 'none' }} {...props}/>
const DeepDreamLink = props => <Link to="/deep_dream" style={{ textDecoration: 'none'}} {...props}/>
const ActivationsLink = props => <Link to="/activations" style={{ textDecoration: 'none' }} {...props}/>
const DeepTaylorLink = props => <Link to="/deep_taylor" style={{ textDecoration: 'none' }} {...props}/>

const links = ['/', '/predict', '/visualize', '/deep_dream', '/activations', '/deep_taylor'];

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
  constructor(props) {
    super();
    this.state = {
      showDrawer: false,
      pageIndex: links.indexOf(props.location.pathname)
    }
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
                <Tab label="Home" component={HomeLink} />
                <Tab label="Predict" component={PredictLink} />
                <Tab label="Visualize" component={VisualizeLink} />
                <Tab label="Deep Dream" component={DeepDreamLink} />
                <Tab label="Activations" component={ActivationsLink} />
                <Tab label="Deep Taylor Decomposition" component={DeepTaylorLink} />
              </Tabs>
            </Toolbar>
          </AppBar>
          <SettingsDrawer globalState={this.props.globalState} updateGlobalState={this.props.updateGlobalState} toggleDrawer={this.toggleDrawer} showDrawer={this.state.showDrawer} />
        </div>
      </div>
    );
  }
}

export default withRouter(withStyles(styles)(Header));
