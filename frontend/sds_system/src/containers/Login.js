import React from 'react';
import {connect} from 'react-redux';

import {Button, Form, Input, Spin} from 'antd';
import {LoadingOutlined, LockOutlined, UserOutlined} from '@ant-design/icons';
import {NavLink} from "react-router-dom";
import * as actions from "../store/actions/auth";

const antIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;



class LoginForm extends React.Component {
    onFinish = (values) => {
        console.log('Received values of form: ', values);
        this.props.onAuth(values.username, values.password);
        if (this.props.error === null) {

            this.props.history.push('/');
        }
    };

  render() {
      let errorMessage = null;
  if (this.props.error){
      errorMessage = (
          <p>{this.props.error.message}</p>
      )
  }

  return (

      <div>
          {errorMessage}
          {
              this.props.loading ?
                  <Spin indicator={antIcon} />
              :
                <Form
                  name="normal_login"
                  className="login-form"
                  initialValues={{remember: true,}}
                  onFinish={this.onFinish}
                >
                  <Form.Item
                    name="username"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your Username!',
                      },
                    ]}
                  >
                    <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
                  </Form.Item>
                  <Form.Item
                    name="password"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your Password!',
                      },
                    ]}
                  >
                    <Input
                      prefix={<LockOutlined className="site-form-item-icon" />}
                      type="password"
                      placeholder="Password"
                    />
                  </Form.Item>
                  {/*<Form.Item>*/}
                  {/*  <Form.Item name="remember" valuePropName="checked" noStyle>*/}
                  {/*    <Checkbox>Remember me</Checkbox>*/}
                  {/*  </Form.Item>*/}

                  {/*  <a className="login-form-forgot" href="">*/}
                  {/*    Forgot password*/}
                  {/*  </a>*/}
                  {/*</Form.Item>*/}

                  <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button">
                      Log in </Button> Or <NavLink to="/signup/">register now!</NavLink>
                  </Form.Item>
                </Form>
          }
      </div>
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

export default  connect(mapStateToProps, mapDispatchToProps)(LoginForm);
