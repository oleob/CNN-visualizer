import React, {Component} from 'react';
import '../../css/graph.css';

class Graph extends Component {

  constructor(props) {
    super();
    const layers = [];
    const numChildren = props.children.length;
    let left = -(props.size*(numChildren-1) + props.spacing*(numChildren-1))/2;
    for(let i=0; i < numChildren; i++){
      const content = props.children[i];
      const style = {
        left,
        height: props.size,
        width: props.size,
        lineHeight: props.size,
        borderRadius: props.size/2,
      }

      const child = {
        content,
        style,
      }

      layers.push(child);
      left += props.size + props.spacing;
    }

    this.state = {
      layers,
    }
  }

  render() {
    return(
      <div className="graph">
        {
          this.state.layers.map((layer, i)=>(
            <div key={i} className = "layer node" style={layer.style} >
              {layer.content}
            </div>
          ))
        }
      </div>
    );
  }
}

export default Graph;
