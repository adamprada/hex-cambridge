import React from 'react';
import { Button, Layout } from 'antd';
import FirebaseService from '../services/FirebaseService';

const { Header, Footer, Content } = Layout;

const Home = () => (
  <Layout>
    <Header>Signed In</Header>
    <Content>
      <Button type="primary" color="red" onClick={FirebaseService.signOut}>Sign Out</Button>
    </Content>
    <Footer>Footer</Footer>
  </Layout>
);

export default Home;