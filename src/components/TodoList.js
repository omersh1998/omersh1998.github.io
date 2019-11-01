import React from 'react';
import { connect } from 'react-redux';
import constants from '../constants/constants';
import DisplayItems from './DisplayItems';

function TodoList(props) {
  return (
    <div className="App">
        <h1>TodoList</h1>
        <input type='text' value={props.inputValue} onChange={(e) => props.onChange(e)}/>
        <div>
            <button onClick={() => props.addItem(props.inputValue)}>Add</button>
            <button onClick={props.deleteItems}>Delete</button>
        </div>
        <div>
            <ul>
                <DisplayItems items={props.items} changeItemStatus={props.changeItemStatus} />
            </ul>
        </div>
    </div>
  );
}

const mapStateToProps = (state) => {
    return {
        inputValue: state.inputValue,
        items: state.items
    };
};

const mapDispatchToProps = (dispatch) => {
    let action;
    return {
        onChange: (e) => {
            action = {type: 'INPUT_CHANGE', text: e.target.value};
            dispatch(action);
        },
        addItem: (input) => {
            if(input.trim() !== "") {
                action = { type: constants.ADD_ITEM }
                dispatch(action);
            }
            else {
                alert("please write an item to do");
            }
        },
        changeItemStatus: (id) => {
            action = { type: constants.CHANGE_ITEM_STATUS, id: id };
            dispatch(action);
        },
        deleteItems: () => {
            action = { type: constants.DELETE_ITEMS }
            dispatch(action);
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(TodoList);
