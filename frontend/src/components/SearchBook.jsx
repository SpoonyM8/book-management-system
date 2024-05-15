import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Grid, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Stack, FormControlLabel, Checkbox, TextField, Typography, CircularProgress } from '@mui/material';
import BookIcon from '@mui/icons-material/Book';



const SearchBook = (props) => {
  const [books, setBooks] = useState([])
  const [shouldFilter, setShouldFilter] = useState(false);
  const [filter, setFilter] = useState(null);
  const [loading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const getBody = () => {
    let data = {}
    const title = props.title;
    const author = props.author;
    if (title) {
      data['title'] = title;
    }
    if (author) {
      data['author'] = author;
    }
    return data;
  }

  const toggleFilter = () => {
    setShouldFilter(!shouldFilter);
  }

  useEffect(() => {
    if (props.shouldFetch) {
      setIsLoading(true);
      fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem('token')}`
        },
        body: JSON.stringify(getBody())
      })
        .then(res => res.json())
        .then(data => {
          if (data.code  && data.code != 200) {
            props.setError(true);
            props.setShouldFetch(false);
          } else {
            props.setShouldFetch(false);
            props.setError(false);
            setBooks(data);
          }
          setIsLoading(false);
        })
    }
  }, [props.shouldFetch])

  return (
    <Grid
    container
    spacing={0}
    direction="column"
    alignItems="center"
    justifyContent="vertical"
    style={{ minHeight: '100vh' }}
  >
    <Stack spacing={2} sx={{ width: 600, marginTop: 5 }}>
        {props.error &&
        <div>No books matched your request</div>}
        {loading &&
            <Grid
            container
            spacing={0}
            direction="column"
            alignItems="center"
            justifyContent="vertical"
          >
          <CircularProgress/>
          </Grid>}
        {!props.error && !loading && 
        <List>
          <ListItem alignItems="center">
            <TextField
              label="Minimum Average Rating"
              type="number"
              variant="standard"
              onChange={(e) => {
                setFilter(e.target.value)
              }}
              inputProps={{ maxLength: 1, max: 5, min: 0}}
            />
            <FormControlLabel sx={{marginTop: 2}} control={<Checkbox disabled={filter === null} />} onChange={toggleFilter} value="shouldFilter" label="Filter By Average Rating" labelPlacement="start"/>
          </ListItem>
          <ListItem><Typography variant='body1' fontFamily={'Roboto'}>Click on a book in the list to view more information about the book</Typography></ListItem>
          {books && books.filter(book => shouldFilter ? Number(book.averageRating) >= filter : true).map(book => (
          <ListItem>
          <ListItemButton>
            <ListItemIcon>
              <BookIcon/>
            </ListItemIcon>
            <ListItemText id={book.bookId} primary={`Title: ${book.title}`} secondary={`Author: ${book.author}`} onClick={() => navigate(`/book/${book.bookId}`)}/>
          </ListItemButton>
        </ListItem>
        ))}
        </List>
        }
    </Stack>
    </Grid>
  );
}

export default SearchBook;