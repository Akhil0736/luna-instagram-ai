-- Luna AI Supabase Database Schema
-- Run this in your Supabase SQL editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User profiles table
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Profile info
  email TEXT UNIQUE,
  instagram_handle TEXT,
  business_type TEXT CHECK (business_type IN ('personal', 'business', 'creator')),
  niche TEXT,

  -- Account metrics
  follower_count INTEGER DEFAULT 0,
  engagement_rate REAL DEFAULT 0.0,
  posting_frequency INTEGER DEFAULT 0,

  -- JSON data
  preferences JSONB DEFAULT '{}',
  goals JSONB DEFAULT '{}'
);

-- Memory contexts table
CREATE TABLE memory_contexts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Memory data
  context_type TEXT NOT NULL,
  context_data JSONB NOT NULL,

  -- Metadata
  confidence_score REAL DEFAULT 1.0,
  is_active BOOLEAN DEFAULT true
);

-- User interactions table
CREATE TABLE user_interactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  session_id UUID NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- Interaction data
  query TEXT NOT NULL,
  query_type TEXT NOT NULL,
  confidence INTEGER NOT NULL,
  response TEXT NOT NULL,
  modules_used JSONB DEFAULT '[]',

  -- Context and metrics
  account_context JSONB DEFAULT '{}',
  processing_time_ms INTEGER,

  -- Feedback
  user_rating INTEGER CHECK (user_rating BETWEEN 1 AND 5),
  user_feedback TEXT
);

-- Strategies table
CREATE TABLE strategies (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Strategy details
  strategy_type TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  implementation_plan JSONB NOT NULL,

  -- Tracking
  status TEXT DEFAULT 'planned' CHECK (status IN ('planned', 'active', 'completed', 'paused')),
  start_date TIMESTAMPTZ,
  end_date TIMESTAMPTZ,

  -- Results
  initial_metrics JSONB DEFAULT '{}',
  current_metrics JSONB DEFAULT '{}',
  success_score REAL CHECK (success_score BETWEEN 0.0 AND 1.0)
);

-- Indexes for performance
CREATE INDEX idx_user_profiles_email ON user_profiles(email);
CREATE INDEX idx_user_profiles_instagram_handle ON user_profiles(instagram_handle);
CREATE INDEX idx_memory_contexts_user_id ON memory_contexts(user_id);
CREATE INDEX idx_memory_contexts_type ON memory_contexts(context_type);
CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_session ON user_interactions(session_id);
CREATE INDEX idx_user_interactions_created_at ON user_interactions(created_at DESC);
CREATE INDEX idx_strategies_user_id ON strategies(user_id);
CREATE INDEX idx_strategies_status ON strategies(status);

-- Row Level Security (RLS) policies
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_contexts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_interactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE strategies ENABLE ROW LEVEL SECURITY;

-- RLS Policies (users can only access their own data)
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own memory" ON memory_contexts
  FOR ALL USING (user_id = auth.uid());

CREATE POLICY "Users can view own interactions" ON user_interactions
  FOR ALL USING (user_id = auth.uid());

CREATE POLICY "Users can view own strategies" ON strategies
  FOR ALL USING (user_id = auth.uid());

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memory_contexts_updated_at BEFORE UPDATE ON memory_contexts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_strategies_updated_at BEFORE UPDATE ON strategies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
