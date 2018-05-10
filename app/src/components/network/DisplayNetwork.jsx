import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import Paper from 'material-ui/Paper';
import Dialog, { DialogTitle } from 'material-ui/Dialog';
import Button from 'material-ui/Button';

import NetworkNode from './NetworkNode';
import InceptionNode from './InceptionNode';

const styles = {
  container: {
    maxWidth: 1000,
  },
  flexContainer: {

  },
  paper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    overflow: 'auto',
    flexWrap: 'nowrap',
    padding: 20,
  },
  infoBox: {
    margin: 20,
    padding: 10,
  },
  layerName: {
    padding: 10,
  }
}

class DisplayNetwork extends Component {

  state = {
    open: false
  }

  changeSelectedLayer = layer => {
    this.props.changeSelectedLayer(layer)
  }

  handleClose = () => {
    this.setState({ open: false });
  }

  toggleOpen = () => {
    this.setState(prevstate => ({open: !prevstate.open}))
  }

  render() {
    const { classes } = this.props;
    return(
      <div>
        <Button variant="raised" onClick={this.toggleOpen}>
          Select Layer
        </Button>
        {!(Object.keys(this.props.selectedLayer.info).length === 0) &&
          <div className={classes.layerName}>
            <p>Selected layer: {this.props.selectedLayer.info.name}</p>
          </div>
        }
        <Dialog open={this.state.open} onClose={this.handleClose} maxWidth={false}>
          {!(Object.keys(this.props.selectedLayer.info).length === 0) &&
            <Paper className={classes.infoBox}>
              <h3>Layer info</h3>
              {
                Object.entries(this.props.selectedLayer.info).map((item, index) => (
                  <p key={index}>{item[0]}: {item[1]}</p>
                ))
              }
            </Paper>
          }
          <Paper className={classes.paper}>
            {
              this.props.layers.map((layer, index) => {
                if(layer.info.operation==='Inception') {
                  return(
                    <InceptionNode key={index} layer={layer} changeSelectedLayer={this.changeSelectedLayer} />
                  )
                }
                else {
                  return(
                    <NetworkNode key={index} layer={layer} changeSelectedLayer={this.changeSelectedLayer} />
                  )
                }
              })
            }
          </Paper>
        </Dialog>
      </div>
    )
  }
}

export default withStyles(styles)(DisplayNetwork);
