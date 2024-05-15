import { Grid, Typography } from '@mui/material'
import React, { useEffect, useState } from 'react'
import Collections from './Collections'
import ReadingProgress from './ReadingProgress'
import Follow from './Follow'
import jwt_decode from 'jwt-decode';
import { useLocation } from "react-router-dom";
const Body = () => {
	const location = useLocation();
	const [currentGoal, setCurrentGoal] = useState(false)

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
					if (responseJson.goals.length !== 0) {
						setCurrentGoal(responseJson.goals)
					} else {
						setCurrentGoal(false);
					}
				});
	}	  

	useEffect(() => {
		getGoals();
	}, [location]);

  return (
    <>
        <Grid 
            container
            direction="row"
            justifyContent="center"
            alignItems="stretch"
            height={'100%'}
        >
            <Grid item p={2} xs={12}>
                <ReadingProgress/>
            </Grid>
						<Grid 
            container             
            justifyContent="center"
            alignItems="stretch"
						item p={2}
						xs={12}
						borderTop={'2px solid #284051'}
						borderBottom={'2px solid #284051'}
        >
					{
						currentGoal ?
						<>
						{
							currentGoal.filter(goal => goal.numMonth == (new Date()).getMonth() + 1 && goal.numYear == (new Date()).getFullYear()).map(goal => {
								return <Typography variant="h5" fontWeight={600} color={'#102C45'} fontFamily={'Roboto'}>Current goal progress: {goal.numRead}/{goal.numTarget} books read</Typography>
							})
						}	
						</>
						:
						<Typography variant="h5" fontWeight={500} color={'#102C45'} fontFamily={'Roboto'}>You don't have a goal set for this month. Head to the goal tab to set one!</Typography>
					}			
        </Grid>
            <Grid item p={2} xs={12} >
                <Collections username={jwt_decode(sessionStorage.getItem("token")).sub} isSelf={true}/>
            </Grid>

        </Grid>
    </>
  )
}

export default Body