import React, {Component} from 'react';

import Graph from '../components/Graph';
import Layer from '../components/Layer';
import ImageForm from '../components/ImageForm';

class Content extends Component {

  constructor(){
    super()

  }

  render(){
    return(
      <div className="content">
        <div className="contentCenter">
          <ImageForm />
          <Graph spacing={40} size={150}>
            <Layer layerName="mixed3a"/>
            <Layer layerName="mixed3b"/>
            <Layer layerName="mixed4a"/>
            <Layer layerName="mixed4b"/>
            <Layer layerName="mixed4c"/>
            <Layer layerName="mixed4d"/>
            <Layer layerName="mixed4e"/>
            <Layer layerName="mixed5a"/>
          </Graph>
        </div>
      </div>
    );
  }

}

export default Content;
