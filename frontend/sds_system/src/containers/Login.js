import React from 'react';

import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { Form, Input, Button } from 'antd';
import {NavLink} from "react-router-dom";
import { connect } from "react-redux";
import * as actions from "../store/actions/auth";

const layout = {
  labelCol: {
    span: 2,
  },
  wrapperCol: {
    span: 4,
  },
};
const tailLayout = {
  wrapperCol: {
    offset: 2,
    span: 4,
  },
};

class Login extends React.Component {
  onFinish = (values) => {
    console.log('Success:', values);
    this.props.onAuth(values.username, values.password);
    this.props.history.push('/');
  };

  onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };
  render() {
      return (
        <Form
          align="center"
          {...layout}
          name="basic"
          // initialValues={{
          //   remember: true,
          // }}
          onFinish={this.onFinish}
          onFinishFailed={this.onFinishFailed}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[
              {
                required: true,
                message: 'Please input your username!',
              },
            ]}
          >
            <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[
              {
                required: true,
                message: 'Please input your password!',
              },
            ]}
          >
            <Input.Password
          prefix={<LockOutlined className="site-form-item-icon" />}
          type="password"
          placeholder="Password"
        />
          </Form.Item>

          {/*<Form.Item*/}
          {/*    {...tailLayout}*/}
          {/*    name="remember"*/}
          {/*    valuePropName="checked">*/}
          {/*  <Checkbox>Remember me</Checkbox>*/}
          {/*</Form.Item>*/}

          <Form.Item
              {...tailLayout}
          >
            <Button type="primary" htmlType="submit">Login</Button> Or <NavLink to='/signup/'>signup!</NavLink>
          </Form.Item>
        </Form>
    );
  }
}

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
        error: state.error
    }
}

const mapDispatchToProps = dispatch => {
  return {
    onAuth: (username, password) => dispatch(actions.authLogin(username, password))
  }
}

export default connect (mapStateToProps, mapDispatchToProps)(Login);