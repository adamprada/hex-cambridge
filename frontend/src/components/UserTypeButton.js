import { Button } from 'antd';

const UserTypeButton = (props) => (
  <Button {...props} style={{ height: "200px", width: "200px", borderRadius: "100px", fontSize: 30, fontWeight: 500 }} >
    {props.children}
  </Button>
);

export default UserTypeButton;