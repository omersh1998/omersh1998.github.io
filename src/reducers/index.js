import constants from '../constants/constants';

const initialState = {
    inputValue: '',
    items: []
};

const reducer = (state = initialState, action) => {
    let newItems;
    switch(action.type) {
        case constants.INPUT_CHANGE:
            return Object.assign({}, state, { inputValue: action.text });
        case constants.ADD_ITEM:
            const item = {
                text: state.inputValue,
                id: Date.now(),
                isFinished: false
            };
            return Object.assign({}, state, { inputValue: '', items: state.items.concat(item) });
        case constants.CHANGE_ITEM_STATUS:
            newItems = state.items.slice();
            newItems.forEach(item => {
                if(item.id === action.id)
                    item.isFinished = !item.isFinished;         
            });
            return Object.assign({}, state, {items: newItems});
        case constants.DELETE_ITEMS:
            newItems = state.items.slice();
            newItems = newItems.filter((item) => item.isFinished === false );
            return Object.assign({}, state, { items:  newItems });
        default:
            return state;
    }
};

export default reducer;
