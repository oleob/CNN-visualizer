import React, { Component } from 'react';

import DeepTaylorSettings from '../../components/DeepTaylorSettings';

class DeepTaylor extends Component {

  updateState = (newState) => {
    this.props.updateState(this.props.name, newState);
  }

  render() {
    return(
      <div className="content">
        <DeepTaylorSettings
          localState={this.props.localState}
          globalState={this.props.globalState}
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
        />
      </div>
    )
  }
}

export default DeepTaylor;
