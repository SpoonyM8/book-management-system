import React from 'react'
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { ButtonBase, CardMedia } from '@mui/material';
import { useNavigate } from 'react-router-dom';


const RecommendedBook = (props) => {
    const details = props.details;
    const navigate = useNavigate();
    
    return (
      <>
        <Grid item xs={1.7}>
          <Card style={{ height: '100%', width: '200px' }} sx={{ 
            display: "flex",
            flexDirection: "column"}}>
            <ButtonBase>
            <CardMedia
              component="img"
              image={details['coverImage']}
              alt="book image"
              sx={{ objectFit: "contain" }}
              alignItems= 'center'
              justifyContent= 'center'
            />
            </ButtonBase>
            <CardContent>
              <Typography gutterBottom onClick={() => navigate(`/book/${details['bookID']}`)} variant="h6" color={"black"} sx={{ wordBreak: "break-word" }} style={{ textDecoration: 'none', color:'black' }}>
                {details['title']}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Authors: {details['author']}<br/>
              </Typography>
            </CardContent>
          </Card>
        </Grid>   
      </>
    )
}

export default RecommendedBook