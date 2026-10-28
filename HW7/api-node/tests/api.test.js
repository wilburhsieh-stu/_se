const request = require('supertest');
const app = require('../server');

// 2. 系統測試 (System / Web API Tests)
describe('Web API System Tests', () => {
  
  test('GET /api/health 應該回傳 200 與系統狀態', async () => {
    const res = await request(app).get('/api/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('POST /api/data 應該驗證必填欄位', async () => {
    const res = await request(app).post('/api/data').send({});
    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBe('Name is required');
  });
  
  test('POST /api/data 成功時應該回傳 201', async () => {
    const res = await request(app).post('/api/data').send({ name: 'TestUser' });
    expect(res.statusCode).toBe(201);
    expect(res.body.success).toBe(true);
  });
});
