export const FETCH_ROOMS_SUCCESS = "FETCH_ROOMS_SUCCESS";
export const FETCH_ROOMS_FAILURE = "FETCH_ROOMS_FAILURE";

import xhr from './ajax';

export const fetchRooms = () => (dispatch) => {
	xhr('/rooms')
		.get()
		.then(
			rooms => dispatch({ 
					type: FETCH_ROOMS_SUCCESS, 
					response: rooms,
				}),
			err => dispatch({ 
				type: FETCH_ROOMS_FAILURE, 
				err,
			}),
		)
};
