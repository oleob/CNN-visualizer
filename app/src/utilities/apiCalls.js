import axios from 'axios';

const predict = (data) => {
  return new Promise((resolve, reject) => {
    axios.post('/predict', data).then((res) => {
      resolve(res.data)
    })
  })
}

const activations = (layerName) => {
  return new Promise((resolve, reject) => {
    axios.post('activations', {layer_name: layerName}).then((res) => {
      resolve(res.data);
    })
  })
}

const visualize = (parameters_here) => {
  return new Promise((resolve, reject) => {
    axios.post('/visualize', {layer_name: 'InceptionV1/InceptionV1/Mixed_3a/concat:0', channel: 0}).then((res) => {
      resolve(res.data);
    })
  })
}


export {predict, activations, visualize};
