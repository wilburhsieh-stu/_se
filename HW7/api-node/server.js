const express = require('express');
const app = express();

app.use(express.json());

// API 路由
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'System is running' });
});

app.post('/api/data', (req, res) => {
  const { name } = req.body;
  if (!name) return res.status(400).json({ error: 'Name is required' });
  res.status(201).json({ success: true, name });
});

// 匯出 app 以供測試使用 (不直接 listen)
module.exports = app;

if (require.main === module) {
  app.listen(3000, () => console.log('API Server running on port 3000'));
}
