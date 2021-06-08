import { createMuiTheme } from "@material-ui/core/styles";

const themeDefault = createMuiTheme({
  typography: {
    fontFamily: '"Lato", "Semibold"',
    font: "normal normal normal 14px/17px Lato",
    letterSpacing: "0px",
    fontSize: 14,
  },
  overrides: {
    MuiButton: {
      label: {
        textTransform: "capitalize",
        fontWeight: "normal",
        lineHeight: "1.14",
        letterSpacing: "1.25px",
        textAlign: "center",
        height: "26px"
      },
    },
  },

  palette: {
    primary: {
      light: "#60568d",
      main: "#2C2799",
      dark: "#271e4f",
      contrastText: "#FFFFFF",
    },
    secondary: {
      light: "#000000",
      main: "#000000",
      dark: "#000000",
      contrastText: "#FFFFFF",
    },
    background: {
      default: "#392C71",
    },
  },
});

themeDefault.typography.h4 = {
  fontSize: "1.875rem",
  fontWeight: "500",

  fontFamily: '"Poppins SemiBold", Regular',
  textAlign: "Left",
  "@media (min-width:600px)": {},
  [themeDefault.breakpoints.up("md")]: {},
};

themeDefault.typography.h4 = {
  fontSize: "1.875rem",
  fontWeight: "500",

  fontFamily: '"Poppins SemiBold", Regular',
  textAlign: "Left",
  "@media (min-width:600px)": {},
  [themeDefault.breakpoints.up("md")]: {},
};

export default themeDefault;
