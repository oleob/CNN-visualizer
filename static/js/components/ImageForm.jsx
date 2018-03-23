import React, { Component } from 'react';
import Button from 'material-ui/RaisedButton';

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
        <Button containerElement='label' label='Upload file'>
          <input type="file" name="myFile" onChange={this.uploadFile}  style={{"display" : "none"}}/>
        </Button>
        <Scoreboard results={this.state.results} />
      </div>
    )
  }
}

export default ImageForm
