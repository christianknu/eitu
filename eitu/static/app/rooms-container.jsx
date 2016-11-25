import React from'react'
import EmptyRoom from './empty-room';

import { connect } from 'react-redux';
import { withRouter } from 'react-router';

const floors = { 
	"Ground_Floor" : 0, 
	"1st_Floor": 1, 
	"2nd_Floor": 2, 
	"3rd_Floor": 3, 
	"4th_Floor": 4, 
	"5th_Floor": 5, 
}

const emptyRooms = React.createClass({
	render() { 
		const { currentFloor, isViewingFavourites, showBooked } = this.props;

		let ls;
		if (isViewingFavourites) ls = localStorage.getItem('rooms');

		const rooms =	this.props.rooms
			.filter(r => {
				if (showBooked) return true;
				return r.empty !== false
			})
			.filter(r => { 
				if (!currentFloor) return true;
				if (floors[currentFloor] == 0 && r.room[0] == "A") return true; 
				return r.room[0] == floors[currentFloor];
			})
			.filter(r => { 
				if (isViewingFavourites) return ls.indexOf(r.room) > -1;
				return true;
			})

			.map((r,i) => <EmptyRoom isBooked={r.empty === false} key={i} room={r.room} until={r.until} wifi={r.wifi} /> )
				
		return ( 
			<div>
				<div style={{ display: 'flex' , flexDirection: 'column' }} >
				<span style={{ padding: '1rem'}}>
					Also show booked rooms
					<i 
						onClick={this.showBooked} 
						style={{
							padding: '1rem',
							color: showBooked ? 'green' : 'tomato',
						}}
						className={showBooked ? "fa fa-toggle-on fa-2x" : "fa fa-toggle-off fa-2x "}>
					</i>
				</span>

				<div style={{ display: "flex", justifyContent: 'space-around' }} >
					<h4>Room</h4>
					<h4>Available</h4>
					<h4>People</h4>
				</div>

				{ rooms.length > 0 
					? rooms
					: "No rooms available on this floor."
				}

				</div>
				</div>
		);
	},

	showBooked() {
		const { location, router, params } = this.props;
		const query = { ...location.query, showBooked: true};
		if (location.query.showBooked) delete query['showBooked'];

		router.push({
			pathname: location.pathname,
			query,
		});

	},
});

const mapStateToProps = (state, ownProps) => {
	return {
		rooms: state.rooms.rooms || [],
		currentFloor: ownProps.params.floor,
		isViewingFavourites: ownProps.location.query.favourites,
		showBooked: ownProps.location.query.showBooked,
	}
}

export default withRouter(connect(mapStateToProps, null)(emptyRooms));

