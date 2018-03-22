import React, {Component} from 'react';

import Graph from '../components/Graph';
import Layer from '../components/Layer';
import SubLayer from '../components/SubLayer';
import ImageForm from '../components/ImageForm';

class Content extends Component {

  constructor(){
    super()

  }

  render(){
    return(
      <div className="content">
        <div className="contentCenter">
          <Graph spacing={40} size={150}>
            <Layer>
              <SubLayer size={120} />
              <SubLayer size={120} />
            </Layer>
            <Layer />
          </Graph>
          <ImageForm />
        </div>
      </div>
    );
  }

}

export default Content;
