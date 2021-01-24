import React from 'react';
import { Steps, Button, Typography, Upload, Table, Tag } from 'antd';
import { InboxOutlined, SearchOutlined } from '@ant-design/icons';
import FirebaseService from '../../services/FirebaseService';
import { FirebaseDatabaseNode } from '@react-firebase/database';
import VideoConference from '../../components/VideoConference';

const { Title, Paragraph, Text } = Typography;
const { Dragger } = Upload;
const { Step } = Steps;

const TuteeStepper = ({ uid, setImageUrl }) => {
  const [current, setCurrent] = React.useState(0);
  const [jitsiId, setJitsiId] = React.useState("");

  const next = () => {
    setCurrent(current + 1);
  };

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

  const StepOne = () => (
    <div style={{ padding: 20, paddingTop: 40, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
      <Typography>
        <Title>Upload your question.</Title>
        <Paragraph>
          We'll process your file to determine which tutor will be most suitable for helping you. We'll process your file to determine which tutor will be most suitable for helping you.
        </Paragraph>
      </Typography>
      <Dragger name="file" multiple={false} action={async (file) => FirebaseService.uploadFile(uid, file).then((url) => setImageUrl(url)).then(() => next())}>
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
        <p className="ant-upload-hint">
          Support for a single or bulk upload. Strictly prohibit from uploading company data or other
          band files
        </p>
      </Dragger>
      <Button onClick={next} style={{ marginTop: 10 }}>Continue</Button>
    </div>
  );
  
  const StepTwo = () => {
    
    return (
      <div style={{ padding: 20, paddingTop: 40, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
        <Typography>
          <Title>Great! Now let's find you a tutor.</Title>
          <Paragraph>
            Based on the file characteristics we've determined using <Text strong>machine learning</Text>, we will find the best tutor for you available at this time.
          </Paragraph>
        </Typography>
        <FirebaseDatabaseNode path="matches/">
          {d => {
            if (d.value) {
              const matches = Object.values(d.value).filter(m => m.tuteeId === uid);
              const data = matches.map(({ tutorId, tuteeId, jitsiId, accepted }) => ({
                key: jitsiId,
                matchId: jitsiId,
                status: accepted ? <Tag color="green">ACCEPTED</Tag> : <Tag color="orange">PENDING</Tag>,
                action: accepted ?
                  <Button onClick={() => { setJitsiId(jitsiId); next() }}>Continue</Button>
                  : null
              }));
              if (data.length > 0) {
                return <Table columns={columns} dataSource={data} />
              }
              return <Button type="primary" shape="round" icon={<SearchOutlined />} onClick={() => FirebaseService.findMatch(uid, "asdf")} style={{ width: 200, height: 100, marginTop: 50 }} />;
            }
            return <Button type="primary" shape="round" icon={<SearchOutlined />} onClick={() => FirebaseService.findMatch(uid, "asdf")} style={{ width: 200, height: 100, marginTop: 50 }} />;
          }}
        </FirebaseDatabaseNode>
      </div>
    );
  }

  const StepThree = () => (
    <div style={{ padding: 20, paddingTop: 40, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
      <VideoConference jitsiId={jitsiId} />
    </div>
  );

  const steps = [
    {
      title: 'Upload Questions',
      content: <StepOne />,
    },
    {
      title: 'Find Tutor',
      content: <StepTwo />,
    },
    {
      title: 'Chat',
      content: <StepThree />,
    },
  ];

  return (
    <>
      <Steps current={current}>
        {steps.map(item => (
          <Step key={item.title} title={item.title} />
        ))}
      </Steps>
      <div className="steps-content" style={{ height: "100%" }}>{steps[current].content}</div>
    </>
  );
};

export default TuteeStepper;