import React, { Component } from 'react';

import { activations } from '../utilities/apiCalls';

import Activations from './Activations';

class Layer extends Component {

  constructor(){
    super();

    this.state = {
      showActivations: false,
      filepaths: [],
    }

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(){
    if(!this.state.showActivations){
      activations().then((res) => {
        this.setState({
          showActivations: true,
          filepaths: res.filepaths,
        });
      })
    } else {
      this.setState({
        showActivations: !this.state.showActivations,
      });
    }
  }

  render(){
    return (
      <div className="layer" onClick={this.handleClick}>
        <Activations showActivations={this.state.showActivations} filepaths={this.state.filepaths}/>
        <p style={{margin:0}}>placeholder</p>
      </div>
    );
  }
}


export default Layer;
