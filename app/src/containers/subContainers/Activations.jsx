import React, { Component } from 'react';

import ActivationSettings from '../../components/ActivationSettings';

class Activations extends Component {
  updateState = (newState) => {
    this.props.updateState(this.props.name, newState);
  }

  render() {
    return(
      <div className='content'>
        <ActivationSettings
          localState={this.props.localState}
          globalState={this.props.globalState}
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState} />
      </div>
    );
  }
}

export default Activations;
