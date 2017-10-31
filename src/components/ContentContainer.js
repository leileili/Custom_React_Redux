import React from 'react'
import TableView from './TableView'
import {connect} from 'react-redux'
import cm from '../common/CommunicationManager'
import rs from '../common/RemoteServices'

class _ContentContainer extends React.Component{

	render() {
		
		return (
				<div>
					<TableView data={this.props.houseData}/>
				</div>
		)
	}
	
}


const ContentContainer = connect(
		  store => {
			    return {
			    	houseData: store.CommonReducer.houseData
			    };
			  }
			)(_ContentContainer);
export default ContentContainer