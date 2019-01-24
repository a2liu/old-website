from scripts.new_post import make_post
from scripts.utils import gitdiff_convert

"""
make_post(
    title, display_title=None,date=None, categories=[], tags=[],
    is_draft = True, has_assets = True)
"""
title = "Meeting Notes" # Will raise exception if None
display_title = None
date = "2019-01-25"
categories = [
    'bugs-nyu'
]

tags = [
    'yacs','ideas','meeting','eboard'
]

make_post(title, display_title=display_title, date=date, categories = categories, tags = tags)

#path =
# gitdiff_convert(path)
