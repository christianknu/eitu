import React from'react'

const glassBoxes = ["2A03", "2A07", "3A03", "4A01", "4A03", "4A07", "5A03", "5A07"];

const wifi = ["none", "few", "many"];

const emptyRoom = React.createClass({
	getInitialState() {
		return {
			isHovered: false,
		};
	},

	render() { 
		const { isBooked, room, until, wifi } = this.props;
		const { isHovered } = this.state;

		const isGlassbox = glassBoxes.includes(room);

		const css = { borderBottom: '1px solid black', borderRight: '1px dashed gray', padding: '1rem', width: '100%' }

		let isFavoriteItem;
			
		try {
			const serealizedState = localStorage.getItem('rooms');
			 if (serealizedState != null) {
				 isFavoriteItem = serealizedState.indexOf(room) > -1;
			 }
		}

		catch (error) { 
			console.log('error', error);
		}


		return ( 
			<div onClick={() => this.makeFavourite(room)}>
				<div style={{ 
					display: 'flex', 
					border: isBooked ? '1px solid red' : '1px solid black',

				}} >

					<span style={css}>
					{ isBooked 
						? `${room} (booked) `
						: room
					}
					<i 
						onMouseEnter={() => this.setState({ isHovered: true })} 
						onMouseLeave={() => this.setState({ isHovered: false })}
						style={{ float: 'right', color: 'gold' }} 
						className={ (isFavoriteItem || isHovered) ? "fa fa-star" : "fa fa-star-o"}>
					</i>

					 </span>
					<span style={css}>{ isBooked ? `from: ${until}` : `to: ${until}`  }</span>
					<span style={css}>{ wifi } </span>

				</div>
			</div>
		);
	},

	makeFavourite(favourite) {
	try {
		const serealizedState = localStorage.getItem('rooms');
		if (serealizedState === null) {
			 localStorage.setItem('rooms', favourite);
		 }

		else {
			const updatedLs = serealizedState.concat(` ${favourite}`);
			localStorage.setItem('rooms', updatedLs);
		}
	}
	catch (error) { 
		console.log('error', error);
	}
	},
});

export default emptyRoom;

