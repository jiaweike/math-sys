ALTER TABLE theorem ADD COLUMN IF NOT EXISTS source_url TEXT;
ALTER TABLE theorem ADD COLUMN IF NOT EXISTS source_license VARCHAR(100);
ALTER TABLE theorem ADD COLUMN IF NOT EXISTS review_status VARCHAR(32) DEFAULT 'draft';

ALTER TABLE formula ADD COLUMN IF NOT EXISTS source_url TEXT;
ALTER TABLE formula ADD COLUMN IF NOT EXISTS source_license VARCHAR(100);
ALTER TABLE formula ADD COLUMN IF NOT EXISTS review_status VARCHAR(32) DEFAULT 'draft';

UPDATE theorem SET review_status = 'draft' WHERE review_status IS NULL;
UPDATE formula SET review_status = 'draft' WHERE review_status IS NULL;
