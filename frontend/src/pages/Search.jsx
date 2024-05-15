import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Grid, Typography, Button, Radio, RadioGroup, FormLabel, FormControlLabel, FormControl, TextField, Stack } from '@mui/material';
import SearchBook from '../components/SearchBook';
import SearchUsername from '../components/SearchUsername'

const Search = () => {
  const [showBooks, setShowBooks] = useState(false);
  const [showPeople, setShowPeople] = useState(false);
  const [bookName, setBookName] = useState('');
  const [authorName, setAuthorName] = useState('');
  const [personName, setPersonName] = useState('');
  const [showPeopleResults, setShowPeopleResults] = useState(false);
  const [showBookResults, setShowBookResults] = useState(false);
  const [shouldFetch, setShouldFetch] = useState(false);
  const [error, setError] = useState(false);

  const location = useLocation();

  const bookSearchHandler = () => {
    setError(false);
    setShowPeopleResults(false);
    setShowBookResults(true);
    setShouldFetch(true);
  }

  const peopleSearchHandler = () => {
    setError(false);
    setShowBookResults(false);
    setShowPeopleResults(true);
    setShouldFetch(true);
  }

  const clearPeopleStates = () => {
    setShowPeople(false);
    setShowPeopleResults(false);
    setPersonName('');
    setShowBooks(true);
  }

  const clearBookStates = () => {
    setShowBooks(false);
    setShowBookResults(false);
    setAuthorName('');
    setBookName('');
    setShowPeople(true);
  }

  useEffect(() => {
    // This stops previous search results from still showing up when the search tab is exited
    // and re-entered
    setShowPeopleResults(false);
    setShowBookResults(false);
  }, [location])

  return (
    <Grid
    container
    spacing={0}
    direction="column"
    alignItems="center"
    justifyContent="vertical"
    style={{ minHeight: '100vh' }}
  >
  <Grid>
    <FormControl>
      <FormLabel sx={{ marginTop: 3 }}>Would you like to search for Books or other people?</FormLabel>
      <RadioGroup
      sx={{ marginLeft: 11}}
        row
      >
        <FormControlLabel onClick={() => {
          clearPeopleStates();
        }} value="books" control={<Radio />} label="Books" />
        <FormControlLabel onClick={() => {
          clearBookStates();
        }} value="people" control={<Radio />} label="People" />
      </RadioGroup>
    </FormControl>
  </Grid>
  {showBooks && <Stack spacing={2} sx={{ width: 600, marginTop: 5 }}>
                  <Typography component="div">
                    Please enter one or both of the fields and submit your search
                  </Typography>
                  <TextField
                    label="Book name"
                    type="search"
                    variant="standard"
                    onChange={(e) => {
                      setBookName(e.target.value)
                    }}
                    inputProps={{ maxLength: 50}} // as per db schema
                  />
                  <TextField
                    label="Author"
                    type="search"
                    variant="standard"
                    onChange={(e) => {
                      setAuthorName(e.target.value)
                    }}
                    inputProps={{ maxLength: 100}} // as per db schema
                  />
                  <Button disabled={!bookName && !authorName} onClick={() => bookSearchHandler()}>
                    Submit Search Query
                  </Button>
                </Stack>}
  {showPeople && <Stack spacing={2} sx={{ width: 500, marginTop: 5 }}>
                  <Typography component="div" variant='subititle1' fontFamily={'Roboto'}>
                    Please enter the username of the user you would like to search for
                  </Typography>

                  <TextField
                    label="Username"
                    type="search"
                    variant="standard"
                    onChange={(e) => {
                      setPersonName(e.target.value)
                    }}
                    inputProps={{ maxLength: 50}} // as per db schema
                  />
                  <Button disabled={!personName} onClick={() => peopleSearchHandler()}>
                    Submit Search Query
                  </Button>
                </Stack>}
  {showBookResults && <SearchBook title={bookName} author={authorName} shouldFetch={shouldFetch} setShouldFetch={setShouldFetch} error={error} setError={setError}/>}
  {showPeopleResults && <SearchUsername username={personName} shouldFetch={shouldFetch} setShouldFetch={setShouldFetch} error={error} setError={setError}/>}
</Grid> 


  );
}


export default Search;