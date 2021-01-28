import React from 'react';
import {Button, Form, Input, Select} from 'antd';
import {NavLink} from "react-router-dom";
import * as actions from "../store/actions/auth";
import {connect} from 'react-redux';

const { Option } = Select;

const layout = {
  labelCol: { span: 2 },
  wrapperCol: { span: 4 },
};


class RegistrationForm extends React.Component{
  // [form] = Form.useForm();

  onFinish = (values) => {
    values.phone_number = '+'+values.prefix+values.phone_number;
    console.log(values.phone_number);
    console.log('Received values of form: ', values);
    this.props.onAuth(
        values.username,
        values.first_name,
        values.last_name,
        values.email,
        values.phone_number,
        values.password1,
        values.password2,

        );
    this.props.history.push('/');
  };

  prefixSelector = (
    <Form.Item name="prefix" noStyle>
      <Select
        style={{
          width: 70,
        }}
      >
        <Option value="92">+92</Option>
        <Option value="966">+966</Option>
      </Select>
    </Form.Item>
  );
  // const [autoCompleteResult, setAutoCompleteResult] = useState([]);


  render() {
      return(
          <div>
              <Form
                  {...layout}
                  // form={form}
                  name="register"
                  onFinish={this.onFinish}
                  initialValues={{remember: true,}}
                  scrollToFirstError
                >
                <Form.Item
                    name="username"
                    label="Username"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your Username!',
                      },
                    ]}
                  >
                    <Input/>
                </Form.Item>

                <Form.Item
                    name="first_name"
                    label="Firstname"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your firstname!',
                      },
                    ]}
                  >
                    <Input/>
                </Form.Item>

                <Form.Item
                    name="last_name"
                    label="Lastname"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your lastname!',
                      },
                    ]}
                  >
                    <Input/>
                </Form.Item>

                <Form.Item
                    name="email"
                    label="E-mail"
                    rules={[
                      {
                        type: 'email',
                        message: 'The input is not valid E-mail!',
                      },
                      {
                        required: true,
                        message: 'Please input your E-mail!',
                      },
                    ]}
                  >
                    <Input/>
                  </Form.Item>

                  <Form.Item
                    name="phone_number"
                    label="Phone Number"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your phone number!',
                      },
                    ]}
                  >
                    <Input
                      addonBefore={this.prefixSelector}
                      style={{
                        width: '100%',
                      }}
                    />
                  </Form.Item>

                  <Form.Item
                    name="password1"
                    label="Password"
                    rules={[
                      {
                        required: true,
                        message: 'Please input your password!',
                      },
                    ]}
                    hasFeedback
                  >
                    <Input.Password />
                  </Form.Item>

                  <Form.Item
                    name="password2"
                    label="Confirm Password"
                    dependencies={['password1']}
                    hasFeedback
                    rules={[
                      {
                        required: true,
                        message: 'Please confirm your password!',
                      },
                      ({ getFieldValue }) => ({
                        validator(rule, value) {
                          if (!value || getFieldValue('password1') === value) {
                            return Promise.resolve();
                          }

                          return Promise.reject('The two passwords that you entered do not match!');
                        },
                      }),
                    ]}
                  >
                    <Input.Password />
                  </Form.Item>

                  <Form.Item>
                    <Button type="primary" htmlType="submit" className="login-form-button">
                      Register </Button> Or <NavLink to="/login/">Login</NavLink>
                  </Form.Item>
                </Form>
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
        onAuth: (username, first_name, last_name, email, phone_number, password1, password2) => dispatch(actions.authSignup(username, first_name, last_name, email, phone_number, password1, password2))
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RegistrationForm);