-- اسکیما کامل پایگاه داده سیستم تولید محتوا
-- این اسکیما را در پایگاه داده PostgreSQL/Neon خود اجرا کنید

-- جدول پست‌های زمان‌بندی شده
CREATE TABLE scheduled_posts (
    id SERIAL PRIMARY KEY,
    source_idea_id INTEGER REFERENCES post_ideas(id),
    topic TEXT NOT NULL,
    content_linkedin TEXT NOT NULL,
    content_twitter TEXT NOT NULL,
    image_url TEXT,
    quality_score NUMERIC(3,1) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending_approval', -- pending_approval / approved / scheduled / published / rejected / failed
    scheduled_at TIMESTAMP WITH TIME ZONE,
    published_linkedin BOOLEAN DEFAULT false,
    published_twitter BOOLEAN DEFAULT false,
    linkedin_post_id TEXT,
    twitter_post_id TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- جدول ایده‌های پست استخراج شده از ترندها
CREATE TABLE post_ideas (
    id SERIAL PRIMARY KEY,
    source_creator TEXT NOT NULL,
    source_post_url TEXT NOT NULL,
    source_post_engagements INTEGER DEFAULT 0,
    topic TEXT NOT NULL,
    content_pattern TEXT NOT NULL,
    hook_type VARCHAR(50) NOT NULL, -- pain_point / counterintuitive / result / story / tip
    our_take TEXT NOT NULL,
    is_used BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- جدول آمار عملکرد هر پست
CREATE TABLE post_performance (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES scheduled_posts(id),
    platform VARCHAR(20) NOT NULL, -- linkedin / twitter
    measured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    impressions INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    engagement_rate NUMERIC(5,2) DEFAULT 0
);

-- جدول لیدهای استخراج شده از کامنت‌ها
CREATE TABLE captured_leads (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(20) NOT NULL,
    post_id INTEGER REFERENCES scheduled_posts(id),
    profile_url TEXT NOT NULL,
    profile_name TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    lead_status VARCHAR(20) DEFAULT 'new', -- new / contacted / qualified / closed / bad_fit
    is_notified_to_mehdi BOOLEAN DEFAULT false,
    captured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- جدول مانیتورینگ خطاها و سلامت سیستم
CREATE TABLE system_logs (
    id SERIAL PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    level VARCHAR(10) NOT NULL, -- INFO / WARNING / ERROR / CRITICAL
    message TEXT NOT NULL,
    stack_trace TEXT,
    resolved BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- جدول تنظیمات کلی سیستم (برای کنترل توقف اضطراری)
CREATE TABLE system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- مقدار پیش‌فرض سیستم فعال است
INSERT INTO system_settings (key, value) VALUES ('system_active', 'true');

-- ایندکس‌ها برای سرعت بالا
CREATE INDEX idx_scheduled_posts_status ON scheduled_posts(status);
CREATE INDEX idx_scheduled_posts_published ON scheduled_posts(published_linkedin, published_twitter);
CREATE INDEX idx_leads_status ON captured_leads(lead_status, is_notified_to_mehdi);
