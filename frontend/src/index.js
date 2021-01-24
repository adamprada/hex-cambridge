import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import firebase from "firebase/app";

var firebaseConfig = {
  apiKey: "AIzaSyD7ynAWSy2ZKledOKKpyhLIlqL-dQz-ztA",
  authDomain: "hex-cambridge-project-2021.firebaseapp.com",
  databaseURL: "https://hex-cambridge-project-2021-default-rtdb.firebaseio.com",
  projectId: "hex-cambridge-project-2021",
  storageBucket: "hex-cambridge-project-2021.appspot.com",
  messagingSenderId: "521415691580",
  appId: "1:521415691580:web:7fecfde9c768ff39dae239",
  measurementId: "G-ZZZBL1D4H6"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);