
const CommonReducer = (state = {"houseData":[], "filterData":""}, action) => {
  	case '_common_':
  		return state
	case 'houseData':
	    return Object.assign({}, state, {
	    	houseData: action.data
	    })
	case 'filterData':
	    return Object.assign({}, state, {
	    	filterData: action.data
	    })
    default:
      return state
  }
}

export default CommonReducer