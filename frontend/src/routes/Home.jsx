import React from 'react';
import { useSearchParams } from 'react-router-dom';
import Card from '@mui/material/Card';
import Book from '../components/Book';
import Grid from '@mui/material/Grid';
import Body from '../components/Body'
import Navbar from '../components/Navbar';

const Home = () => {

  return (
    <>
      <Grid 
          container 
          direction="column"
          justifyContent="center"
          alignItems="stretch"
      >
        <Grid item xs>
            <Body/>
        </Grid>
      </Grid>
    </>
  )
}

export default Home;
