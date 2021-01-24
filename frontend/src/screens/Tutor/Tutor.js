import React from 'react';
import { Button, Layout, Typography, Menu, Row, Col, Table, Tag } from 'antd';
import FirebaseService from '../../services/FirebaseService';
import { FirebaseDatabaseNode } from '@react-firebase/database';
import logo from '../../logo.svg';
import VideoConference from '../../components/VideoConference';
import { SketchField, Tools } from 'react-sketch';

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

const columns = [
  {
    title: 'Match Id',
    dataIndex: 'matchId',
    key: 'matchId',
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: 'Action',
    dataIndex: 'action',
    key: 'action'
  },
];

const Tutor = ({ uid }) => {
  const [jitsiId, setJitsiId] = React.useState("");
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
                  <Col span={12} style={{ padding: 20 }}>
                    {!jitsiId && <FirebaseDatabaseNode path="matches/">
                      {d => {
                        if (d.value) {
                          const matches = Object.values(d.value).filter(m => m.tutorId === uid);
                          const data = matches.map(({ tuteeId, jitsiId, accepted }) => ({
                            key: jitsiId,
                            matchId: jitsiId,
                            status: accepted ? <Tag color="green">ACCEPTED</Tag> : <Tag color="orange">PENDING</Tag>,
                            action: <Button onClick={() => { FirebaseService.getImageUrl(tuteeId).then((url) => { setImageUrl(url) }); setJitsiId(jitsiId) }}>Accept</Button>
                          }));
                          return <Table columns={columns} dataSource={data} />
                        }
                        return null;
                      }}
                    </FirebaseDatabaseNode>}
                    {jitsiId && <VideoConference jitsiId={jitsiId} />}
                  </Col>
                  <Col span={12} style={{ padding: 20 }}>
                    {!imageUrl && <FirebaseDatabaseNode path={"users/" + uid}>
                      {d => {
                        if (d.value) {
                          return (
                            <Typography>
                              <Title>Welcome back, {d.value.email}</Title>
                              <Paragraph>
                                We will match you according to the skills you listed when you created your account, which include: {d.value.domains}
                              </Paragraph>
                            </Typography>
                          );
                        }
                        return null;
                      }}
                      </FirebaseDatabaseNode>}
                    {imageUrl && [
                      <SketchField width='1024px' 
                        height='768px' 
                        tool={Tools.Pencil}
                        backgroundColor="transparent"
                        lineColor='black'
                        opacity={1}
                        lineWidth={3}
                        style={{ position: 'absolute', zIndex: 1000}}/>,
                      <img src={imageUrl} style={{ zIndex: -1000}}/>
                    ]}
                  </Col>
                </Row>
      </Content>
    </Layout>
  );
}

export default Tutor;