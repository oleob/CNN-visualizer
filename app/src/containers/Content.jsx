import React, {Component} from 'react';
import {Route, Switch} from 'react-router-dom';

//import Graph from '../components/Graph';
//import Layer from '../components/Layer';
//import ImageForm from '../components/ImageForm';
import Home from './subContainers/Home';
import Predict from './subContainers/Predict';
import Visualize from './subContainers/Visualize';
import Activations from './subContainers/Activations';
import DeepTaylor from './subContainers/DeepTaylor';

class Content extends Component {

  state = {
    home: {

    },
    predict: {

    },
    visualize: {

    },
    activations: {

    },
    deepTaylor: {

    }
  }

  updateState = (name, values) => {
    let newState = {};
    //Map old values to new state
    Object.entries(this.state[name]).map((item) => newState[item[0]] = item[1]);
    //map new values to new state
    Object.entries(values).map((item) => newState[item[0]] = item[1]);
    this.setState({ [name]: newState });
  }

  render(){
    return(
      <Switch>
        <Route exact path="/"
        render={() => (<Home
          name="home"
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
          globalState={this.props.globalState}
          localState={this.state.home} />)}
        />
        <Route path="/predict"
        render={() => (<Predict
          name="predict"
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
          globalState={this.props.globalState}
          localState={this.state.predict} />)}
        />
        <Route path="/visualize"
        render={() => (<Visualize
          name="visualize"
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
          globalState={this.props.globalState}
          localState={this.state.visualize} />)}
        />
        <Route path="/activations"
        render={() => (<Activations
          name="activations"
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
          globalState={this.props.globalState}
          localState={this.state.activations} />)}
        />
        <Route path="/deep_taylor"
        render={() => (<DeepTaylor
          name="deepTaylor"
          updateState={this.updateState}
          updateGlobalState={this.props.updateGlobalState}
          globalState={this.props.globalState}
          localState={this.state.deepTaylor} />)}
        />
      </Switch>
    );
  }

}

export default Content;
