import React from 'react';
import {Route} from 'react-router-dom';
import ArticleList from './components/ArticleList';
import Login from './containers/Login';
import Signup from './containers/Signup';

const BaseRouter = () => (
    <div>
        <Route exact path='/list' component={ArticleList}></Route>
        <Route exact path='/login/' component={Login}></Route>
        <Route exact path='/signup/' component={Signup}></Route>
    </div>
);

export default BaseRouter