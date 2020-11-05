import 'antd/dist/antd.css';
import React, {Component} from "react";
import CustomLayout from "./containers/Layout";
import {BrowserRouter as Router} from 'react-router-dom';
import {connect} from 'react-redux';
import BaseRouter from './routes';
import * as actions from "./store/actions/auth";


class App extends Component {
    componentDidMount() {
        this.props.onTryAutoSignup();
    }

    render() {
    return (
      <div>
          <Router>
              <header className="App-header">
                  <CustomLayout {...this.props}>
                      <BaseRouter></BaseRouter>
                  </CustomLayout>
              </header>
          </Router>

      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    isAuthenticated: state.token !== null
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onTryAutoSignup: () => dispatch(actions.authCheckState())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
