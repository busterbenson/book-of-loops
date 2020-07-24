#!/usr/bin/env python3

import sys
from lettersmith import *

# Update base_url to deployment URL for publishing
if len(sys.argv) > 1 and sys.argv[1] == '--dev':
    base_url = "file:///Users/buster/projects/book-of-loops/public/"
else:
    base_url = 'https://book-of-loops.com'

site_title = 'Book of Loops'
site_css = base_url + '/' + 'main.css'

static = files.find('static/**/*')

pages = pipe(
    docs.find('**/*.md'),
    docs.remove_index,
    docs.remove_drafts,
    permalink.rel_page_permalink('.'),
    docs.uplift_frontmatter,
    docs.with_template('page.html'),
)

home = pipe(
    docs.find('index.md'),
    permalink.rel_page_permalink('.'),
    docs.uplift_frontmatter,
    docs.with_template('index.html'),
)

all_pages = pipe(
    (*pages, *home),
    wikidoc.content_markdown(base_url),
    absolutize.absolutize(base_url),
)

context = {
    'site': {
        'title': site_title,
    },
    'base_url': base_url,
    'css'     : site_css   
}

rendered_docs = pipe(
    (all_pages),
    jinjatools.jinja('templates', base_url, context)
)

write(chain(static, rendered_docs), directory='public')

print('Done!')
