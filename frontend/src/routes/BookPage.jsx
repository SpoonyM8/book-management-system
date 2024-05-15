import React, { useEffect, useState } from 'react'
import { Button, CardMedia, Box, FormControl, InputLabel, Select, setRef } from '@mui/material';
import { Grid, Typography, TextField, Dialog, DialogActions, DialogContent, DialogTitle, Checkbox, FormGroup, FormControlLabel, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material'
import { useParams } from 'react-router-dom';
import jwt_decode from 'jwt-decode'
import RecommendedBook from '../components/RecommendedBook';
import Rating from '@mui/material/Rating';
import './BookPage.css';
import { useNavigate } from 'react-router-dom';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

const BookPage = () => {

  const [details, setDetails] = useState({});
  const [ratings, setRatings] = useState({});
  const [reviews, setReviews] = useState({});
  const [collections, setCollections] = useState([]);
  const [sharedCollections, setSharedCollections] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [collectionId, setCollectionId] = useState("");
  const [open, setOpen] = useState(false);
  const [openRecommend, setOpenRecommend] = useState(false);
  const { id: bookId} = useParams();
  const [shared, setShared] = useState(false);
  const username = jwt_decode(sessionStorage.getItem("token")).sub
  const [preferences, setPreferences] = useState({ 'follows': false, 'genre': false, 'similar': false }) 
  const [showRecommendations, setShowRecommendations] = useState(false)
  const [alreadyReviewed, setAlreadyReviewed] = useState(false);
  const [openAddReview, setOpenAddReview] = useState(false);
  const [refresh, setRefresh] = useState(false);
  const [ratingWarning, setRatingWarning] = useState(false);
  const [notRead, setNotRead] = useState(false);
  const [alreadyAdded, setAlreadyAdded] = useState(false);

  const navigate = useNavigate();


  const HandleClickOpen = () => {
    setOpen(true);
    const options = {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionStorage.token}`
      },
    };
    fetch(`http://localhost:5000/collections/user/${username}`, options)
    .then((response) => response.json())
    .then((responseJson) => {
      setCollections(responseJson.collections)
    });
    fetch(`http://localhost:5000/sharedCollection`, options)
    .then((response) => response.json())
    .then((responseJson) => {
      setSharedCollections(responseJson.collections)
    });
  };

  const collectionNames = collections.map(({collectionName})=> collectionName)
  const sharedCollectionNames = sharedCollections.map(({collectionName})=> collectionName)

  const handleClose = () => {
    setOpen(false);
  };

  const togglePreference = (e) => {   
    preferences[e.target.value] = !preferences[e.target.value]; 
    setPreferences(preferences)
  }

  const handleRecommendation = () => {
    const options = {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${sessionStorage.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(preferences)
    };

    fetch(`http://localhost:5000/recommend/${bookId}`, options)
      .then((response) => response.json())
      .then((responseJson) => {
        setRecommendations(responseJson.recommend)
        setShowRecommendations(true)
    });
    
    setPreferences({ 'follows': false, 'genre': false, 'similar': false })
    setOpenRecommend(false)
  }

  const handleChange = (e) => {
    var id = collections.filter(c => c.collectionName == e.target.value)
    const check = (id.length == 0)
    if (check) {
      setShared(true)
      id = sharedCollections.filter(c => c.collectionName == e.target.value)
    } else {
      setShared(false)
    }
    setCollectionId(id[0]['collectionID'])
  };
  
  const addBook = () => {
    
    const options = {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${sessionStorage.token}`
      }
    };
    if(!shared){
      fetch(`http://localhost:5000/collections/${collectionId ? collectionId : collections.filter(c => c.collectionName == 'main')[0]['collectionID']}/add/${bookId}`, options)
        .then((response) => response.json())
        .then((responseJson) => {
          if (responseJson.code && responseJson.code != 200) {
            setAlreadyAdded(true);
          }
          setRefresh(true);
      });
    } else {
      fetch(`http://localhost:5000/sharedCollection/${collectionId ? collectionId : collections.filter(c => c.collectionName == 'main')[0]['collectionID']}/add/${bookId}`, options)
        .then((response) => response.json())
        .then((responseJson) => {
          if (responseJson.code && responseJson.code != 200) {
            setAlreadyAdded(true);
          }
          setRefresh(true);
      });
    }
    handleClose()
  };

  useEffect(() => {
    const options = {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${sessionStorage.token}`
      }
    };
    
    fetch(`http://localhost:5000/books/${bookId}`, options)
      .then((response) => response.json())
      .then((responseJson) => {
        setDetails(responseJson)
        setShowRecommendations(false)
        setRefresh(false);
    });
  }, [bookId, refresh]);

  const handleSubmit = (event) => {
    event.preventDefault();

    let review = event.target.review.value;
    let rating = event.target.rating.value;
    
    if (rating === '') {
      setRatingWarning(true);
    } else {
      add_review(review, rating);
    }
};

const deleteReview = () => {
  const requestOptions = {
    method: "DELETE",
    headers: { "Content-Type": "application/json",
    'Authorization': `Bearer ${sessionStorage.token}`
    },
  }

  fetch(`http://localhost:5000/books/${bookId}/review/delete`, requestOptions)
    .then(res => res.json())
    .then(() => setRefresh(true))
};

  const add_review = (review, rating) => {
    const data = {
      comment: review,
      rating: rating,
    };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json",
        'Authorization': `Bearer ${sessionStorage.token}`
     },
      body: JSON.stringify(data),
    };

    fetch(`http://localhost:5000/books/${bookId}/review/add`, requestOptions)
        .then((response) => response.json())
        .then((data) => {
          if (data && data.code  && data.code != 200) {
            if (data.message == 'user must read book before reviewing') {
              setNotRead(true);
            } else {
              setAlreadyReviewed(true);
            }
          } else {
            setNotRead(false);
            setAlreadyReviewed(false);
            setRefresh(true);
            setOpenAddReview(false);
          }
        });
    }

  return (
    <>
      <Grid container display={'flex'} flexDirection={'row'} justifyContent={'center'} alignItems={'center'} margin={5}>
        <Grid item display={'flex'} flexDirection={'column'} alignItems={'flex-end'} justifyContent={'flex-end'}  marginRight={7}>
          <CardMedia
            component="img"
            image={details.coverImage}
            alt="book image"
            sx={{ objectFit: "contain" }}
            height="500"
          />
        </Grid>
        <Grid item>
          <Grid display={'flex'} flexDirection="column">
            <Grid >
              <Typography variant="h4" style={{  wordWrap: "break-word"}}>
                {details.title}
              </Typography>
              <Typography variant="h6">
                Author: {details.author}
              </Typography>
              <Typography variant="h6">
                Publisher: {details.publisher}
              </Typography>
              <Typography variant="h6">
                Year Published: {details.yearPublished}
              </Typography>
              <Typography variant="h6">
                Genre: {details.genre}
              </Typography>
              <Typography variant="h6">
                Number of readers: {details.numRead} 
              </Typography>
              <Typography variant="h6">
                Average Rating:
                <Rating
                    className="current-rating" 
                    name="current rating"
                    value = {details.averageRating ? details.averageRating : 0}
                    readOnly
                />
              </Typography>
            </Grid>
            <Grid marginTop={14}>
              <Grid item>
                <Button onClick={HandleClickOpen} size="large">ADD TO COLLECTION</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => setOpenAddReview(true)} size="large">ADD A REVIEW</Button>
              </Grid>
              <Grid item>
                <Button onClick={() => setOpenRecommend(true)} size="large">RECOMMEND ME A BOOK!</Button>
              </Grid>
            </Grid>

          </Grid>
        </Grid>
        {(showRecommendations) ?
        <Grid item xs={9} marginTop={5} border={'1px solid #F1F5F8'} borderRadius={5} style={{ backgroundColor: '#F1F5F8' }}>
          <Typography variant='h5' align='center' fontWeight={700} marginTop={2} marginBottom={2}> BOOK RECOMMENDATIONS </Typography>
          <Grid item display={'flex'} flexDirection={'row'} justifyContent={'space-evenly'} marginBottom={2} >
            {recommendations.map((book, i) => <RecommendedBook details={book}/>)}
          </Grid>
        </Grid>
        :<></>}
                <Grid item xs={12} marginTop={5}>
          <Typography variant='h5' align='center' fontWeight={700} marginTop={2} marginBottom={2}> Reviews </Typography>
          <Grid item display={'flex'} flexDirection={'row'} justifyContent={'center'} align='center'>
          <TableContainer component={Paper} sx={{ minWidth: 400, maxWidth: 1000 }}>
      <Table style={{ tableLayout: 'fixed' }}  size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell><Typography variant='subtitle1' fontWeight={700}>Username</Typography></TableCell>
            <TableCell><Typography variant='subtitle1' fontWeight={700}>Rating</Typography></TableCell>
            <TableCell><Typography variant='subtitle1' fontWeight={700}>Comment</Typography></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {details.reviews && JSON.parse(details.reviews).map((review) => (
            <TableRow
              key={review.username}
            >
              <TableCell component="th" scope="row" onClick={() => navigate(`/profile/${review.username}`)}>
              <AccountCircleIcon/>
                {' ' + review.username}
              </TableCell>
              <TableCell component="th" scope="row">
                <Rating
                    value = {review.rating}
                    readOnly
                />
              </TableCell>
              <TableCell component="th" scope="row" style={{ whiteSpace: "normal", wordWrap: "break-word"}}>
                <Typography>
                  {review.comment}
                </Typography>
                {username === review.username && <Button onClick={deleteReview}>Delete your review?</Button>}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>

          </Grid>
        </Grid>
      </Grid>
      
      <Dialog open={openAddReview} onClose={() => setOpenAddReview(false)} fullWidth={false}>
        <Grid item xs={7} className="comment-container">
          <Typography sx={{ fontWeight: 'bold' }}><center>Add a review</center> </Typography>
          <form onSubmit={handleSubmit} className="review-form">
          <TextField name="review" placeholder="Type here..." />
          <div className="add-rating-container">
          <Typography sx={{ fontWeight: 'bold' }} component="span">Rating: </Typography>
              <Rating
                  className="add-rating"
                  name="rating"
              />
          </div>
          
          <Button type="submit" variant="contained" className="save-button">Save</Button>
          </form>
      </Grid>
      </Dialog>

      <Dialog open={open} onClose={handleClose} fullWidth={false}>
        <DialogTitle>Collection:</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ display: 'flex', flexWrap: 'wrap' }}>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
              <InputLabel htmlFor="grouped-native-select">Collections</InputLabel>
              <Select native defaultValue="" id="grouped-native-select" label="Collections" onChange={handleChange}>
                <option aria-label="None" value="" />
                <optgroup label="Personal Collections">
                  {collectionNames.map((name) => (
                    <option key={name} value={name}>{name}</option>
                  ))}
                </optgroup>
                <optgroup label="Shared Collections">
                  {sharedCollectionNames.map((name) => (
                    <option key={name} value={name}>{name}</option>
                  ))}
                </optgroup>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={addBook}>Add book to Collection</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openRecommend} onClose={() => setOpenRecommend(false)} fullWidth={false}>
        <DialogTitle>Recommendation Criteria:</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ display: 'flex', flexWrap: 'wrap' }}>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
              <FormControlLabel control={<Checkbox/>} onChange={togglePreference} value="follows" label="Follows"/>
              <FormControlLabel control={<Checkbox/>} onChange={togglePreference} value="genre" label="Genre"/>
              <FormControlLabel control={<Checkbox/>} onChange={togglePreference} value="similar" label="Similar"/> 
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleRecommendation}>Recommend me a book!</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={alreadyReviewed} onClose={() => {
        setOpenAddReview(false);
        setAlreadyReviewed(false);}} fullWidth={false}>
        <DialogTitle>
          You have already reviewed this book! Please delete your previous review if you would like to review again.
        </DialogTitle>
      </Dialog>

      <Dialog open={ratingWarning} onClose={() => setRatingWarning(false)} fullWidth={false}>
        <DialogTitle>
          Please provide a rating in your review. Comments are not required, but a rating is.
        </DialogTitle>
      </Dialog>

      <Dialog open={notRead} onClose={() => {
        setOpenAddReview(false);
        setNotRead(false);
      }} fullWidth={false}>
        <DialogTitle>
          Please read the book (by adding it to a collection) before reviewing.
        </DialogTitle>
      </Dialog>

      <Dialog open={alreadyAdded} onClose={() => setAlreadyAdded(false)} fullWidth={false}>
        <DialogTitle>
          This book already exists in the specified collection.
        </DialogTitle>
      </Dialog>
    </>
  )
}

export default BookPage