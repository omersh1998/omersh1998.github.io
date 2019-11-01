import React from 'react';


function DisplayItems(props) {
    return (
      <div>
        {props.items.map((item) => <li onClick={() => props.changeItemStatus(item.id)} key={item.id}>{item.text}</li>)}
      </div>
    );
}


export default DisplayItems;
