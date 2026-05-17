-- 用户配置表
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  avatar_url TEXT,
  role TEXT DEFAULT 'parent' CHECK (role IN ('parent', 'family', 'viewer')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 倒计时事件表
CREATE TABLE IF NOT EXISTS countdown_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  event_name TEXT NOT NULL,
  target_date TIMESTAMP WITH TIME ZONE NOT NULL,
  event_type TEXT DEFAULT 'custom' CHECK (event_type IN ('birth', 'birthday', 'milestone', 'custom')),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 信件表
CREATE TABLE IF NOT EXISTS letters (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  unlock_date TIMESTAMP WITH TIME ZONE,
  reminder_date TIMESTAMP WITH TIME ZONE,
  is_unlocked BOOLEAN DEFAULT false,
  is_reminded BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 孕妇餐记录表
CREATE TABLE IF NOT EXISTS meals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  meal_date DATE NOT NULL,
  meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  description TEXT,
  image_url TEXT,
  nutrition_tags TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 技术文章表
CREATE TABLE IF NOT EXISTS articles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  category TEXT,
  tags TEXT[],
  published_at TIMESTAMP WITH TIME ZONE,
  view_count INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_countdown_events_user_id ON countdown_events(user_id);
CREATE INDEX idx_countdown_events_is_active ON countdown_events(is_active);
CREATE INDEX idx_letters_user_id ON letters(user_id);
CREATE INDEX idx_letters_unlock_date ON letters(unlock_date);
CREATE INDEX idx_meals_user_id ON meals(user_id);
CREATE INDEX idx_meals_meal_date ON meals(meal_date);
CREATE INDEX idx_articles_user_id ON articles(user_id);

-- 启用行级安全策略 (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE countdown_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE letters ENABLE ROW LEVEL SECURITY;
ALTER TABLE meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

-- profiles 表策略
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- countdown_events 表策略
CREATE POLICY "Users can view own countdown events"
  ON countdown_events FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own countdown events"
  ON countdown_events FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own countdown events"
  ON countdown_events FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own countdown events"
  ON countdown_events FOR DELETE
  USING (auth.uid() = user_id);

-- letters 表策略
CREATE POLICY "Users can view own letters"
  ON letters FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own letters"
  ON letters FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own letters"
  ON letters FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own letters"
  ON letters FOR DELETE
  USING (auth.uid() = user_id);

-- meals 表策略
CREATE POLICY "Users can view own meals"
  ON meals FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own meals"
  ON meals FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own meals"
  ON meals FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own meals"
  ON meals FOR DELETE
  USING (auth.uid() = user_id);

-- articles 表策略
CREATE POLICY "Users can view own articles"
  ON articles FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own articles"
  ON articles FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own articles"
  ON articles FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own articles"
  ON articles FOR DELETE
  USING (auth.uid() = user_id);

-- 创建触发器：新用户注册时自动创建 profile
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
