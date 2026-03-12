-- スマートシティ×サステナビリティ統合プラットフォーム
-- データベース初期化SQL

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ユーザーテーブル
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IoTセンサーテーブル
CREATE TABLE IF NOT EXISTS iot_sensors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id VARCHAR(255) UNIQUE NOT NULL,
    sensor_type VARCHAR(50) NOT NULL, -- environment, traffic, energy, security, infrastructure
    location_name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, maintenance
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 環境データテーブル（メタデータ）
CREATE TABLE IF NOT EXISTS environment_data_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id UUID REFERENCES iot_sensors(id),
    data_type VARCHAR(50) NOT NULL, -- air_quality, water_quality, soil_quality, biodiversity
    measurement_type VARCHAR(100), -- PM2.5, pH, temperature, etc.
    unit VARCHAR(50),
    threshold_value DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 交通データテーブル（メタデータ）
CREATE TABLE IF NOT EXISTS traffic_data_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id UUID REFERENCES iot_sensors(id),
    location_name VARCHAR(255),
    road_type VARCHAR(50), -- highway, street, bridge, etc.
    direction VARCHAR(50), -- north, south, east, west
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- エネルギーデータテーブル（メタデータ）
CREATE TABLE IF NOT EXISTS energy_data_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id UUID REFERENCES iot_sensors(id),
    energy_type VARCHAR(50) NOT NULL, -- electricity, gas, renewable
    source_type VARCHAR(100), -- solar, wind, hydro, etc.
    capacity DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ESGレポートテーブル
CREATE TABLE IF NOT EXISTS esg_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- environment, social, governance, integrated
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'draft', -- draft, generated, published
    file_path VARCHAR(500),
    metadata JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- カーボンフットプリントテーブル
CREATE TABLE IF NOT EXISTS carbon_footprint (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    scope VARCHAR(50) NOT NULL, -- scope1, scope2, scope3
    category VARCHAR(100),
    value DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) DEFAULT 'tCO2e',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- アラートテーブル
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sensor_id UUID REFERENCES iot_sensors(id),
    alert_type VARCHAR(50) NOT NULL, -- threshold_exceeded, anomaly_detected, system_error
    severity VARCHAR(50) NOT NULL, -- low, medium, high, critical
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open', -- open, acknowledged, resolved
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 判断支援ログテーブル
CREATE TABLE IF NOT EXISTS decision_support_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    decision_type VARCHAR(100) NOT NULL,
    scenario_analysis JSONB,
    risk_assessment JSONB,
    decision_recommendation TEXT,
    decision_made TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Runbookテーブル
CREATE TABLE IF NOT EXISTS runbooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    runbook_name VARCHAR(255) NOT NULL,
    runbook_type VARCHAR(50) NOT NULL, -- environment_management, smart_city_management, disaster_response
    content TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'draft', -- draft, active, archived
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックスの作成
CREATE INDEX IF NOT EXISTS idx_iot_sensors_sensor_type ON iot_sensors(sensor_type);
CREATE INDEX IF NOT EXISTS idx_iot_sensors_status ON iot_sensors(status);
CREATE INDEX IF NOT EXISTS idx_environment_data_metadata_sensor_id ON environment_data_metadata(sensor_id);
CREATE INDEX IF NOT EXISTS idx_traffic_data_metadata_sensor_id ON traffic_data_metadata(sensor_id);
CREATE INDEX IF NOT EXISTS idx_energy_data_metadata_sensor_id ON energy_data_metadata(sensor_id);
CREATE INDEX IF NOT EXISTS idx_esg_reports_period ON esg_reports(period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_carbon_footprint_period ON carbon_footprint(period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_alerts_sensor_id ON alerts(sensor_id);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_decision_support_logs_user_id ON decision_support_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_decision_support_logs_created_at ON decision_support_logs(created_at);

-- 初期データの投入（開発用）
INSERT INTO users (username, email, hashed_password, full_name, role) VALUES
    ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Administrator', 'admin'),
    ('manager', 'manager@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Manager', 'manager'),
    ('user', 'user@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'User', 'user')
ON CONFLICT (username) DO NOTHING;

