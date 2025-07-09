import { useState, useEffect } from 'react';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket('wss://people2025.orbdent.com/ws/chat');
    websocket.onopen = () => console.log('Connected');
    websocket.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };
    setWs(websocket);
    return () => websocket.close();
  }, []);

  const sendMessage = () => {
    if (ws && message) {
      ws.send(message);
      setMessage('');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Chat</h2>
      <div className="bg-white p-4 rounded-lg shadow-lg h-96 overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className="mb-2">{msg}</div>
        ))}
      </div>
      <div className="mt-4 flex">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={sendMessage}
          className="ml-2 bg-blue-500 text-white p-2 rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chat;
