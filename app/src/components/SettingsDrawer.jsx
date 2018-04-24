import React from 'react';
import Drawer from 'material-ui/Drawer';
import Button from 'material-ui/Button';


const SettingsDrawer = (props) => {
  return (
    <Drawer open={props.showDrawer} onClose={props.toggleDrawer}>
        <Button variant="raised">
          Potato
        </Button>
    </Drawer>
  );
}


export default SettingsDrawer;
