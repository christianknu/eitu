 import { combineReducers } from 'redux';
import * as actions from '../actions/actions';

const rooms = (state = [], action) => {
	switch (action.type) {

		case actions.FETCH_ROOMS_SUCCESS:

			const rooms = JSON.parse(action.response).rooms;
			
			return [...state, ...rooms];

		default:
			return state;
	}
}

export default combineReducers({ 
	rooms,
})

