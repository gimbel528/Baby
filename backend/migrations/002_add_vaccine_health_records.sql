-- ======================
-- 1. 更新 modules 表，添加 module_type 字段
-- ======================
ALTER TABLE modules ADD COLUMN IF NOT EXISTS module_type TEXT DEFAULT 'custom';

-- 为预设的三个模块设置类型
UPDATE modules SET module_type = 'checklist' WHERE name = '待产包';
UPDATE modules SET module_type = 'vaccine' WHERE name = '疫苗记录';
UPDATE modules SET module_type = 'health' WHERE name = '健康档案';

-- ======================
-- 2. 创建疫苗记录表 (vaccine_records)
-- ======================
CREATE TABLE IF NOT EXISTS vaccine_records (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    module_id UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    scheduled_date DATE,
    actual_date DATE,
    status TEXT DEFAULT 'pending', -- pending, done, missed
    notes TEXT,
    age TEXT, -- 如 "出生", "1月龄", "2月龄"
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 启用行级安全
ALTER TABLE vaccine_records ENABLE ROW LEVEL SECURITY;

-- 创建 RLS 策略
CREATE POLICY "Users can view their own vaccine records"
    ON vaccine_records FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own vaccine records"
    ON vaccine_records FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own vaccine records"
    ON vaccine_records FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own vaccine records"
    ON vaccine_records FOR DELETE
    USING (auth.uid() = user_id);

-- ======================
-- 3. 创建健康档案表 (health_records)
-- ======================
CREATE TABLE IF NOT EXISTS health_records (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    module_id UUID NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    record_type TEXT NOT NULL, -- height, weight, sick, injury, allergy, other
    title TEXT NOT NULL,
    value TEXT,
    date DATE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 启用行级安全
ALTER TABLE health_records ENABLE ROW LEVEL SECURITY;

-- 创建 RLS 策略
CREATE POLICY "Users can view their own health records"
    ON health_records FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own health records"
    ON health_records FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own health records"
    ON health_records FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own health records"
    ON health_records FOR DELETE
    USING (auth.uid() = user_id);
