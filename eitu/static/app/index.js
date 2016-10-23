import React from 'react'

import App from './app'
import thunkMiddleware from 'redux-thunk'

import rootReducer from './reducers/rootReducer'

import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
// import { loadState, saveState } from './localStorage';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux'

import createActionLogger from 'redux-logger';

const midddleWare = [thunkMiddleware, createActionLogger({ collapsed: true, duration: true })];

const store = createStore(
			rootReducer, 
			{},
			applyMiddleware(...midddleWare),
		window.devToolsExtension ? window.devToolsExtension() : undefined
);

const history = syncHistoryWithStore(browserHistory, store);

const router = (
	<Provider store={store}>
		<Router history={history}>
			<Route path="/" component={App}> </Route>
			<Route path="/floor/:floor" component={App}> </Route>
			<Route path="/favourites" component={App}> </Route>
		</Router>
	</Provider>
);

render(router, document.getElementById('app'));

// render(<App>, document.getElementById('app'));
