-- ========================================
-- MySQL元数据库初始化脚本
-- ========================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS agriculture CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agriculture;

-- ========================================
-- 产品维度表
-- ========================================
CREATE TABLE IF NOT EXISTS dim_product (
    product_id VARCHAR(32) PRIMARY KEY COMMENT '产品ID',
    product_name VARCHAR(100) NOT NULL COMMENT '产品名称',
    category_id VARCHAR(16) NOT NULL COMMENT '分类ID',
    category_name VARCHAR(50) NOT NULL COMMENT '分类名称',
    spec VARCHAR(50) COMMENT '规格',
    unit VARCHAR(10) NOT NULL DEFAULT '千克' COMMENT '单位（千克/斤）',
    description TEXT COMMENT '产品描述',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category_id),
    INDEX idx_name (product_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品维度表';

-- ========================================
-- 市场维度表
-- ========================================
CREATE TABLE IF NOT EXISTS dim_market (
    market_id VARCHAR(32) PRIMARY KEY COMMENT '市场ID',
    market_name VARCHAR(100) NOT NULL COMMENT '市场名称',
    market_type VARCHAR(20) NOT NULL COMMENT '市场类型（批发/零售）',
    region_id VARCHAR(16) NOT NULL COMMENT '地区ID',
    address VARCHAR(200) COMMENT '详细地址',
    latitude DECIMAL(10,6) COMMENT '纬度',
    longitude DECIMAL(10,6) COMMENT '经度',
    contact VARCHAR(50) COMMENT '联系方式',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='市场维度表';

-- ========================================
-- 地区维度表
-- ========================================
CREATE TABLE IF NOT EXISTS dim_region (
    region_id VARCHAR(16) PRIMARY KEY COMMENT '地区ID',
    region_name VARCHAR(50) NOT NULL COMMENT '地区名称',
    province VARCHAR(20) NOT NULL COMMENT '省份',
    city VARCHAR(20) NOT NULL COMMENT '城市',
    district VARCHAR(20) COMMENT '区县',
    level TINYINT(1) NOT NULL COMMENT '行政级别',
    parent_id VARCHAR(16) COMMENT '上级地区ID',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_province (province),
    INDEX idx_city (city),
    INDEX idx_parent (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地区维度表';

-- ========================================
-- 用户表
-- ========================================
CREATE TABLE IF NOT EXISTS sys_user (
    user_id VARCHAR(32) PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(100) NOT NULL COMMENT '密码（加密）',
    real_name VARCHAR(50) COMMENT '真实姓名',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    role_id VARCHAR(16) NOT NULL COMMENT '角色ID',
    status TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态（1启用/0禁用）',
    last_login_time DATETIME COMMENT '最后登录时间',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ========================================
-- 角色表
-- ========================================
CREATE TABLE IF NOT EXISTS sys_role (
    role_id VARCHAR(16) PRIMARY KEY COMMENT '角色ID',
    role_name VARCHAR(50) NOT NULL COMMENT '角色名称',
    role_code VARCHAR(50) NOT NULL COMMENT '角色编码',
    description VARCHAR(200) COMMENT '角色描述',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- ========================================
-- 系统配置表
-- ========================================
CREATE TABLE IF NOT EXISTS sys_config (
    config_key VARCHAR(100) PRIMARY KEY COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    config_type VARCHAR(20) NOT NULL COMMENT '配置类型',
    description VARCHAR(200) COMMENT '配置描述',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

-- ========================================
-- 插入初始数据
-- ========================================

-- 插入地区数据
INSERT INTO dim_region (region_id, region_name, province, city, district, level, parent_id) VALUES
('R000', '贵州省', '贵州省', '贵州省', NULL, 1, NULL),
('R001', '贵阳市', '贵州省', '贵阳市', NULL, 2, 'R000'),
('R00101', '云岩区', '贵州省', '贵阳市', '云岩区', 3, 'R001'),
('R00102', '南明区', '贵州省', '贵阳市', '南明区', 3, 'R001'),
('R00103', '花溪区', '贵州省', '贵阳市', '花溪区', 3, 'R001'),
('R00104', '乌当区', '贵州省', '贵阳市', '乌当区', 3, 'R001'),
('R00105', '白云区', '贵州省', '贵阳市', '白云区', 3, 'R001'),
('R00106', '观山湖区', '贵州省', '贵阳市', '观山湖区', 3, 'R001'),
('R00107', '清镇市', '贵州省', '贵阳市', '清镇市', 3, 'R001'),
('R00108', '修文县', '贵州省', '贵阳市', '修文县', 3, 'R001'),
('R00109', '息烽县', '贵州省', '贵阳市', '息烽县', 3, 'R001'),
('R00110', '开阳县', '贵州省', '贵阳市', '开阳县', 3, 'R001'),
('R002', '遵义市', '贵州省', '遵义市', NULL, 2, 'R000'),
('R003', '六盘水市', '贵州省', '六盘水市', NULL, 2, 'R000'),
('R004', '安顺市', '贵州省', '安顺市', NULL, 2, 'R000'),
('R005', '毕节市', '贵州省', '毕界市', NULL, 2, 'R000'),
('R006', '铜仁市', '贵州省', '铜仁市', NULL, 2, 'R000'),
('R007', '黔西南州', '贵州省', '黔西南州', NULL, 2, 'R000'),
('R008', '黔东南州', '贵州省', '黔东南州', NULL, 2, 'R000'),
('R009', '黔南州', '贵州省', '黔南州', NULL, 2, 'R000');

-- 插入角色数据
INSERT INTO sys_role (role_id, role_name, role_code, description) VALUES
('ROLE_ADMIN', '管理员', 'ADMIN', '系统管理员，拥有所有权限'),
('ROLE_USER', '普通用户', 'USER', '普通用户，只能查看数据'),
('ROLE_ANALYST', '分析师', 'ANALYST', '数据分析师，可以进行分析和导出');

-- 插入默认管理员用户（密码：admin123）
INSERT INTO sys_user (user_id, username, password, real_name, role_id, status) VALUES
('U0001', 'admin', '$2a$10$N9q0C1QPKlRW3QjAdy2z3K3Y3uK3l3i3j3h3g3f3d3s3a3', '系统管理员', 'ROLE_ADMIN', 1);

-- 插入系统配置
INSERT INTO sys_config (config_key, config_value, config_type, description) VALUES
('system.name', '农产品价格监测系统', 'string', '系统名称'),
('system.version', '1.0.0', 'string', '系统版本'),
('alert.enabled', 'true', 'boolean', '是否启用预警'),
('alert.email', 'admin@example.com', 'string', '预警通知邮箱'),
('prediction.days', '7', 'integer', '预测天数');

-- ========================================
-- 显示创建的表
-- ========================================
SHOW TABLES;
