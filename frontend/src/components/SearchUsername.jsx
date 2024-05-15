import React, { useEffect, useState } from 'react';
import { Grid, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Stack } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useNavigate } from 'react-router-dom';

const SearchUsername = (props) => {
  const [users, setUsers] = useState([])
  const navigate = useNavigate();

  const getBody = () => {
    let data = {}
    if (props.username) {
      data['username'] = props.username;
    }
    return data;
  }

  useEffect(() => {
    if (props.shouldFetch) {
      fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem("token")}`
        },
        body: JSON.stringify(getBody())
      })
        .then(res => res.json())
        .then(data => {
          if (data.code && data.code != 200) {
            props.setError(true)
            props.setShouldFetch(false);
          } else {
            props.setShouldFetch(false);
            setUsers(data)
          }
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
    style={{ minHeight: '100vh', maxWidth: '60vw', marginLeft: '20vw', marginRight: '20vw' }}
  >
    <Stack justifyContent="center" alignItems="center" spacing={2} sx={{ width: 600, marginTop: 5 }}>
        {props.error ? <div>No Users matched your request </div> :
        <List>
          <ListItem>Click on a username in the list to view more information about the user</ListItem>
          {users && users.map(user => (
          <ListItem>
          <ListItemButton>
            <ListItemIcon>
              <AccountCircleIcon/>
            </ListItemIcon>
            <ListItemText id={user.username} primary={user.username} onClick={() => navigate(`/profile/${user.username}`)}/>
          </ListItemButton>
        </ListItem>
        ))}

        </List>
        }
        </Stack>
      </Grid>
  );
}

export default SearchUsername;