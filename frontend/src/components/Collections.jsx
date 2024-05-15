import React, { useEffect, useState } from 'react'
import { Grid, Typography, TextField, Dialog, DialogActions, DialogContent, DialogTitle, Checkbox, FormGroup, FormControlLabel } from '@mui/material'
import LibraryAddIcon from '@mui/icons-material/LibraryAdd';
import Button from '@mui/material/Button';
import CollectionCard from './CollectionCard';
import SharedCollectionCard from './SharedCollectionCard';

const Collections = (props) => {

  const [open, setOpen] = useState(false);
  const [openShared, setOpenShared] = useState(false);
  const [name, setName] = useState("");
  const [fetchCollections, setFetchCollections] = useState(true)

  const dataa = {
    username: props.username,
    collectionName: name,
  };
  const options = {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${sessionStorage.token}`
    },
    body: JSON.stringify(dataa),
  };

  const handleSubmit = () => {
    fetch(`http://localhost:5000/collections/create/${name}`, options)
      .then((response) => response.json())
      .then(() => {
        setFetchCollections(true)
    });
    setOpen(false)
  }

  const handleSubmitShared = () => {
    fetch(`http://localhost:5000/sharedCollection/create/${name}`, options)
      .then((response) => response.json())
      .then(() => {
        setFetchCollections(true)
    })
    setOpenShared(false)
  }


  return (
    <>
      <Grid container spacing={0} direction="column" alignItems="center" justify="center" marginBottom={0.5}>
        <Grid item>
          <Typography variant='h5' align='left' fontWeight={600} color={'#102C45'} fontFamily={'Roboto'}> {props.isSelf ? 'My collections' : `${props.username}'s collections`} </Typography>
        </Grid>
        <Grid item>
          {props.isSelf && <Button size='large' onClick={() => setOpen(true)} startIcon={<LibraryAddIcon />}>Create A New Collection</Button> }
        </Grid>
      </Grid>
      <CollectionCard shouldFetch={props.fetchCollections ? props.fetchCollections : fetchCollections} setShouldFetch={props.setFetchCollections ? props.setFetchCollections : setFetchCollections} username={props.username} isSelf={props.isSelf}/>
      
      <Grid container spacing={0} direction="column" alignItems="center" justify="center" marginTop={2} marginBottom={0.5}>
        <Grid item>
          <Typography variant='h5' align='left' fontWeight={600} color={'#102C45'} fontFamily={'Roboto'}> {props.isSelf ? 'My shared collections' : `${props.username}'s shared collections`} </Typography>
        </Grid>
        <Grid item>
          {props.isSelf && <Button size='large' onClick={() => setOpenShared(true)} startIcon={<LibraryAddIcon />}>Create A New Shared Collection</Button> }
        </Grid>
      </Grid>
      <SharedCollectionCard shouldFetch={fetchCollections} setShouldFetch={setFetchCollections} username={props.username} isSelf={props.isSelf}/>

      <Dialog open={open} onClose={() => setOpen(false)} fullWidth={false}>
        <DialogTitle>New collection</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            name='name'
            margin="dense"
            id="collection_name"
            label="Collection Name"
            type="text"
            variant="standard"
            onBlur={(e) => {setName(e.target.value)}}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSubmit}>Create New Collection</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openShared} onClose={() => setOpenShared(false)} fullWidth={false}>
        <DialogTitle>New Shared collection</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            name='name'
            margin="dense"
            id="collection_name"
            label="Shared Collection Name"
            type="text"
            variant="standard"
            onBlur={(e) => {setName(e.target.value)}}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSubmitShared}>Create New Shared Collection</Button>
        </DialogActions>
      </Dialog>


    </>
  )
}

export default Collections