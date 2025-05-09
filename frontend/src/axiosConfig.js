import axios from 'axios';

// Set axios to send cookies with every request globally
axios.defaults.withCredentials = true;

export default axios;
