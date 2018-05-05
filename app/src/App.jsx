import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';

import './css/grid.css';
import './css/components.css';

import Header from './containers/Header';
import Content from './containers/Content';
import Footer from './containers/Footer';

class App extends Component {

  state = {
    networkName: '',
    imagePath: '',
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
            <Header updateGlobalState={this.updateState}/>
            <Content updateGlobalState={this.updateState}/>
            <Footer />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
