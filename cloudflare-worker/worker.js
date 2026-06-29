export default {
  async scheduled(event, env, ctx) {
    const RENDER_URL = env.RENDER_URL
    
    try {
      const response = await fetch(`${RENDER_URL}/health`, {
        method: 'GET',
        headers: {
          'User-Agent': 'Cloudflare-Worker-Keep-Alive'
        }
      })
      
      console.log(`Keep-alive ping sent to Render at ${new Date().toISOString()}`)
      console.log(`Status: ${response.status}`)
      
      return new Response('OK', { status: 200 })
    } catch (error) {
      console.error('Keep-alive failed:', error)
      return new Response('Error', { status: 500 })
    }
  },
  
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    
    if (url.pathname === '/health') {
      return new Response('Worker is running', { status: 200 })
    }
    
    if (url.pathname === '/ping') {
      const RENDER_URL = env.RENDER_URL
      try {
        const response = await fetch(`${RENDER_URL}/health`, {
          method: 'GET',
          headers: {
            'User-Agent': 'Cloudflare-Worker-Keep-Alive'
          }
        })
        return new Response(`Ping sent, status: ${response.status}`, { status: 200 })
      } catch (error) {
        return new Response(`Ping failed: ${error.message}`, { status: 500 })
      }
    }
    
    return new Response('Baby Keep-Alive Worker', { status: 200 })
  }
}
