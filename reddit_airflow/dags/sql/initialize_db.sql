CREATE TABLE IF NOT EXISTS "reddit_posts" (
	"id" VARCHAR(20) PRIMARY KEY, 
	"title" TEXT NOT NULL,
	"selftext" TEXT NOT NULL,
	"num_comments" INTEGER,
	"created_utc" TIMESTAMP,
	"upvote_ratio" NUMERIC(3, 2), 
	"permalink" TEXT,
	"created_at" TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS "reddit_comments" (
	"id" VARCHAR(20) PRIMARY KEY, 
	"post_id" VARCHAR(20),
	"text" TEXT NOT NULL,
	"created_utc" TIMESTAMP,
	"ups" INTEGER, 
	"downs" INTEGER,
	"likes" INTEGER,
	"created_at" TIMESTAMP DEFAULT NOW(),
	CONSTRAINT fk_posts
		FOREIGN KEY(post_id)
			REFERENCES reddit_posts(id)
);

CREATE TABLE IF NOT EXISTS "reddit_docs" (
	"doc_id" VARCHAR(20) NOT NULL, 
	"document" TEXT NOT NULL, 
	"created_at" TIMESTAMP DEFAULT NOW(),
	CONSTRAINT fk_posts
		FOREIGN KEY(doc_id)
			REFERENCES reddit_posts(id)
);
