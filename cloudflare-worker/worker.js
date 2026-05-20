export default {
  async scheduled(event, env, ctx) {
    const RAILWAY_URL = env.RAILWAY_URL
    
    try {
      const response = await fetch(`${RAILWAY_URL}/health`, {
        method: 'GET',
        headers: {
          'User-Agent': 'Cloudflare-Worker-Keep-Alive'
        }
      })
      
      console.log(`Keep-alive ping sent to Railway at ${new Date().toISOString()}`)
      console.log(`Status: ${response.status}`)
      
      return new Response('OK', { status: 200 })
    } catch (error) {
      console.error('Keep-alive failed:', error)
      return new Response('Error', { status: 500 })
    }
  }
}
