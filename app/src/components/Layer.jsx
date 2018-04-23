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
      activations(this.props.layerName).then((res) => {
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
        <p style={{margin:0}}>{this.props.layerName}</p>
        <Activations showActivations={this.state.showActivations} filepaths={this.state.filepaths}/>
      </div>
    );
  }
}


export default Layer;
