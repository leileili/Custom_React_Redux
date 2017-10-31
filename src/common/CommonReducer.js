//import cm from '../common/CommunicationManager'

const CommonReducer = (state = {"houseData":[]}, action) => {
  switch (action.type) {
  	case '_common_':
  		return state
	case 'houseData':
	    return Object.assign({}, state, {
	    	houseData: action.data
	    })
    default:
      return state
  }
}

export default CommonReducer