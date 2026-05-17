export default {
  async scheduled(event, env, ctx) {
    const SUPABASE_URL = env.SUPABASE_URL
    const SUPABASE_ANON_KEY = env.SUPABASE_ANON_KEY
    
    try {
      const response = await fetch(`${SUPABASE_URL}/rest/v1/`, {
        method: 'GET',
        headers: {
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`
        }
      })
      
      console.log(`Keep-alive ping sent at ${new Date().toISOString()}`)
      console.log(`Status: ${response.status}`)
      
      return new Response('OK', { status: 200 })
    } catch (error) {
      console.error('Keep-alive failed:', error)
      return new Response('Error', { status: 500 })
    }
  }
}
