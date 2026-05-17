import { createClient } from '@supabase/supabase-js'

// 从 Supabase 后台 Settings → API 复制这两个值
const SUPABASE_URL = 'https://hxgljdlvhnqhuujfjgpq.supabase.co'
const SUPABASE_ANON_KEY = 'sb_publishable_aNDSsfln80e8IeBn2UPDRQ_fEp3Ob6Z'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)