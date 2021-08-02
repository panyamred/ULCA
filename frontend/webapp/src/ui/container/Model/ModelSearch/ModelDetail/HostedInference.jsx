import { withStyles } from '@material-ui/core/styles';
import DatasetStyle from '../../../../styles/Dataset';
import { useHistory } from 'react-router';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
import HostedInferenceAPI from "../../../../../redux/actions/api/Model/ModelSearch/HostedInference";
import {
    Grid,
    Typography,
    TextField,
    Button,
    CardContent, Card
} from '@material-ui/core';
import { useState } from 'react';

const HostedInference = (props) => {
    const { classes, title, para, modelId } = props;
    const history = useHistory();
    const [translation, setTranslationState] = useState(false)
    const [sourceText, setSourceText] = useState("");
    const handleCompute = () => {
        const apiObj = new HostedInferenceAPI(modelId, sourceText);
        fetch(apiObj.apiEndPoint(), {
            method: 'POST',
            headers: apiObj.getHeaders().headers,
            body: JSON.stringify(apiObj.getBody())
        }).then(async resp => {
            let rsp_data = await resp.json();
            if (resp.ok) {
                setTranslationState(true)
            } else {
                new Promise.reject(rsp_data);
            }
        }).catch(err => {
            console.log(err)
        })
    };
    return (
        <div>
            <Typography className={classes.hosted}>Hosted inference API {< InfoOutlinedIcon className={classes.buttonStyle} fontSize="small" color="disabled" />}</Typography>
            <Grid container spacing={2}>
                <Grid className={classes.gridCompute} item xl={8} lg={8} md={8} sm={8} xs={8}>
                    <TextField fullWidth
                        color="primary"
                        label="Enter Text"
                        value={sourceText}
                        // error={error.name ? true : false}
                        // helperText={error.name}
                        onChange={(e) => {
                            setSourceText(e.target.value);
                        }}
                    />
                    {/* <textarea
                    rows={4}
                    cols={40}
                    placeholder="Enter Text"
                    //  rowsMax={4}
                    //     color="primary"
                    //     label="Enter Text"
                    // value={model.modelName}
                    // error={error.name ? true : false}
                    // helperText={error.name}
                    onChange={(e) => {
                        setModelInfo({ ...model, modelName: e.target.value })
                        setError({ ...error, name: false })
                    }}
                    /> */}
                </Grid>
                <Grid item xl={4} lg={4} md={4} sm={4} xs={4} className={classes.computeGrid}>
                    <Button
                        color="primary"
                        className={classes.computeBtn}
                        variant="contained"
                        size={'small'}

                        onClick={handleCompute}
                    >
                        Translate
                    </Button>
                </Grid>

                {translation &&
                    // <Grid item xl={11} lg={11} md={12} sm={12} xs={12}>
                    <Card style={{ backgroundColor: '#139D601A', color: 'black', heigth: '50px', width: '440px' }}>
                        <CardContent style={{ paddingBottom: '16px' }}>
                            This is my translated text
                        </CardContent>
                    </Card>
                    // </Grid>
                }
            </Grid>
        </div>

    )
}
export default withStyles(DatasetStyle)(HostedInference);