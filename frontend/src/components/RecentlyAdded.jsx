import React from 'react'
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { CardMedia } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react'

const RecentlyAdded = (book) => {
  const navigate = useNavigate();
  const bookDetails = book.book
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

  return (
    <>
    {(windowSize[0] < 500) ? 
      <Grid item  xs={3}>
        <Card sx={{ height: "100%" }} onClick={() => navigate(`/book/${bookDetails[0]}`)}>
          <CardMedia  component="img" image={bookDetails[2]}/>
          <CardContent>
          <Typography textAlign={'center'} fontSize={8} fontFamily={'Roboto'} style={{ textDecoration: 'none', color:'black', wordWrap: "break-word" }}>{bookDetails[1]}</Typography>
          </CardContent>
        </Card>
      </Grid>
      :
      <>
      {(windowSize[0] < 1200) ? 
        <Grid item xs={2.4}>
          <Card sx={{ height: "100%" }} onClick={() => navigate(`/book/${bookDetails[0]}`)}>
            <CardMedia  component="img" image={bookDetails[2]}/>
            <CardContent>
            <Typography textAlign={'center'} fontSize={12} fontFamily={'Roboto'} style={{ textDecoration: 'none', color:'black', wordWrap: "break-word" }}>{bookDetails[1]}</Typography>
            </CardContent>
          </Card>
        </Grid>
        :
        <Grid item xs={1.2} >
        <Card sx={{ height: "100%" }} onClick={() => navigate(`/book/${bookDetails[0]}`)}>
          <CardMedia  component="img" image={bookDetails[2]}/>
          <CardContent>
          <Typography textAlign={'center'} fontSize={14} fontFamily={'Roboto'} style={{ textDecoration: 'none', color:'black', wordWrap: "break-word"  }}>{bookDetails[1]}</Typography>
          </CardContent>
        </Card>
      </Grid>
      }
      </>
    } 
    </>
  )
}

export default RecentlyAdded