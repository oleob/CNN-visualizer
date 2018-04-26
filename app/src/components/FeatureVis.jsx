import React, { Component } from 'react';
import Button from 'material-ui/Button';

import {visualize} from '../utilities/apiCalls';

class FeatureVis extends Component {
  constructor(props) {
    super(props)

    this.state={
      results: [],
    }

    this.visualizeFeature = this.visualizeFeature.bind(this);
  }

  visualizeFeature(event) {
      visualize().then((results)=>{
          this.setState({
              results,
          })
      })
  }

  render() {
    return (
      <div className = "featureVis">
        <label htmlFor="raised-button-file">
          <Button variant="raised" component="span" onClick={this.visualizeFeature}>
            Visualize Stuff
          </Button>
        </label>
          <div>{this.state.results}</div>
      </div>
    )
  }
}

export default FeatureVis
