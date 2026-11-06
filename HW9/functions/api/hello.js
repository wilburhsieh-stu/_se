export async function onRequest(context) {
  // 建立回傳的 JSON 資料
  const responseBody = {
    message: "你好！這是來自 Cloudflare 全球邊緣節點 (Edge Network) 的即時回應 🌍",
    timestamp: new Date().toISOString()
  };

  // 回傳 HTTP Response
  return new Response(JSON.stringify(responseBody), {
    headers: { 
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    }
  });
}
