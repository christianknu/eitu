import React from'react'

const glassBoxes = ["2A03", "2A07", "3A03", "4A01", "4A03", "4A07", "5A03", "5A07"];

const emptyRoom = React.createClass({
	getDefaultProps() {
		isFavoriteItem: !!(Date.now() % 2)
	},

	getInitialState() {
		return {
			isHovered: false,
		};
	},

	render() { 
		const { room, until } = this.props; 
		const { isHovered } = this.state;

		const isGlassbox = glassBoxes.includes(room);

		const css = { border: '1px solid black', padding: '1rem', width: '100%' }

		const isFavoriteItem = localStorage.getItem('rooms').indexOf(room) > -1;

		return ( 
			<div onClick={() => this.makeFavourite(room)}>
				<div style={{ display: 'flex', border: '1px solid black' }} >

					<span style={css}>
					{ isGlassbox 
						? `${room} (glass box)`
						: room
					}
					<i 
						onMouseEnter={() => this.setState({ isHovered: true })} 
			      onMouseLeave={() => this.setState({ isHovered: false })} 
						style={{ float: 'right', color: 'gold' }} 
						className={ (isFavoriteItem || isHovered) ? "fa fa-star" : "fa fa-star-o"}>
					</i>

					 </span>
					<span style={css}>{ until }</span>

				</div>
			</div>
		);
	},

	makeFavourite(favourite) {
		const ls = localStorage.getItem('rooms');

		const updatedLs = ls.concat(` ${favourite}`);

		localStorage.setItem('rooms', updatedLs);
	},
});

export default emptyRoom;

