import React, { Component } from 'react';
import { withStyles } from 'material-ui/styles';

const styles = {
  conv: {
    textAlign: 'center',
    backgroundColor: '#B95450',
    padding: 20,
    margin: 10,
    borderRadius: 25,
    cursor: 'pointer',
  },
  pool: {
    textAlign: 'center',
    backgroundColor: '#6D8EBF',
    padding: 20,
    margin: 10,
    borderRadius: 25,
    cursor: 'pointer',
  },
  inception: {
    textAlign: 'center',
    backgroundColor: '#9673A6',
    padding: 20,
    margin: 10,
    borderRadius: 25,
    cursor: 'pointer',
  }
}

class NetworkNode extends Component {

  handleClick = () => {
    if(this.props.handleOpen!==undefined) {
      this.props.handleOpen();
    }
    this.props.changeSelectedLayer(this.props.layer)
  }

  render() {
    const {classes} = this.props;
    let cName;
    if(this.props.layer.info.operation==='Inception'){
      cName = classes.inception;
    } else if(this.props.layer.info.operation==='Convolution'){
      cName = classes.conv;
    } else {
      cName = classes.pool;
    }

    return(
      <div className={cName} onClick={this.handleClick}>
        {this.props.layer.info.name}
      </div>
    )
  }
}

export default withStyles(styles)(NetworkNode);
