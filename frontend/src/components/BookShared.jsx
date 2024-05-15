import React, { useState, useEffect } from 'react'
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { Box, ButtonBase, CardMedia, IconButton } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import DeleteIcon from '@mui/icons-material/Delete';

const BookShared = (props) => {
    const details = props.details
    const collectionId = useParams();
    const navigate = useNavigate();
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
  
    const removeBook = () => {
      const options = {
        method: "DELETE",
        headers: {
          'Authorization': `Bearer ${sessionStorage.token}`
        }
      };
      if (props.shouldFetch) {
        fetch(`http://localhost:5000/sharedCollection/${collectionId.id}/remove/${details['bookID']}`, options)
          .then((response) => response.json())
          .then((responseJson) => {
          props.setShouldFetch(false)
        });
      }
    };
  
    return (
      <>
      {(windowSize[0] < 600) ? 
        <Grid item xs={4} paddingTop={5}>
          <Card style={{ height: '100%', width: `${(windowSize[0]-100)/3}px` }} sx={{ 
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              boxShadow: 3
              }}>
              <Box onClick={() => navigate(`/book/${details[0]}`)}>
                <ButtonBase>
                <CardMedia
                  component="img"
                  image={details['coverImage']}
                  alt="book image"
                  sx={{ objectFit: "contain"}}
                  alignItems= 'center'
                  justifyContent= 'center'
                />
                </ButtonBase>
                <CardContent>
                  <Typography gutterBottom fontSize={9} fontWeight={700} component="div" color={"black"} fontFamily={'Roboto'} sx={{ wordBreak: "break-word" }}>
                    {details['title']}
                  </Typography>
                  <Typography fontSize={7} fontFamily={'Roboto'} color="text.secondary">
                    Authors: {details['author']}<br/>
                    Publisher: {details['publisher']}<br/>
                    Publication Date: {details['yearPublished']}<br/>
                    Category: {details['genre']}
                  </Typography>
                </CardContent>
              </Box>
              <CardActions>
                <IconButton color='primary' onClick={removeBook}><DeleteIcon /></IconButton>
              </CardActions>
            </Card>
          </Grid>   
        :
        <>
        {(windowSize[0] < 1920) ? 
        <Grid item xs={3} paddingTop={5}>
        <Card style={{ height: '100%', width: `${(windowSize[0]-200)/4}px` }} sx={{ 
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          boxShadow: 3
          }}>
          <Box onClick={() => navigate(`/book/${details[0]}`)}>
            <ButtonBase>
            <CardMedia
              component="img"
              image={details['coverImage']}
              alt="book image"
              sx={{ objectFit: "contain"}}
              alignItems= 'center'
              justifyContent= 'center'
            />
            </ButtonBase>
            <CardContent>
              <Typography gutterBottom fontSize={12} fontWeight={700} component="div" color={"black"} fontFamily={'Roboto'} sx={{ wordBreak: "break-word" }}>
                {details['title']}
              </Typography>
              <Typography fontSize={10} fontFamily={'Roboto'} color="text.secondary">
                Authors: {details['author']}<br/>
                Publisher: {details['publisher']}<br/>
                Publication Date: {details['yearPublished']}<br/>
                Category: {details['genre']}
              </Typography>
            </CardContent>
          </Box>
          <CardActions>
            <Button variant='outlined' color='primary' onClick={removeBook} size="small">REMOVE FROM COLLECTION</Button>
          </CardActions>
        </Card>
      </Grid>   
          :
          <Grid item xs={1.3} paddingTop={5}>
          <Card style={{ height: '100%', width: '190px' }} sx={{ 
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: 3
            }}>
            <Box onClick={() => navigate(`/book/${details[0]}`)}>
              <ButtonBase>
              <CardMedia
                component="img"
                image={details['coverImage']}
                alt="book image"
                sx={{ objectFit: "contain"}}
                alignItems= 'center'
                justifyContent= 'center'
              />
              </ButtonBase>
              <CardContent>
                <Typography gutterBottom variant="subtitle1" fontWeight={700} component="div" color={"black"} fontFamily={'Roboto'} sx={{ wordBreak: "break-word" }}>
                  {details['title']}
                </Typography>
                <Typography variant="subtitle2" fontFamily={'Roboto'} color="text.secondary">
                  Authors: {details['author']}<br/>
                  Publisher: {details['publisher']}<br/>
                  Publication Date: {details['yearPublished']}<br/>
                  Category: {details['genre']}
                </Typography>
              </CardContent>
            </Box>
            <CardActions>
              <Button variant='outlined' color='primary' onClick={removeBook} size="small">REMOVE FROM COLLECTION</Button>
            </CardActions>
          </Card>
        </Grid>   
        }  
        </>
      }
      </>
    )
}

export default BookShared