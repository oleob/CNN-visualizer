import React, { Component } from 'react';
import {predict} from '../utilities/apiCalls';

class ImageForm extends Component {
    constructor(props) {
      super(props)
      this.uploadFile = this.uploadFile.bind(this);
    }

    uploadFile(event) {
        let file = event.target.files[0];
        if (file) {
          let data = new FormData();
          data.append('image', file);
          predict(data)
        }
    }

    render() {
      return <span>
        <input type="file"
        name="myFile"
        onChange={this.uploadFile} />
      </span>
    }
}

export default ImageForm
