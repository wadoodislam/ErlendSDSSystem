import React from 'react';
import * as actions from "../store/actions/auth";
import {Link, withRouter} from "react-router-dom";
import {connect} from "react-redux";

import { Layout, Menu, Breadcrumb } from 'antd';
const { Header, Content, Footer } = Layout;


class CustomLayout extends React.Component {
    render() {
        return (
        <Layout className="layout">
    <Header>
      <div className="logo" />
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']}>
        <Menu.Item key="1">Home</Menu.Item>

          {
              this.props.isAuthenticated ?
                  <Menu.Item key="2" onClick={this.props.logout}>
                    Logout
                  </Menu.Item>

              :
                  <Menu.Item key="2">
                    <Link to='/login'>Login</Link>
                  </Menu.Item>
          }


      </Menu>
    </Header>
    <Content style={{ padding: '0 50px' }}>
      <Breadcrumb style={{ margin: '16px 0' }}>
        <Breadcrumb.Item>Home</Breadcrumb.Item>
        <Breadcrumb.Item>List</Breadcrumb.Item>
        <Breadcrumb.Item>App</Breadcrumb.Item>
      </Breadcrumb>
      <div className="site-layout-content">{this.props.children}</div>
    </Content>
    <Footer style={{ textAlign: 'center' }}>Created by Softcreed Co.</Footer>
  </Layout>
    )
    }
}

const mapDispatchToProps = dispatch => {
    return {
        logout: () => dispatch(actions.logout())
    }
}

export default withRouter(connect (null, mapDispatchToProps)(CustomLayout)) ;
