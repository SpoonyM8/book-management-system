import React from 'react';
import {  Routes, Route, Navigate } from "react-router-dom";
import { createTheme } from '@mui/material/styles';
import Register from './pages/Register';
import Login from './pages/Login/Login';
import Home from './routes/Home';
import Collection from './routes/Collection';
import BookPage from './routes/BookPage';
import Navbar from './components/Navbar';
import Search from './pages/Search';
import { ThemeProvider } from '@emotion/react';
import NavbarLayout from './routes/NavbarLayout';
import Profile from './pages/Profile';
import SharedCollectionsPage from './routes/SharedCollectionsPage';
import SpecificSharedCollectionPage from './routes/SpecificSharedCollectionPage';
import Goal from './pages/Goal/Goal';

const theme = createTheme({
  palette: {
    primary: {
      main: "#102C45",
      contrastText: '#fff',
    }
  }
});


function App() {
  return (
    <ThemeProvider theme={theme}>
      <Routes>
        <Route element={<NavbarLayout/>}>
          <Route path='/home' element={<Home/>} />
          <Route path='/collection/:id' element={<Collection/>} />
          <Route path='/book/:id' element={<BookPage/>}/>
          <Route exact path="/search" element={<Search/>}/>
          <Route path='/profile/:username' element={<Profile/>}/>
          <Route path='/sharedCollections' element={<SharedCollectionsPage/>}/>
          <Route path='/sharedCollections/:id' element={<SpecificSharedCollectionPage/>}/>
        </Route>
        <Route exact path="/" element={<Navigate to="/login"/>}/>
        <Route exact path="/register" element={<Register/>}/>
        <Route exact path="/login" element={<Login/>}/>
        <Route exact path="/goal" element={<Goal/>}/>
        <Route exact path="*" element={<Navigate to="/login"/>}/>
      </Routes>
    </ThemeProvider>
  );
}

export default App;
