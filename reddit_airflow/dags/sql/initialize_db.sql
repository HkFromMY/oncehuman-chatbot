CREATE TABLE IF NOT EXISTS "reddit_posts" (
	"subreddit_id" VARCHAR(255), 
	"title" TEXT,
	"text" TEXT,
	"comments" TEXT,
	"post_date" TIMESTAMP,
	"created_at" TIMESTAMP DEFAULT NOW()
);