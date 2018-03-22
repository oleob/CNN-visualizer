import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import '../css/grid.css';


import Header from './containers/Header';
import Content from './containers/Content';
import Footer from './containers/Footer';

class App extends Component {
  constructor(){
    super();
  }

  render() {
    return(
      <MuiThemeProvider>
        <div className="grid">
          <Header />
          <Content />
          <Footer />
        </div>
      </MuiThemeProvider>
    );
  }
}

export default App;
