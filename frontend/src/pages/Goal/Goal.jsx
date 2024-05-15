import {
    Card,
    CardContent,
    Typography,
    Grid,
    styled,
    TextField,
    Button,
    Snackbar,
  } from "@mui/material";
  import React from "react";
  import Navbar from "../../components/Navbar";
  import bookImage from './book.jpeg';
  import './Goal.css'
  import { DatePicker } from "@mui/x-date-pickers";
  import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
  import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
  import { useState } from "react";
  import dayjs, { Dayjs } from 'dayjs';
  import {Dialog, DialogTitle} from '@mui/material';

  function Goal() {
    const [snackbar, setSnackbar] = useState(null);
    const [target, setTarget] = useState(null);
    const [date, setDate] = useState(null);
    const handleClose = () => setSnackbar(null);
    const [startMinDate] = useState(dayjs(Date.now()))
    const [goals, setGoals] = useState(null);
    const [reviewSuccess, setReviewSuccess] = useState(false);

    const handleSetGoal = () => {
      if (!target) {
        setSnackbar("Please fill the number of books.");
        return;
      }
      if (!date) {
        setSnackbar("Please fill the goal date.");
        return;
      }
      const month = date.$M;
      const year = date.$y;
      const createGoal = (target, month, year) => {
        const data = {
            target: Number(target),
            month: month + 1,
            year: year,
        };
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json",
              'Authorization': `Bearer ${sessionStorage.token}`
           },
            body: JSON.stringify(data),
          };
      
          fetch(`http://localhost:5000/goals/create`, requestOptions)
              .then((response) => response.json())
              .then(() => setReviewSuccess(true));
        };
      createGoal(target, month, year)
    };
  
    const handleTarget = (e) => {
      setTarget(e.target.value);
    };
    const handleDate = (e, d) => {
      if (d.validationError) {
        setDate(null);
        return;
      }
      setDate(e);
    };

    const getGoals = () => {
        const requestOptions = {
          method: "GET",
          headers: { "Content-Type": "application/json",
            'Authorization': `Bearer ${sessionStorage.token}`
         }
        };
    
        fetch(`http://localhost:5000/goals`, requestOptions)
            .then((response) => response.json())
            .then((responseJson) => {
                setGoals(responseJson.goals)
            });
    }  

    return (
      <>
        <Navbar />
        <Grid container spacing={2}>
          <Grid item xs={3}></Grid>
          <Grid item xs={6}>
            <Item>
              <Typography variant="h4" p={2} textAlign="center">
                Set or update your reading goal
              </Typography>
  
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <img width={250} src={bookImage} alt="Books" />
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="h6">
                      I want to read this many books...
                    </Typography>
                    <Input
                      label="Set a number"
                      variant="outlined"
                      size="small"
                      margin="normal"
                      type="number"
                      onChange={handleTarget}
                    />
                    <Typography variant="h6">
                      In the month and year of...
                    </Typography>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <DatePicker
                        label="Set goal date"
                        views={["month", "year"]}
                        disablePast                  
                        minDate = {startMinDate}
                        slotProps={{
                          textField: {
                            size: "small",
                            margin: "normal",
                          },
                        }}
                        slots={{
                          textField: Input,
                        }}
                        onChange={handleDate}
                      />
                    </LocalizationProvider>
                    <ColorButton
                  variant="contained"
                  size="small"
                  onClick={handleSetGoal}
                  sx={{marginTop: 2}}
                >
                  Submit
                </ColorButton>
                  </Grid>
                </Grid>
              </CardContent>
              
            </Item>
          </Grid>
          <Grid item xs={3}></Grid>
          <Snackbar
            open={snackbar}
            autoHideDuration={6000}
            onClose={handleClose}
            message={snackbar}
          />
        </Grid>
        {/* Goal Timeline code*/ }
        <Grid container spacing={2}>
            <Grid item xs={3}></Grid>
            <Grid item xs={6}>
            <Item>
              <Typography variant="h4" p={2} textAlign="center">
                Review you goal timeline
              </Typography>
  
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <DatePicker
                        label="Select year"
                        views={["year"]}
                        slotProps={{
                          textField: {
                            size: "small",
                          },
                        }}
                        slots={{
                          textField: Input,
                        }}
                        onChange={handleDate}
                      />
                    </LocalizationProvider>
                    <ColorButton
                  variant="contained"
                  size="small"
                  sx={{marginTop: 0}}
                  onClick={getGoals}
                  width = "10%"
                >
                  Submit
                </ColorButton>
                  </Grid>
                  <Grid item xs={12}>
                  </Grid>
                </Grid>
                <Grid item>
                  
            </Grid>
            <Grid>
              {goals && goals.filter(goal => goal.numYear == date.$y).map((goal) => 
                <>
                <Grid container border= '4px solid grey' padding="10px" marginBottom="20px" >
                <Grid container spacing={0}
                    direction="column"
                    alignItems="center"
                    justifyContent="center"
                    style={{ minHeight: '50px' }}
                    >
                <strong><Typography variant="h5" style={{color: '#001F3C'}}> Goal Date: {goal.numMonth}/{goal.numYear}</Typography></strong>
                <Typography variant="h5">Reading Goal Progress: {goal.numRead}/{goal.numTarget}</Typography>
                </Grid>
                </Grid>
                </>
              )}
            </Grid>
            <Grid>
                
            </Grid>
            </CardContent> 
            </Item>
            </Grid>
            <Grid item xs={3}></Grid>
        </Grid>
        <Dialog open={reviewSuccess} onClose={() => setReviewSuccess(false)} fullWidth={false}>
        <DialogTitle>
                Successfully created/updated your goal.
        </DialogTitle>
        </Dialog>
      </>
    );
  }
  const Item = styled(Card)(({ theme }) => ({
    backgroundColor: theme.palette.grey[100],
    ...theme.typography.body2,
    margin: theme.spacing(4),
  }));
  const Input = styled(TextField)(({ theme }) => ({
    backgroundColor: theme.palette.background.paper,
  }));
  const ColorButton = styled(Button)(({ theme }) => ({
    paddingLeft: theme.spacing(10),
    paddingRight: theme.spacing(10),
    borderRadius: "10px",
    margin: "auto",
    marginBottom: theme.spacing(2),
    marginLeft: "30px",
    background: "rgb(0, 30, 60)",
    width: "10px",
  }));
  export default Goal;
  