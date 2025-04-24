import React, { useState, useEffect } from 'react';

const API_URL = 'https://organic-xylophone-97674v6r6q762x7r9-3001.app.github.dev/api/PackingList'; // Replace with your backend URL

function PackingList() {
  const [items, setItems] = useState([]);
  const [input, setInput] = useState('');
  const token = localStorage.getItem('token'); // or sessionStorage

  useEffect(() => {
    fetch(API_URL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => setItems(data))
      .catch(err => console.error('Error fetching items:', err));
  }, []);

  const addItem = () => {
    if (!input.trim()) return;

    fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: input.trim() }),
    })
      .then(res => res.json())
      .then(newItem => {
        setItems(prevItems => [...prevItems, newItem]);
        setInput('');
      })
      .catch(err => console.error('Error adding item:', err));
  };

  const deleteItem = (id) => {
    fetch(`${API_URL}/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(() => {
        setItems(prevItems => prevItems.filter(item => item.id !== id));
      })
      .catch(err => console.error('Error deleting item:', err));
  };

  return (
    <div className="max-w-md mx-auto p-4 bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-4">🧳 My Packing List</h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Add item..."
          className="flex-grow p-2 border rounded"
        />
        <button onClick={addItem} className="bg-blue-600 text-white px-4 py-2 rounded">
          Add
        </button>
      </div>

      <ul className="space-y-2">
        {items.map(item => (
          <li key={item.id} className="flex justify-between items-center bg-gray-100 px-3 py-2 rounded">
            <span>{item.name}</span>
            <button
              onClick={() => deleteItem(item.id)}
              className="text-red-500 hover:underline"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PackingList;
 