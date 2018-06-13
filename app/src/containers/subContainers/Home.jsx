import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';

import HomeLink from '../../components/HomeLink';

const styles = {
  linkContainer: {
    height: '100%',
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'center',
  }
}

class Home extends Component {

  state = {
    linkInfo: [
      {
        name: 'Prediction',
        imagePath: '/static/images/thumbnails/predict.jpg',
        description: 'This page lets the user generated classifications for uploaded images, by utilizing the selected network.',
        text: '',
        link:'/predict',
      },
      {
        name: 'Feature visualization',
        imagePath: '/static/images/thumbnails/feature.jpg',
        description: 'On this page the user can visualize features present within a convolutional neural network',
        text: 'The user has the possiblity to choose which layer, and which filters within the selected layer to visualize. In addition there are several paramters which the user can adjust, in order to improve the quality of the resulting visualizations.',
        link:'/visualize',
      },
      {
        name: 'Deep Dream',
        imagePath: '/static/images/thumbnails/deepdream.jpg',
        description: 'Here the user can create "Deep Dreamed" versions of images uploaded to the server.',
        text: '',
        link:'/deep_dream',
      },
      {
        name: 'Activation visualization',
        imagePath: '/static/images/thumbnails/activation.jpg',
        description: 'This page lets the user visualize the output (also known as activations) for a selected layer.',
        text: '',
        link:'/activations',
      },
      {
        name: 'Deep Taylor Decomposition',
        imagePath: '/static/images/thumbnails/heatmap.jpg',
        description: 'This method lets the user generate a heatmap for a given image, which highlights areas of the original image that were important for classifying said image.',
        text: '',
        link:'/deep_taylor',
      },
    ]
  }

  render() {
    const {classes} = this.props;
    return(
      <div className="content">
        <div className={classes.linkContainer}>
          {
            this.state.linkInfo.map((info, index) => (
              <HomeLink key={index} {...info} />
            ))
          }
        </div>
      </div>
    );
  }
}

export default withStyles(styles)(Home);
