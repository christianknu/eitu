
import React from'react'
// import Toolbar from './toolbar'

import EmptyRooms from './rooms-container';

import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import { Link } from 'react-router'
import { fetchRooms } from './actions/actions';

import Filter from './filter';

const App = React.createClass({
	contextTypes: { 
		store: React.PropTypes.object
	},
	componentDidMount() {
		const { store } = this.context;
		this.unsubscribe = store.subscribe(() => 
			this.forceUpdate()
		);

		this.props.dispatchFetchRooms();
	},
	render() { 
		const { params, location } = this.props;

		return ( 
			<div>
				<div style={{ display: 'flex' }} >
					<Filter params={params} location={location} />
					<EmptyRooms params={params} location={location} />

			</div>
				</div>
		);
	}
});

const mapDispatchToProps = (dispatch) => {
	return { 
		dispatchFetchRooms: () => dispatch(fetchRooms()),
	}
}

export default connect(null, mapDispatchToProps)(App);
