import React, { useState, useEffect } from 'react'
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { CardMedia } from '@mui/material';
import { Link } from 'react-router-dom';
import RecentlyAdded from './RecentlyAdded';

const CollectionCard = (props) => {

  const [collections, setCollections] = useState([]);

  const options = {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.token}`
    },
  };

  useEffect(() => {
    if (props.shouldFetch) {
      fetch(`http://localhost:5000/collections/user/${props.username}`, options)
      .then((response) => response.json())
      .then((responseJson) => {
        setCollections(responseJson.collections)
        props.setShouldFetch(false)
      });
    }
  }, [props.shouldFetch]);

  if (!collections) {return (<>Empty Collection</>)}

  return (
    <>
      <Grid container >
        {collections.map((collection,i) => 
          <Grid key={`collectioncard#${i}`} container direction="row" alignItems="center" justifyContent="center" item xs={12} padding={2} style={{ backgroundColor: "#E8ECEE" }} marginBottom={2} borderRadius={2}>
            <Typography component={Link} to={`/Collection/${collection.collectionID}`} variant="h5" fontWeight={600} fontFamily={'Roboto'} state={{isSelf: props.isSelf}} style={{ textDecoration: 'none', color: '#102C45' }}>{collection.collectionName} &#40;{collection.numBooks} books&#41;</Typography>
            <Grid container direction="row" justifyContent="center" paddingTop={2} spacing={2}>
              {collection.books.map((book, i) => <RecentlyAdded book={book}/>)}
            </Grid> 
          </Grid>
        )}
      </Grid> 
    </>
  )
}

export default CollectionCard