import React from 'react'


const FilterItem = React.createClass({ 
	render() { 
		return (
			<span 
				onClick={() => this.props.onSelectFilter(this.props.id)} 
				style={{ userSelect: 'none', listStyle: 'none', margin: 0, marginBottom: '0.5em', padding: 0, color: 'steelblue', cursor: 'pointer' }}>

					<li>{this.props.title}</li>
				</span>
		)
	}
}) 

export default FilterItem;
