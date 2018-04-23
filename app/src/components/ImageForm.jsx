import React, { Component } from 'react';
import Button from 'material-ui/Button';

import {predict} from '../utilities/apiCalls';
import Scoreboard from './Scoreboard';

class ImageForm extends Component {
  constructor(props) {
    super(props)

    this.state={
      results: [],
    }

    this.uploadFile = this.uploadFile.bind(this);
  }

  uploadFile(event) {
      let file = event.target.files[0];
      if (file) {
        let data = new FormData();
        data.append('image', file);
        predict(data).then((results)=>{
          this.setState({
            results,
          })
        })
      }
  }

  render() {
    return (
      <div className = "imageForm">
        <input accept="image/*" id="raised-button-file" onChange={this.uploadFile} type="file" style={{"display" : "none"}}/>
        <label htmlFor="raised-button-file">
          <Button variant="raised" component="span" >
            Upload image
          </Button>
        </label>
        <Scoreboard results={this.state.results} />
      </div>
    )
  }
}

export default ImageForm
