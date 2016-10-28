import React from'react'
import EmptyRoom from './empty-room';

import { connect } from 'react-redux';

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
		console.log('currentFloor', this.props.currentFloor);
		const { currentFloor, isViewingFavourites } = this.props;

		let ls;
		if (isViewingFavourites) ls = localStorage.getItem('rooms');

		const rooms =	this.props.rooms
			.filter(r => { 
				if (!currentFloor) return true;
				if (floors[currentFloor] == 0 && r.room[0] == "A") return true; 
				return r.room[0] == floors[currentFloor];
			})
			.filter(r => { 
				if (isViewingFavourites) return ls.indexOf(r.room) > -1;
				return true;
			})

			.map((r,i) => <EmptyRoom key={i} room={r.room} until={r.until} wifi={r.wifi} /> )
				
		return ( 
			<div>
				<div style={{ display: 'flex' , flexDirection: 'column' }} >

				<h1>Empty Rooms</h1>
				<div style={{ display: "flex", justifyContent: 'space-around' }} >
					<h2>Room</h2>
					<h2>Until</h2>
					<h2>People</h2>
				 </div>

				 { rooms.length > 0 
					 ? rooms
					 : "No rooms available on this floor."
				 }

				</div>
			</div>
		);
	}
});

const mapStateToProps = (state, ownProps) => {
	// console.log('state', state);
	console.log('ownProps', ownProps);
	return {
		rooms: state.rooms.rooms || [],
		currentFloor: ownProps.params.floor,
		isViewingFavourites: ownProps.location.query.favourites,
	}
}

export default connect(mapStateToProps, null)(emptyRooms);
