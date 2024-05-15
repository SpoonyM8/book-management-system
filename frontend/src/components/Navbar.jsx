import { Box, Typography, Grid } from '@mui/material'
import React, { useState, useEffect } from 'react'
import { useLocation, Link, NavLink, useNavigate } from 'react-router-dom'

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import MenuItem from "@mui/material/MenuItem";
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import Menu from "@mui/material/Menu";
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';
import MoreIcon from '@mui/icons-material/MoreVert';
import SearchIcon from '@mui/icons-material/Search';
import jwt_decode from 'jwt-decode'

const Navbar = () => {

  const navigate = useNavigate();

  const searchClickHandler = () => {
    navigate("/search");
  }

  const logoutClickHandler = () => {
    sessionStorage.removeItem("token");
    navigate("/login");
  }

  const profileClickHandler = () => {
    navigate(`/profile/${jwt_decode(sessionStorage.getItem("token")).sub}`)
  }

  const goalClickHandler = () => {
    navigate(`/goal`)
  }

  const sCollectionsClickHandler = () => {
    navigate(`/sharedCollections`)
  }

  const Actions = [
    { action: 'Shared Collections', icon: <LibraryBooksIcon/>, onClick: sCollectionsClickHandler},
    { action: 'Profile', icon: <AccountCircleIcon/>, onClick: profileClickHandler},
    { action: 'Goal', icon: <MenuBookIcon/>, onClick: goalClickHandler},
    { action: 'Search', icon: <SearchIcon/>, onClick: searchClickHandler},
    { action: 'Logout', icon: <LogoutIcon/>, onClick: logoutClickHandler},
  ]

  const [anchorEl, setAnchorEl] = React.useState(null);

  const isMenuOpen = Boolean(anchorEl);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const menuId = "navbar-menu";
  const renderMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{
        vertical: "top",
        horizontal: "right"
      }}
      id={menuId}
      keepMounted
      transformOrigin={{
        vertical: "top",
        horizontal: "right"
      }}
      open={isMenuOpen}
      onClose={handleMenuClose}
    >
      {Actions.map((action, i) => <MenuItem key={`action#${i}`}><Button key={`action#${i}`} startIcon={action.icon} onClick={() => action.onClick()}>{action.action}</Button></MenuItem>)}
    </Menu>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" style={{ background: '#001e3c' }}>
        <Toolbar>
          <Typography
            variant="h6"
            noWrap
            component={NavLink}
            sx={{ display: { xs: "block", sm: "block" }, textDecoration: "none", color: "white" }}
            to="/home"
          >
            READPACT
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Box sx={{ display: { xs: "none", md: "flex" } }}>
            <ButtonGroup variant="string">
              {Actions.map((action, i) => <Button key={`action#${i}`} startIcon={action.icon} onClick={() => action.onClick()}>{action.action}</Button> )}
            </ButtonGroup>
          </Box>
          <Box sx={{ display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="show more"
              aria-controls={menuId}
              aria-haspopup="true"
              onClick={handleMenuOpen}
              color="inherit"
            >
              <MoreIcon />
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>
      {renderMenu}
    </Box>
  );
}

export default Navbar