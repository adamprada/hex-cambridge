import React from 'react';
import { Tabs } from 'antd';
import SignIn from './SignIn';
import SignUp from './SignUp';

const { TabPane } = Tabs;

const SignInOrUp = () => {
  return (
    <Tabs defaultActiveKey="1" centered size="large">
      <TabPane tab="Sign In" key="1">
        <SignIn />
      </TabPane>
      <TabPane tab="Sign Up" key="2">
        <SignUp />
      </TabPane>
    </Tabs>
  );
}

export default SignInOrUp;