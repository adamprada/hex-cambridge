import React from 'react';
import { Form, Input, Button } from 'antd';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import AuthService from '../../services/FirebaseService';


const layout = {
  labelCol: { span: 6 },
  wrapperCol: { span: 16 },
};
const tailLayout = {
  wrapperCol: { offset: 6, span: 16 },
};

const formItemLayout = {
  labelCol: { span: 6 },
  wrapperCol: { span: 18 },
};

const formItemLayoutWithOutLabel = {
  wrapperCol: { span: 18, offset: 6 },
};

const SignUp = () => {
  const onFinish = (values) => AuthService.signUpTutor(values);

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  return (
    <Form
      {...layout}
      name="signup"
      initialValues={{ remember: true }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
      <Form.Item
        label="Email"
        name="email"
        rules={[{ required: true, message: 'Please input your email!' }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
      >
        <Input.Password />
      </Form.Item>

      <Form.List
        name="domains"
        rules={[
          {
            validator: async (_, domains) => {
              if (!domains || domains.length < 1) {
                return Promise.reject(new Error('At least 1 domain'));
              }
            },
          },
        ]}
      >
        {(fields, { add, remove }, { errors }) => (
          <>
            {fields.length === 0 && 
              <Form.Item
                label="Domain"
                name="domain"
                rules={[{ required: true, message: 'Please add domains!' }]}
                {...formItemLayout}
              >
                <Button
                type="dashed"
                onClick={() => add()}
                style={{ width: '60%' }}
                icon={<PlusOutlined />}
              >
                Add domain
              </Button>
              </Form.Item>}
            {fields.map((field, index) => (
              <Form.Item
                {...(index === 0 ? formItemLayout : formItemLayoutWithOutLabel)}
                label={index === 0 ? 'Domain' : ''}
                required={false}
                key={field.key}
              >
                <Form.Item
                  {...field}
                  validateTrigger={['onChange', 'onBlur']}
                  rules={[
                    {
                      required: true,
                      whitespace: true,
                      message: "Please input domain's name or delete this field.",
                    },
                  ]}
                  noStyle
                >
                  <Input placeholder="domain name" style={{ width: '60%' }} />
                </Form.Item>
                  <MinusCircleOutlined
                    className="dynamic-delete-button"
                    onClick={() => remove(field.name)}
                  />
              </Form.Item>
            ))}
            {fields.length > 0 && 
              <Form.Item wrapperCol={{ offset: 6 }}>
                <Button
                  type="dashed"
                  onClick={() => add()}
                  style={{ width: '60%' }}
                  icon={<PlusOutlined />}
                >
                  Add domain
                </Button>
                <Form.ErrorList errors={errors} />
              </Form.Item>
            }
          </>
        )}
      </Form.List>

      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          Create Account
        </Button>
      </Form.Item>
    </Form>
  )
}

export default SignUp;