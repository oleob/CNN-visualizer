import React,  { Component } from 'react';

import ImageForm from '../../components/ImageForm';

class Predict extends Component {

  updateState = (newState) => {
    this.props.updateState(this.props.name, newState);
  }

  render() {
    return(
      <div className="content">
        <ImageForm
          localState={this.props.localState}
          globalState={this.props.globalState}
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}/>
      </div>
    );
  }
}

export default Predict;
