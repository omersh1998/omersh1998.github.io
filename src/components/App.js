import React from 'react';
import '../css/App.css';
import TodoList from './TodoList';
import store from '../store/'

function App() {
  return (
    <div className="App">
      <TodoList store={store}/>
    </div>
  );
}

export default App;
