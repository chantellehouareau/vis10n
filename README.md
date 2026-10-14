# VIS10N Holdings website

Static single-page site (Home, Portfolio, Founder, Insight) deployed on Netlify. No build step: Netlify publishes the repo root.

## Enquiry form

The "Work with us" form uses Netlify Forms (form name `enquiry`). To have every enquiry emailed to chantelle.houareau@vis10nholdings.com:

1. Deploy once so Netlify detects the form.
2. In Netlify: Site configuration → Forms → enable form detection if prompted.
3. Forms → Form notifications → Add notification → Email notification → form `enquiry` → chantelle.houareau@vis10nholdings.com.

Submissions also appear under the site's Forms tab.

## Adding an Insight article

Articles live in the `POSTS` array near the bottom of `index.html`. Add a new object at the top of the array:

```js
{slug:"my-new-post", title:"Title", date:"2026-10-20", author:"RayJ Dennis", cats:["Sports"],
 excerpt:"One or two sentences for the listing.",
 body:`## Heading
Paragraph text.
- List item`},
```

Lines starting with `## ` become headings and lines starting with `- ` become list items.
