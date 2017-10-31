import React from 'react'
import { BootstrapTable,TableHeaderColumn } from 'react-bootstrap-table'
import 'react-bootstrap-table/dist/react-bootstrap-table-all.min.css';
import ContentContainer from './ContentContainer'
import cm from '../common/CommunicationManager'

export default class TableView extends React.Component{
	constructor() {
		super()
		this.state = {filter:""}
		cm.subscribe("/Filter/Changed", function(data) {
			this.setState(Object.assign({}, this.state, {filter:data}))
		}, this)
	}
	
	/*
	componentDidUpdate(){
		cm.getStore().subscribe(function(){
			debugger
		});
	}
	*/
	
	render() {
		var data = [];
		var list = this.props.data;
		if (this.state.filter!=='') {
			for (var i=0; i<list.length; i++) {
				if (list[i].city.toLowerCase().indexOf(this.state.filter)>-1) {
					data.push(list[i])
				}
			}
		} else {
			data = list
		}
		
		return (
				<div style={{"height":"300px"}}>
					<p> Here are the house data loaded from a json file.</p>
					<BootstrapTable data={ data }>
				        <TableHeaderColumn dataField='street' isKey>street</TableHeaderColumn>
				        <TableHeaderColumn dataField='city'>city</TableHeaderColumn>
				        <TableHeaderColumn dataField='state'>state</TableHeaderColumn>
				        <TableHeaderColumn dataField='zipcode'>zipcode</TableHeaderColumn>
				      </BootstrapTable>	

				</div>
		)
	}
	
}
