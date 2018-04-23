import React, { Component } from 'react';
import './css/grid.css';
import './css/components.css';

import Header from './containers/Header';
import Content from './containers/Content';
import Footer from './containers/Footer';

class App extends Component {

  render() {
    return(
      <div className="grid">
        <Header />
        <Content />
        <Footer />
      </div>
    );
  }
}

export default App;
