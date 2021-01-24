import React from 'react';
import { Layout, Typography, Menu, Row, Col } from 'antd';
import FirebaseService from '../../services/FirebaseService';
import logo from '../../logo.svg';
import TuteeStepper from './TuteeStepper';
import { SketchField, Tools } from 'react-sketch';

const { Header, Content } = Layout;
const { Title, Paragraph, Text } = Typography;

const Tutee = ({ uid }) => {
  const [imageUrl, setImageUrl] = React.useState("");
  return (
    <Layout style={{ height: "100vh" }}>
      <Header style={{ textAlign: "center" }}>
        <img src={logo} className="App-logo" alt="logo" style={{ position: "absolute" }} />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="1" onClick={FirebaseService.signOut} style={{ position: "absolute", right: 40, fontWeight: 600 }}>Sign Out</Menu.Item>
        </Menu>
      </Header>
      <Content>
        <Row type="flex" align="middle" style={{ height: '100%' }}>
          <Col span={12} style={{ padding: 70, height: "60%" }}>
            <TuteeStepper uid={uid} setImageUrl={setImageUrl} />
          </Col>
          <Col span={12} style={{ padding: 20 }}>
            <SketchField width='1024px' 
                         height='768px' 
                         tool={Tools.Pencil}
                         backgroundColor="transparent"
                         lineColor='black'
                         opacity={1}
                         lineWidth={3}
                         style={{ position: 'absolute', zIndex: 1000}}/>
            <img src={imageUrl} style={{ zIndex: -1000}}/>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
}

export default Tutee;