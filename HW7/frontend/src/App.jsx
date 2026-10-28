import React, { useState } from 'react';

function App() {
  const [tested, setTested] = useState(false);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>CI/CD Test Dashboard</h1>
      <p>目前系統狀態：連線正常</p>
      
      <button onClick={() => setTested(true)}>開始測試</button>

      {tested && (
        <div className="test-results" style={{ marginTop: '20px', padding: '10px', background: '#eee' }}>
          <h3>測試結果：</h3>
          <ul>
            <li>✅ Rust 單元測試 (Unit) - 通過</li>
            <li>✅ Node.js API 測試 (System) - 通過</li>
            <li>✅ Playwright E2E 測試 - 通過</li>
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
