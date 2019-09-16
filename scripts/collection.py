import os
import logging
import re
import json
from scripts.vars import COLLECTIONS_DIR

class Collection:

    format_string = '%Y-%m-%d'
    multiple_dashes_regex = re.compile('[\s-]+')

    new_post_format = re.sub('\n +', '\n', """---
        title: %s
        categories: [%s]
        tags: [%s]
        ---
        <!-- {%% raw %%} -->
        <!-- {%% include refc-small.html text="ref commit" commit="3cad965..." %%} -->
        <!-- {%% include ref-commit.html text="ref commit" commit="3cad965..." %%} -->
        <!-- {%% endraw %%} -->
    """)

    def __init__(self, name):
        self.name = name
        if not os.path.exists(self.path):
            logging.info("Collection didn't exist, made empty folder.")
            os.mkdir(self.path)

        self.logger = logging.getLogger(f'collection-{name}')

    # Path of the collection
    @property
    def path(self):
        return os.path.join(COLLECTIONS_DIR, '_'+self.name)

    # Where an entry's includes should be
    @property
    def include_path(self, **entry):
        if entry == None:
            return None # Eventually return the location of the includes folder
        raise NotImplementedError()

    # Adds an item to this collection, and returns the path of the new item.
    # Item should not be an element already in the collection.
    def add_item(self, _strict=True, **entry):
        self.logger.info(\
                f'`add_item` called with\n  _strict=`{_strict}`\n  attributes=`{entry}`')

        str_attr = ['title']
        list_attr = ['categories', 'tags']
        attributes = ['title', 'date', 'categories', 'tags']

        def map(attr_list, func, default):
             return (func(entry[attr]) if attr in entry else default for attr in attr_list)

        (title,) = map(str_attr, lambda s: s.strip(), '')
        (categories, tags) = map(list_attr, lambda l: ','.join((s.strip() for s in l)), '')

        assert title != ''

        if 'date' in entry:
            try:
                date = entry['date'].strftime(Collection.format_string) + '-'
            except AttributeError:
                date = entry['date'] + '-'

        else:
            date = ''

        slug = date + Collection.multiple_dashes_regex.sub('-', title).lower()
        path = os.path.join(self.path, slug + '.md')

        if os.path.exists(path):
            self.logger.info(f'path `{path}` already exists.')
            raise Exception("Output path already existed!")
        else:
            post_text = Collection.new_post_format % (title, categories, tags)
            with open(path, 'x') as f:
                f.write(post_text)
            return path

    def list_items(self):
        items = []
        for path in [path for path in os.listdir(self.path) if not path.startswith('.')]:
            logging.info(f"Opening {path}")
            with open(os.path.join(self.path, path), 'r') as f:
                txt = f.read()

            (_, yaml, *text) = txt.split('---\n', 3)
            attributes = json.loads('{"' + yaml.strip().replace(': ', '":"').replace('\n','","') + '"}')
            attributes = {k:[*v.strip()[1:-1].split(',')] if v.startswith('[') else v for k,v in attributes.items() }
            items.append({"attributes":attributes, "text":text})
        return items

    def __str__(self):
        return f"Collection({self.name})"

    add_entry = add_item