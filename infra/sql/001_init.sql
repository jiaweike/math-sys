CREATE TABLE IF NOT EXISTS theorem (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  aliases VARCHAR(255),
  statement_latex TEXT NOT NULL,
  proof_md TEXT NOT NULL,
  conditions TEXT,
  tags VARCHAR(255),
  refs TEXT
);

CREATE TABLE IF NOT EXISTS formula (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  latex TEXT NOT NULL,
  meaning TEXT NOT NULL,
  constraints TEXT,
  examples TEXT,
  refs TEXT
);

CREATE TABLE IF NOT EXISTS algo (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  complexity VARCHAR(100),
  pseudocode TEXT
);

CREATE TABLE IF NOT EXISTS theorem_dependency (
  id SERIAL PRIMARY KEY,
  theorem_id INTEGER NOT NULL REFERENCES theorem(id),
  depends_on_theorem_id INTEGER NOT NULL REFERENCES theorem(id)
);
