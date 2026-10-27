# VIS10N Holdings website

Static site on Netlify. Each page has its own address, title, description, share image and Google structured data:

| Address | File |
|---|---|
| `/` | `index.html` |
| `/portfolio` | `portfolio.html` |
| `/rayj-dennis` | `rayj-dennis.html` |
| `/insight` | `insight.html` |
| `/insight/<slug>` | `insight/<slug>.html` |
| `/privacy`, `/terms` | `privacy.html`, `terms.html` |

Also generated: `404.html`, `sitemap.xml`, `robots.txt`.

## How to make changes

Do not edit the page files above directly; they are generated.

1. Edit the design and copy in `src/site.html`, or the articles in `src/posts.json`.
2. Run `python3 build.py` (standard library only).
3. Commit everything and push. Netlify publishes the folder as is.

## Adding an Insight article

Add an object to `src/posts.json`:

```json
{"slug": "my-new-post", "title": "Title", "date": "2026-11-02", "author": "RayJ Dennis",
 "cats": ["Sports"], "excerpt": "One or two sentences for search results and the listing.",
 "body": "## Heading\nParagraph text.\n- List item"}
```

In `body`, lines starting with `## ` become headings and lines starting with `- ` become list items. Run `python3 build.py`; the article gets its own page at `/insight/my-new-post` and is added to the sitemap.

## Enquiry form

Uses Netlify Forms (form name `enquiry`). Notification emails are set in Netlify under Forms → Form notifications.

## Old Squarespace addresses

`netlify.toml` redirects the old Squarespace pages (`/leadership`, `/partners`, `/blog`, and so on) to their new equivalents, so existing links and search results still land on the right page.
