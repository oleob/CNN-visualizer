import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';
import Close from '@material-ui/icons/Close';

import NetworkNode from './NetworkNode';

const styles = {
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#77aa77',
    borderRadius: 25,
    margin:10,
  },
  column: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    flexDirection: 'column',
    alignItems: 'center',
  },
  close: {
    position: 'absolute',
    top: 20,
    left: 20,
    cursor: 'pointer',
  },
  c2: {
    position: 'relative',
  }
}

class InceptionNode extends Component {

  state = {
    open: false,
  }

  handleOpen = () => {
    this.props.changeSelectedLayer(this.props.name)

    this.setState({open: true});
  }

  handleClose = () => {
    this.setState({open:false})
  }

  render() {
    const {classes} = this.props;
    return (
      <div className={classes.c2}>
        {!this.state.open &&
          <NetworkNode layer={this.props.layer} changeSelectedLayer={this.props.changeSelectedLayer} handleOpen={this.handleOpen}/>
        }

        {this.state.open &&
          <div className={classes.container}>
            <Close className={classes.close} onClick={this.handleClose}/>
            <div className={classes.column}>
              <NetworkNode layer={this.props.layer.children[0]} changeSelectedLayer={this.props.changeSelectedLayer} />
            </div>
            <div className={classes.column}>
              <NetworkNode layer={this.props.layer.children[1]} changeSelectedLayer={this.props.changeSelectedLayer} />
              <NetworkNode layer={this.props.layer.children[2]} changeSelectedLayer={this.props.changeSelectedLayer} />
            </div>
            <div className={classes.column}>
              <NetworkNode layer={this.props.layer.children[3]} changeSelectedLayer={this.props.changeSelectedLayer} />
              <NetworkNode layer={this.props.layer.children[4]} changeSelectedLayer={this.props.changeSelectedLayer} />
            </div>
            <div className={classes.column}>
              <NetworkNode layer={this.props.layer.children[5]} changeSelectedLayer={this.props.changeSelectedLayer} />
              <NetworkNode layer={this.props.layer.children[6]} changeSelectedLayer={this.props.changeSelectedLayer} />
            </div>
          </div>
        }
      </div>
    )
  }
}

export default withStyles(styles)(InceptionNode)
