import React, { useState, useEffect } from 'react'
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { CardMedia } from '@mui/material';
import { Link } from 'react-router-dom';
import emptyImage from '../components/img/empty.jpg'

const SharedCollectionsPage = () => {
  const [collections, setCollections] = useState([]);
  const [windowSize, setWindowSize] = useState([
    window.innerWidth,
    window.innerHeight,
  ]);

  useEffect(() => {
    const handleWindowResize = () => {
      setWindowSize([window.innerWidth, window.innerHeight]);
    };

    window.addEventListener('resize', handleWindowResize);

    return () => {
      window.removeEventListener('resize', handleWindowResize);
    };
  }, []);

  const options = {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.token}`
    },
  };

  useEffect(() => {
    fetch(`http://localhost:5000/sharedCollection/all`, options)
    .then((response) => response.json())
    .then((responseJson) => {
      setCollections(responseJson.collections)
    });
  }, []);

  if (collections.length === 0) {return (<><Typography paddingTop={5} textAlign={'center'} variant='h6' fontFamily={'Roboto'} fontWeight={700}>There are no shared collections at the moment</Typography></>)}

  return (
    <>
    {(windowSize[0] < 500) ? 
      <Grid container display={'flex'} flexDirection="row" alignItems="center" justifyContent="center" paddingLeft={3}>
      {collections.map((collection,i) =>
        <Grid key={`collectioncard#${i}`} item xs={4} paddingTop={5}>
          <Card style={{ height: '100%', width: `${(windowSize[0]-100)/3}px`}} sx={{ 
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: 3}}>
            <CardMedia  
            component="img" 
            image={collection.books[0] ?collection.books[0][2] : emptyImage}
            alt="collection image"
            sx={{ objectFit: "contain" }}
            alignItems= 'center'
            justifyContent= 'center'
            />
            <CardContent style={{textAlign: 'center'}}>
              <Typography component={Link} to={`/sharedCollections/${collection.collectionID}`} style={{ textDecoration: 'none', color:'black'}}>{collection.collectionName}</Typography>
            </CardContent>
          </Card>
        </Grid>
      )}
    </Grid> 
      :
      <>
      {(windowSize[0] < 900) ? 
      <Grid container display={'flex'} flexDirection="row" alignItems="center" justifyContent="center" paddingLeft={2}>
      {collections.map((collection,i) =>
        <Grid key={`collectioncard#${i}`} item xs={2.4} paddingTop={5}>
          <Card style={{ height: '100%', width: `${(windowSize[0]-100)/5}px`}} sx={{ 
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: 3}}>
            <CardMedia  
            component="img" 
            image={collection.books[0] ?collection.books[0][2] : emptyImage}
            alt="collection image"
            sx={{ objectFit: "contain" }}
            alignItems= 'center'
            justifyContent= 'center'
            />
            <CardContent style={{textAlign: 'center'}}>
              <Typography component={Link} to={`/sharedCollections/${collection.collectionID}`} style={{ textDecoration: 'none', color:'black'}}>{collection.collectionName}</Typography>
            </CardContent>
          </Card>
        </Grid>
      )}
    </Grid> 
        :
        <Grid container display={'flex'} flexDirection="row" alignItems="center" justifyContent="center" paddingLeft={3}>
        {collections.map((collection,i) =>
          <Grid key={`collectioncard#${i}`} item xs={2} paddingTop={5}>
            <Card style={{ height: '100%', width: `${(windowSize[0]-100)/7}px`}} sx={{ 
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              boxShadow: 3}}>
              <CardMedia  
              component="img" 
              image={collection.books[0] ?collection.books[0][2] : emptyImage}
              alt="collection image"
              sx={{ objectFit: "contain" }}
              alignItems= 'center'
              justifyContent= 'center'
              />
              <CardContent style={{textAlign: 'center'}}>
                <Typography component={Link} to={`/sharedCollections/${collection.collectionID}`} style={{ textDecoration: 'none', color:'black'}}>{collection.collectionName}</Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid> 
      }
      </>
    } 
    </>
  )
}

export default SharedCollectionsPage