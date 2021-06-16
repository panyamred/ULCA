const HeaderStyles = (theme) => ({

  root: {
    
  },
  drawerHeader: {
    display: "flex",
    flexDirection: "row",
  },
  toolbar: {
    maxWidth: "1272px",
    width : "100%",
    margin :"0 auto",
    display: 'flex',
    alignItems: 'center',
    padding:"0"
  },
  
 
  
  menu: {
    width: '100%',
    display: 'flex'
  },
  datasetOption: {
    marginLeft: '14.4%',
    marginRight: '2.4%',
    
  },
  profile: {
    marginLeft: 'auto'
  },
  
 
  profileName: {
    marginLeft: '0.5rem',
    "@media (max-width:800px)": {
      display: 'none'
    },
  },
 




});
export default HeaderStyles;
