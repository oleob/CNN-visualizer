import React, {Component} from 'react';
import {Route, Switch} from 'react-router-dom';

//import Graph from '../components/Graph';
//import Layer from '../components/Layer';
//import ImageForm from '../components/ImageForm';
import Home from './subContainers/Home';
import Predict from './subContainers/Predict';
import Visualize from './subContainers/Visualize';

class Content extends Component {

  render(){
    return(
      <div className="content">
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/predict" component={Predict} />
          <Route path="/visualize" component={Visualize} />
        </Switch>
      </div>
    );
  }

}

export default Content;
