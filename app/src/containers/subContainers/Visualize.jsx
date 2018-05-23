import React, { Component } from 'react';

import FeatureVis from '../../components/FeatureVis';

class Visualize extends Component {

  updateState = (newState) => {
    this.props.updateState(this.props.name, newState);
  }

  render() {
    return(
      <div className="content">
        <FeatureVis
          localState={this.props.localState}
          globalState={this.props.globalState}
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
        />
      </div>
    );
  }
}

export default Visualize;
