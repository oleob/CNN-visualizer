import React, {Component} from 'react';
import {Route, Switch} from 'react-router-dom';

//import Graph from '../components/Graph';
//import Layer from '../components/Layer';
//import ImageForm from '../components/ImageForm';
import Home from './subContainers/Home';
import Predict from './subContainers/Predict';
import Visualize from './subContainers/Visualize';
import Activations from './subContainers/Activations';

class Content extends Component {

  render(){
    return(
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/predict" component={Predict} />
        <Route path="/visualize" component={Visualize} />
        <Route path="/activations" component={Activations} />
      </Switch>
    );
  }

}

export default Content;
