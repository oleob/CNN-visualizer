import React from 'react';
import Paper from 'material-ui/Paper';

const Activations = (props) => {

  if(props.showActivations){
    return(
      <Paper className="activations" >
        {
          props.filepaths.map((filepath, i)=>(
            <div key={i} className="activation">
              <img style={{width: 75, height: 75, imageRendering: 'pixelated'}}src={filepath}/>
            </div>
          ))
        }
      </Paper>
    )
  }
  else{
    return(<div />)
  }
}

export default Activations;
