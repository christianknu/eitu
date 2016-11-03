 import { combineReducers } from 'redux';
import * as actions from '../actions/actions';

const rooms = (state = [], action) => {
	switch (action.type) {

		case actions.FETCH_ROOMS_SUCCESS:
			const emptyRooms = JSON.parse(action.response).empty;
			const bookedRooms = JSON.parse(action.response).booked;

			return [...state, ...emptyRooms, ...bookedRooms ];

		default:
			return state;
	}
}

export default combineReducers({ 
	rooms,
})

