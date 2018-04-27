import React, { Component } from 'react';

import FeatureVis from '../../components/FeatureVis';

class Visualize extends Component {
  render() {
    return(
      <div className="content">
        <h1>Visualizing happens here</h1>
        <FeatureVis/>
      </div>
    );
  }
}

export default Visualize;
