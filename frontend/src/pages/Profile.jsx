import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { useParams, useLocation } from "react-router-dom";
import jwt_decode from 'jwt-decode';
import { Grid, Card, Button, Typography, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import Collections from "../components/Collections";

const Profile = () => {
  const { username } = useParams();
  const [followersList, setFollowersList] = useState([]);
  const [followingsList, setFollowingsList] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [isSelf, setIsSelf] = useState(false);
  const [fetchCollections, setFetchCollections] = useState(true);

  const navigate = useNavigate();
  const location = useLocation(); // Otherwise the set following/followers lists still show up when u go to another users profile

  const token = sessionStorage.getItem("token")
 // we won't want the follow user button if self, and we wont want the create collection buttons if not self etc
  useEffect(() => {
    fetch(`http://localhost:5000/users/followers/${username}`, {method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }})
    .then((response) => response.json())
    .then((responseJson) => {
      setIsSelf(jwt_decode(token).sub == username);
      setFollowersList(responseJson.followers)
    });
  }, [location, isFollowing]);

  useEffect(() => {
    setFetchCollections(true);
  }, [location]);

  useEffect(() => {
    fetch(`http://localhost:5000/users/following/${username}`, {method: "GET",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }})
    .then((response) => response.json())
    .then((responseJson) => {
      setFollowingsList(responseJson.following)
    });
  }, [location]);


  useEffect(() => {
    if (!isSelf) {
      fetch(`http://localhost:5000/users/followers/${username}`, {method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }})
      .then((response) => response.json())
      .then((responseJson) => {
        setIsFollowing(responseJson.followers.some(user => user == jwt_decode(token).sub))
      });
    }
  }, [location, isSelf]);

  const followUser = () => {
    fetch(`http://localhost:5000/users/follow/${username}`, {method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }})
    .then((response) => response.json())
    .then(() => 
      setIsFollowing(true)
    );
  }

  const unfollowUser = () => {
    fetch(`http://localhost:5000/users/unfollow/${username}`, {method: "DELETE",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }})
    .then((response) => response.json())
    .then(() => {
      setIsFollowing(false)
    });
  }



  return (
    <>
      <Grid container direction="column" alignItems="center" justifyContent="center">
        <Card style={{ border: "none", boxShadow: "none" }} sx={{minWidth: 300, marginBottom: 5}}>
          <Grid container spacing={0} direction="column" alignItems="center" justifyContent="center">
            <AccountCircleIcon style={{fontSize: 100}}/>
            <Typography variant="h5" fontFamily={'Roboto'} fontWeight={700}>
              {isSelf ? 'Your profile' : `${username}s profile`}
            </Typography>
            {
              !isFollowing && !isSelf && <Button onClick={() => followUser()}>FOLLOW</Button>
             }
            {
              isFollowing && !isSelf &&<Button onClick={() => unfollowUser()}>UNFOLLOW</Button>
            }
          </Grid>
        </Card>
        <Grid sx={{width: '95%'}}item margin={2}>
          <Collections fetchCollections={fetchCollections} setFetchCollections={setFetchCollections} isSelf={isSelf} username={username}/>
        </Grid>
        <Grid container spacing={5} direction="row" justifyContent="center" sx={{marginTop: 1}}>
          <Grid item>
            <List>
              <ListItem>
                <Typography variant="h6" fontFamily={'Roboto'} fontWeight={700}>{isSelf ? 'Users that follow you' : `Users that follow ${username}`}</Typography>
              </ListItem>
              {followersList && followersList.map(user => (
              <ListItem>
              <ListItemButton>
                <ListItemIcon>
                  <AccountCircleIcon/>
                </ListItemIcon>
                <ListItemText id={user} primary={user} onClick={() => navigate(`/profile/${user}`)}/>
              </ListItemButton>
            </ListItem>
            ))}
            </List>
          </Grid>
          <Grid item>
            <List>
              <ListItem>
                <Typography variant="h6" fontFamily={'Roboto'} fontWeight={700}>{isSelf ? 'Users that you follow': `Users that ${username} follows`}</Typography>
              </ListItem>
              {followingsList && followingsList.map(user => (
              <ListItem>
              <ListItemButton>
                <ListItemIcon>
                  <AccountCircleIcon/>
                </ListItemIcon>
                <ListItemText id={user} primary={user} onClick={() => navigate(`/profile/${user}`)}/>
              </ListItemButton>
            </ListItem>
            ))}
            </List>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}

export default Profile;