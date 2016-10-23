 import { combineReducers } from 'redux';
import * as actions from '../actions/actions';

const rooms = (state = [], action) => {
	switch (action.type) {

		case actions.FETCH_ROOMS_SUCCESS:

				// console.log("action", action);

			// const rooms = JSON.parse(response).rooms;
			const rooms = response.rooms;
			
			console.log('rooms', rooms);
			return [...state, ...rooms];

		default:
			return state;
	}
}

export default combineReducers({ 
	rooms,
})

const response = {"rooms": [{"until": "Fri Oct 28 at 08:00", "room": "4A30"}, {"until": "Tue Oct 25 at 10:00", "room": "5A60"}, {"until": "Mon Oct 24 at 14:00", "room": "4A58"}, {"until": "Mon Oct 24 at 14:00", "room": "4A54"}, {"until": "Mon Oct 24 at 12:00", "room": "3A12/14"}, {"until": "Mon Oct 24 at 12:00", "room": "2A18"}, {"until": "Mon Oct 24 at 12:00", "room": "2A54"}, {"until": "Mon Oct 24 at 12:00", "room": "4A14"}, {"until": "Mon Oct 24 at 12:00", "room": "3A54"}, {"until": "Mon Oct 24 at 12:00", "room": "2A52"}, {"until": "Mon Oct 24 at 12:00", "room": "4A16"}, {"until": "Mon Oct 24 at 12:00", "room": "4A56"}, {"until": "Mon Oct 24 at 10:00", "room": "4A22"}, {"until": "Mon Oct 24 at 10:00", "room": "4A20"}, {"until": "Mon Oct 24 at 10:00", "room": "Aud 4"}, {"until": "Mon Oct 24 at 10:00", "room": "2A20"}, {"until": "Mon Oct 24 at 10:00", "room": "Aud 3"}, {"until": "Mon Oct 24 at 10:00", "room": "3A18"}, {"until": "Mon Oct 24 at 09:00", "room": "2A12"}, {"until": "Mon Oct 24 at 09:00", "room": "2A14"}, {"until": "Mon Oct 24 at 08:00", "room": "2A50"}, {"until": "Mon Oct 24 at 08:00", "room": "Aud 2"}, {"until": "Mon Oct 24 at 08:00", "room": "Aud 1"}, {"until": "Mon Oct 24 at 08:00", "room": "5A14-16"}]}
