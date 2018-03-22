import axios from 'axios';

const predict = (data) => {
  axios.post('/predict', data).then((res)=>{
    console.log(res.data);
  })
}

export {predict};
