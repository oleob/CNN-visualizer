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
    axios.post('activations', {layerName}).then((res) => {
      resolve(res.data);
    })
  })
}

export {predict, activations};
