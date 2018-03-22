import React, { Component } from 'react';

const Layer = (props) => {
  if(props.children){
    return (
      props.children
    )
  }
  return(
    <div/>
  )
}

export default Layer;
