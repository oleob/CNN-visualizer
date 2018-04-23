import React from 'react';
import Drawer from 'material-ui/Drawer';

const SettingsDrawer = (props) => (
  <Drawer open={props.showDrawer} >
    <div
      tabIndex={0}
      role="button"
      onClick={props.toggleDrawer}
      onKeyDown={props.toggleDrawer}
    >
    </div>
  </Drawer>
);

export default SettingsDrawer;
