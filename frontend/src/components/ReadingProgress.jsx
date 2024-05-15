import React from 'react'
import { Grid, Typography } from '@mui/material'

const ReadingProgress = () => {
  return (
    <>
        <Grid 
            container             
            justifyContent="center"
            alignItems="stretch"
            margin={1}
        >
            <Typography variant="h4" fontWeight={700} color={'#102C45'} fontFamily={'Roboto'}>Welcome to BMS!</Typography>
        </Grid>
    </>
  )
}

export default ReadingProgress