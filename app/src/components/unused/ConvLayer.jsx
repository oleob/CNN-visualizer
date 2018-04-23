import React, { Component } from 'react';
import {Circle} from 'react-konva';

class ConvLayer extends Component {
  constructor(){
    super();
    this.state = {
      color: 'black',
      radius: 10,
    }
    this.onClick = this.onClick.bind(this);
  }

  onClick(){
    this.setState({
      radius: this.state.radius + 10,
    })
  }

  render(){
    return(
      <Circle className="convlayer" x={this.props.x} y={this.props.y} radius={this.state.radius} fill={this.state.color} onClick={this.onClick}/>
    )
  }
}

export default ConvLayer;
