-- Reference schema (SQLAlchemy creates these automatically on startup)
CREATE TABLE IF NOT EXISTS contacts (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        VARCHAR(100) NOT NULL,
  phone       VARCHAR(30)  NOT NULL,
  relation    VARCHAR(50)  DEFAULT '',
  language    VARCHAR(5)   DEFAULT 'en',      -- en | ur | sd : language of SMS sent to this contact
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  token       VARCHAR(32) UNIQUE NOT NULL,    -- used in the public tracking link
  user_name   VARCHAR(100) DEFAULT '',
  message     TEXT DEFAULT '',
  summary     TEXT DEFAULT '',
  latitude    REAL,
  longitude   REAL,
  category    VARCHAR(30) DEFAULT 'other',
  level       VARCHAR(10) DEFAULT 'low',
  priority    INTEGER DEFAULT 3,
  risk_score  INTEGER DEFAULT 0,
  language    VARCHAR(10) DEFAULT 'en',
  source      VARCHAR(10) DEFAULT 'manual',   -- manual | voice
  status      VARCHAR(20) DEFAULT 'active',   -- active | resolved
  notified    INTEGER DEFAULT 0,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
