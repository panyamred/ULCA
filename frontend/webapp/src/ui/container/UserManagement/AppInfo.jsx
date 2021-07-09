import {
  Grid,
  Hidden,
  Typography,
  withStyles,
  Button,
} from "@material-ui/core";
import LoginStyles from "../../styles/Login";
import {  useHistory } from "react-router-dom";

function AppInfo(props) {
  const { classes } = props;
  const history = useHistory();
  return (
    <Hidden only="xs">
      <Grid item xs={12} sm={4} md={3} lg={3} color = {"primary"}className={classes.appInfo}>
        
        <Typography className={classes.title} variant={"h2"} onClick={() => { history.push(`${process.env.PUBLIC_URL}/dashboard`)}}>ULCA</Typography>
        <Typography variant={"h3"} className={classes.subTitle}>
          Universal Language Contribution API
        </Typography>
        <Typography variant={"body1"} className={classes.body}>
        ULCA is an open-sourced scalable data platform, supporting various types of dataset for Indic languages, along with a user interface for interacting with the datasets.
        </Typography>
      </Grid>
    </Hidden>
  );
}

export default withStyles(LoginStyles)(AppInfo);
