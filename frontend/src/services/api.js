import axios from 'axios';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

export const getPrediction = async (inputValue) => {
  try {
    const response = await API.post('predict/', { input: [inputValue] });
    return response.data.prediction;
  } catch (error) {
    console.error('Prediction Error:', error);
    return null;
  }
};

export default API;
