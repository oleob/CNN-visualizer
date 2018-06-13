import React, { Component } from 'react';
import Typography from 'material-ui/Typography'
import Card, { CardActions, CardContent, CardMedia } from 'material-ui/Card';
import { withStyles } from 'material-ui/styles';
import Collapse from 'material-ui/transitions/Collapse';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ContentCopy from '@material-ui/icons/ContentCopy';
import IconButton from 'material-ui/IconButton';
import Button from 'material-ui/Button';
import { Link } from 'react-router-dom';
import classNames from 'classnames';

const styles = theme => ({
  card: {
    width: 224,
    margin: 12,
  },
  cardContent: {
    padding: 16,
    minHeight: 240,
  },
  media: {
    height: 0,
    paddingTop: '100%',
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
  textContainer: {
    padding: 16,
  }
});

class HomeLink extends Component {
  state = { expanded: false };

  handleExpandClick = () => {
    this.setState({ expanded: !this.state.expanded });
  };

  render() {
    const {classes} = this.props;
    return(
    <Card className={classes.card}>
      <Link to={this.props.link}>
        <CardMedia
          className={classes.media}
          image={this.props.imagePath}
          title={this.props.name}
        />
      </Link>
      <CardContent className={classNames(classes.cardContent)} style={{minWdith: 250}}>
        <Typography gutterBottom variant="headline" component="h2">
          {this.props.name}
        </Typography>
        <Typography component="p">
          {this.props.description}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" color="primary" onClick={this.handleExpandClick}>
          Learn More
        </Button>
        <Button size="small" color="primary">
          External Link
        </Button>
      </CardActions>
      <Collapse className={classes.textContainer} in={this.state.expanded} timeout="auto" unmountOnExit>
        <Typography component="p">
          {this.props.text}
        </Typography>
      </Collapse>
    </Card>
    );
  }
}

export default withStyles(styles)(HomeLink);
