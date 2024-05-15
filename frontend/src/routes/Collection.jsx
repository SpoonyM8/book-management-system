import React, { useState, useEffect } from 'react'
import Book from '../components/Book'
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { Button, Grid, Typography } from '@mui/material'
import jwt_decode from 'jwt-decode'

const Collection = () => {

  const [books, setBooks] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const collectionId = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const username = jwt_decode(sessionStorage.getItem("token")).sub
  const [fetchBooks, setFetchBooks] = useState(true)

  const options = {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.token}`
    },
  };

  useEffect(() => {
    fetch(`http://localhost:5000/collections/${collectionId.id}`, options)
    .then((response) => response.json())
    .then((responseJson) => {
      setBooks(responseJson.books)
      setFetchBooks(true)
    });
  }, [fetchBooks]);

  // to get collection name
  useEffect(() => {
    fetch(`http://localhost:5000/collections/user/${username}`, options)
    .then((response) => response.json())
    .then((responseJson) => {
      setCollectionName(responseJson.collections.filter(c => c.collectionID === collectionId.id)[0]['collectionName'])
    });
  }, []);

  const handleDelete = () => {
    const opt = {
      method: "DELETE",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionStorage.token}`
      },
    };
    fetch(`http://localhost:5000/collections/delete/${collectionId.id}`, opt)
    .then((response) => response.json())
    .then((responseJson) => {
    });
    navigate("/home");
  }

  return (
    <>    
      <Grid container display={'flex'} width={'100%'}>
        <Grid item xs={12} display="flex" justifyContent="center">
          <Typography variant="h3" noWrap margin={1}>{collectionName}</Typography>
        </Grid>
        <Grid item xs={12} display="flex" justifyContent="center">
          {collectionName !== 'main' &&
            <Button onClick={handleDelete} variant="outlined" noWrap margin={1}>
              Delete the collection
            </Button>
          }
        </Grid>

        <Grid item width={'100%'}>
          <Grid 
            container 
            width={'100%'} 
            display={'flex'}
            flexDirection={'row'}
            justifyContent={'center'}
            alignContent={'center'}
            paddingLeft={5}
            >
            {(books.length == 0) ? <Typography variant="h6" color={'#102C45'} fontFamily={'Roboto'} noWrap margin={1}>There are no books in the collection</Typography>:<></>}
            {books.map((book,i) => <Book shouldFetch={fetchBooks} setShouldFetch={setFetchBooks} isSelf={location.state.isSelf} details={book}/>)}
          </Grid>
        </Grid>
      </Grid>

    </>

  )
}

export default Collection