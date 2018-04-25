import axios from 'axios';

const postRequest = (url, body) => {
  return new Promise((resolve, reject) => {
    axios.post(url, body).then((res) => {
      if(res.status===200){
        resolve(res.data)
      } else {
        reject(res)
      }
    });
  });
}

const getRequest = (url) => {
  return new Promise((resolve, reject) => {
    axios.get(url).then((res) => {
      if(res.status===200){
        resolve(res.data)
      } else {
        reject(res)
      }
    });
  });
}

const activations = (layerName) => {
  return new Promise((resolve, reject) => {
    axios.post('activations', {layer_name: layerName}).then((res) => {
      resolve(res.data);
    })
  })
}

export {activations, postRequest, getRequest};
