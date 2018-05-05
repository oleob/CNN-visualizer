import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';

import './css/grid.css';
import './css/components.css';

import Header from './containers/Header';
import Content from './containers/Content';
import Footer from './containers/Footer';

import { getRequest } from './utilities/apiCalls';

class App extends Component {

  state = {
    networkName: '',
    imagePath: '',
  }

  componentDidMount() {
    getRequest('/current_settings').then((res)=> {
      this.setState({
          imagePath: res.image_path,
          networkName: res.network_name,
        });
    });
  }

  updateState = (values) => {
    let newState = {};
    //Map old values to new state
    Object.entries(this.state).map((item) => newState[item[0]] = item[1]);
    //map new values to new state
    Object.entries(values).map((item) => newState[item[0]] = item[1]);
    this.setState(newState);
  }

  render() {
    return(
      <BrowserRouter>
        <div className="grid">
            <Header globalState={this.state} updateGlobalState={this.updateState}/>
            <Content globalState={this.state} updateGlobalState={this.updateState}/>
            <Footer />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
