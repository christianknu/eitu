import React from 'react'

import { connect } from 'react-redux';

const FilterItem = React.createClass({ 
	render() { 

		const { id, params, title  } = this.props;
		return (
			<span 
				onClick={() => this.props.onSelectFilter(id)} 
				style={{ 
					WebkitUserSelect: 'none', 
					listStyle: 'none', 
					margin: 0, 
					marginBottom: '0.5em', 
					padding: 0, 
					color: 'steelblue', 
					cursor: 'pointer', 
					backgroundColor: (params && params.floor === title) && '#c8e6ff',
				}}>
					<li>{title}</li>
				</span>
		)
	}
}) 


export default FilterItem;
