import React, {Component} from 'react';
import '../../css/graph.css';

class Graph extends Component {

  constructor(props) {
    super();
  }

  render() {
    return(
      <div className="graph">
        {
          this.props.children
        }
      </div>
    );
  }
}

export default Graph;
