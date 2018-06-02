import React, { Component } from 'react';

import DeepDreamSettings from '../../components/DeepDreamSettings';

class DeepDream extends Component {

  updateState = (newState) => {
    this.props.updateState(this.props.name, newState);
  }

  render() {
    return(
      <div className="content">
        <DeepDreamSettings
          localState={this.props.localState}
          globalState={this.props.globalState}
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
        />
      </div>
    );
  }
}

export default DeepDream;
