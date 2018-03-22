import React from 'react';

const SubLayer = (props) =>{
  const style = {
    top: 200,
    width: props.size,
    height: props.size,
    lineHeight: props.size,
    borderRadius: props.size/2,
  }
  return(
    <div className="subLayer" style={style}/>
  );
}

export default SubLayer;
