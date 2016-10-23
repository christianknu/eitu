import React from 'react'
import FilterItem from './filter-item'

import { connect } from 'react-redux';
import { withRouter } from 'react-router';

import { Link } from 'react-router'

const Filter = React.createClass({
	getInitialState() {
		return {
			floors: [ 
				{id: 0, title: "All"}, 
				{id: 1, title: "Ground_Floor"}, 
				{id: 2, title: "1st_Floor"}, 
				{id: 3, title: "2nd_Floor"}, 
				{id: 4, title: "3rd_Floor"}, 
				{id: 5, title: "4th_Floor"}, 
				{id: 6, title: "5th_Floor"}, 
			],
			isViewingFavourites: false,
		}
	},
	render() { 
		const toolbarStyle = { background: 'aliceblue', display: 'flex', flexDirection: 'column', };

		return ( 
			<div style={toolbarStyle}>
				<div style={{display: 'flex', justifyContent: 'center', marginBottom: '1rem', alignItems: 'center' }}>
					<Link style={{ textDecoration: 'none', color: '#386890' }} to='/'> <h2 style={{padding: '0.5em'}}>Filter</h2></Link>
				</div>

				<ul style={{padding: '1em', listStyle: "none", display: 'flex', flexDirection: 'column'}}>
				<h3 style={{color: '#878a8c', fontStyle: 'italic'}}>Floors</h3>

				{ this.state.floors.map((f,i) => <FilterItem key={i} id={f.id} title={f.title} onSelectFilter={this.changeFilter}/> ) }
				
			<h3 style={{ cursor: 'pointer', userSelect: 'none' }} onClick={this.viewFavourites}>Favourites</h3>
				
						</ul>
					</div>
				);
		},

			changeFilter(floor) {
				const { router } = this.props;

				if (floor) router.push(`/floor/${this.state.floors[floor].title}`); 
				else router.push('/');
			},

			viewFavourites() {
				const { router, location } = this.props;

				this.setState({
								isViewingFavourites: !this.state.isViewingFavourites
				}, () => {
						if (!this.state.isViewingFavourites) {
							return router.push(`${location.pathname}`)
						}
						
						return router.push(`${location.pathname}?favourites=${this.state.isViewingFavourites}`);
					})
			},
	});

	const mapStateToProps = (state, ownProps) => {
		return {
		}
	}

	export default withRouter(connect(mapStateToProps, null)(Filter));

