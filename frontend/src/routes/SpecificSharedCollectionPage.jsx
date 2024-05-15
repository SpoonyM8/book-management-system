import React, { useState, useEffect } from 'react'
import { Button, Grid, Typography } from '@mui/material';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import BookShared from '../components/BookShared';
import jwt_decode from 'jwt-decode';

const SpecificSharedCollectionPage = () => {
  const [books, setBooks] = useState([]);
  const [collectionName, setCollectionName] = useState("");
  const [owner, setOwner] = useState(false);
  const [member, setMember] = useState(false);
  const [fetchBooks, setFetchBooks] = useState(true)
  const collectionId = useParams();
  const navigate = useNavigate();
  const username = jwt_decode(sessionStorage.getItem("token")).sub

  const options = {
    method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.token}`
    },
  };

  useEffect(() => {
    fetch(`http://localhost:5000/sharedCollection/${collectionId.id}/details`, options)
    .then((response) => response.json())
    .then((responseJson) => {
      setBooks(responseJson.books)
      setCollectionName(responseJson.collectionName)
      setOwner(username == responseJson.owner)
      setFetchBooks(true)
    });
  }, [fetchBooks]);

  useEffect(() => {
    fetch(`http://localhost:5000/sharedCollection/${collectionId.id}/is_member/${username}`, options)
      .then((response) => response.json())
      .then((responseJson) => {
        setMember(responseJson["is_member"])
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
    fetch(`http://localhost:5000/sharedCollection/delete/${collectionId.id}`, opt)
    .then((response) => response.json())
    .then((responseJson) => {
    });
    navigate("/home");
  }

  const handleLeave = () => {
    const opt = {
      method: "DELETE",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionStorage.token}`
      },
    };
    fetch(`http://localhost:5000/sharedCollection/leave/${collectionId.id}`, opt)
    .then((response) => response.json())
    .then((responseJson) => {
    });
    navigate("/sharedCollections");
  }

  const handleJoin = () => {
    const opt = {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionStorage.token}`
      },
    };
    fetch(`http://localhost:5000/sharedCollection/join/${collectionId.id}`, opt)
    .then((response) => response.json())
    .then(() => {
      setMember(true)
    });
  }

  return (
    <>    
      <Grid container display={'flex'} width={'100%'}>
        <Grid item xs={12} display="flex" justifyContent="center">
          <Typography variant="h3" noWrap margin={1}>{collectionName}</Typography>
        </Grid>
        <Grid item xs={12} display="flex" justifyContent="center">
          {(owner)?<Button onClick={handleDelete} variant="outlined" noWrap margin={1}>Delete the collection</Button>:<></>}
          {(member & !owner)?<Button onClick={handleLeave} variant="outlined" noWrap margin={1}>Leave the collection</Button>:<></>}
          {(!member)?<Button onClick={handleJoin} variant="outlined" noWrap margin={1}>Join the collection</Button>:<></>}
        </Grid>

        <Grid item xs={12} width={'100%'}>
          <Grid 
            container 
            width={'100%'} 
            display={'flex'}
            flexDirection={'row'}
            justifyContent={'center'}
            margin={3}
            >
            {(books.length == 0) ? <Typography variant="h6" noWrap margin={1}>There are no books in the collection</Typography>:<></>}
            {books.map((book,i) => <BookShared shouldFetch={fetchBooks} setShouldFetch={setFetchBooks} details={book}/>)}
          </Grid>
        </Grid>
      </Grid>
    </>

  )
}
export default SpecificSharedCollectionPage