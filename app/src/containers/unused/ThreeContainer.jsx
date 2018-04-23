import React, { Component } from 'react';
import {run} from '../utilities/ThreeHelper';

class ThreeContainer extends Component {

  constructor(){
    super();
  }

  componentDidMount(){
    run(this.refs.content)
  }

  render(){
    return(
      <div className="content" ref="content" />
    )
  }
}

export default ThreeContainer;
