import React, { useState } from 'react';
import { Layout, Row, Col, Modal, Typography } from 'antd';
import FirebaseService from '../services/FirebaseService';
import SignUp from './SignInOrUp/SignInOrUp';
import UserTypeButton from '../components/UserTypeButton';

const { Title } = Typography;
const { Header, Content } = Layout;

const Landing = () => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = () => {
    setIsModalVisible(false);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <Layout style={{ height: "100vh" }}>
      <Header style={{ textAlign: "center", paddingTop: "7px" }}>
        <Typography>
          <Title style={{ color: "white" }}>Welcome</Title>
        </Typography>
      </Header>
      <Content>
        <Row type="flex" align="middle" style={{ height: '100%' }}>
          <Col span={12} style={{ textAlign: "right", paddingRight: "80px" }}>
            <UserTypeButton type="primary" onClick={FirebaseService.signInTutee}>
              Tutee
            </UserTypeButton>
          </Col>
          <Col span={12} style={{ textAlign: "left", paddingLeft: "80px" }}>
            <UserTypeButton type="primary" onClick={showModal}>
              Tutor
            </UserTypeButton>
          </Col>
        </Row>
        <Modal centered visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
          <SignUp />
        </Modal>
      </Content>
    </Layout>
  );
}

export default Landing;