import React, { useState } from "react";
import { Toolbar, FormControl, InputLabel, Select, AppBar, Paper, Grid } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import { withStyles, Button, Menu, MenuItem, MuiThemeProvider } from "@material-ui/core";
import HeaderStyles from "../../styles/HeaderStyles";
import { DatasetItems } from "../../../configs/DatasetItems";
import Statistics from "./Statistics";
import Theme from "../../theme/theme-default";

const TitleBar = (props) => {
    const { classes, options, selectedOption,handleSelectChange, page, count } = props;
    // const [options, setOptions] = useState('parallel-corpus');
    console.log(selectedOption)
    const gridArray = [{ title: 'Title1', value: '35555' }, { title: 'Title2', value: '4000' }]

    const handleChange = (event) => {
        const obj = {};
        debugger
        obj.value = event.target.value;
        obj.label = options.reduce((acc,rem) => rem.value === event.target.value ? acc= rem.label : acc, "")
            debugger
        handleSelectChange(obj,"","",page) 
        debugger
    };
   
    return (
        <MuiThemeProvider theme={Theme}>
            <AppBar position="static" color="inherit" elevation={0} >
                <Toolbar className={classes.toolbar}>
                    <Grid container className={classes.toolGrid}>
                        < Grid item xs={3} sm={3} md={2} lg={2} xl={2} className={classes.selectGrid}>
                            <FormControl className={classes.formControl}>
                                <Select disableUnderline
                                    disabled = {page!==0 ? true : false}
                                    value={selectedOption.value}
                                    onChange={handleChange}
                                >
                                    {
                                        options.map(menu => {
                                            return <option
                                                value={menu.value}
                                                className={classes.styledMenu}
                                            >
                                                {menu.label}
                                            </option>
                                        })
                                    }
                                </Select>
                            </FormControl>
                        </Grid>
                        < Grid item xs={4} sm={4} md={2} lg={2} xl={2} className={classes.tempGrid}>
                        <Typography variant="body2" gutterBottom>
                            {/* {props.label} */}
                            Total Sentences Count
                        </Typography>
                        <Typography variant="body1">
                            {/* {props.totValue} */}
                            {count ? new Intl.NumberFormat('en').format(count) : 0}
                        </Typography>
                    </Grid>
                        <Grid item xs={0} sm={0} md={3} lg={3} xl={3}></Grid>
                        <Grid item xs={5} sm={5} md={5} lg={5} xl={5}>
                            <Grid container spacing={2}>
                               {props.children}
                            </Grid>
                        </Grid>
                    </Grid>
                </Toolbar>  
            </AppBar>
            {/* <Statistics label='Total parallel sentences' totValue='53645447'>
                 {
                    gridArray.map(grid => {
                        return (
                            <Grid item>
                                <Typography gutterBottom>{grid.title}</Typography>
                                <Typography variant="h6" component="h5">{grid.value}</Typography>
                            </Grid>
                        )
                    })
                <Grid item>
                    <Typography gutterBottom variant='body2'> Title Here</Typography>
                    <Typography variant="body1">29875</Typography>
                </Grid>
                 <Grid item>
                    <Typography gutterBottom variant='body2'> Title Here</Typography>
                    <Typography variant="h6" component='h5'>46786</Typography>
                </Grid>
                <Grid item>
                    <Typography gutterBottom variant='body2'> Title Here</Typography>
                    <Typography variant="h6" component='h5'>56676</Typography>
                </Grid> 
            </Statistics> */}
            </MuiThemeProvider>
    )
}

export default withStyles(HeaderStyles)(TitleBar);