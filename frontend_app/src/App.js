import './App.css';
import { BrowserRouter as Router } from "react-router-dom";
import { Route, Routes } from "react-router-dom";
import Login from './Login';
import Home from './Home';
import Time from './Time';
import { useState, useEffect } from 'react';
import Nav from './Nav';
import axios from "axios"
import { useSelector, useDispatch } from 'react-redux';

function App() {
  return (
    <>
      <Router>

        <Nav></Nav>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/time" element={<Time />} />
        </Routes>
      </Router>
    </>
  );
}


export default App;
