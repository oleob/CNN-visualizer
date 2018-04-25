import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';

import './css/grid.css';
import './css/components.css';

import Header from './containers/Header';
import Content from './containers/Content';
import Footer from './containers/Footer';

class App extends Component {

  render() {
    return(
      <BrowserRouter>
        <div className="grid">
            <Header />
            <Content />
            <Footer />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
