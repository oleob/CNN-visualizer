import axios from 'axios';

const predict = (data) => {
  return new Promise((resolve, reject) => {
    axios.post('/predict', data).then((res) => {
      resolve(res.data)
    })
  })
}

const changeSettings = (settings) => {
  return new Promise((resolve, reject) => {
    axios.post('/change_settings', {...settings}).then((res) => {
      if(res.data.status === 'ok') {
        resolve(res.data)
      }
      else{
        reject(res.data)
      }
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

export {predict, activations, changeSettings};
