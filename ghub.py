# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
# Several functions that upload data to
# github storage.
# Authentification is done via token. The token is stored in a
# separate file.

# The code in this file is appropriated from publicly available
# snippet which can be found here:
# https://stackoverflow.com/questions/50071841/how-to-push-local-files-to-github-using-python-or-post-a-commit-via-python

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
from base64 import b64encode
import os
# pip install
from github import Github, UnknownObjectException
from github import InputGitTreeElement
# same project

def readf( path, encoding='utf-8' ):

    # Reads a file.

    with open( path, 'r', encoding=encoding ) as f:
        text = f.read()
        log.info( 'read file %s'%path )
        return text
    
def read_base64_image_as_string( path, encoding='utf-8' ):
    
    # help:
    # https://stackoverflow.com/questions/50071841/how-to-push-local-files-to-github-using-python-or-post-a-commit-via-python
    # https://stackoverflow.com/questions/58300101/illegal-multibyte-sequence-error-from-beautifulsoup-when-python-3
    # https://pythonexamples.org/python-bytes-to-string/
    
    with open( path, 'rb' ) as input_file:
        data = input_file.read()
        return b64encode(data).decode( encoding )
    
def login_into_repo( repo_name ):
    
    # Logs in into my github account and returns
    # selected repository.
    
    # login and choose a repository
    g = Github( readf('token') )
    repo = g.get_user().get_repo( repo_name )
    
    return repo

def list_files_in_github( root ):
    
    # help:
    # https://pygithub.readthedocs.io/en/latest/examples/Repository.html
    
    repo = login_into_repo( 'co1111k2_storage' )
    
    try:
        
        contents = repo.get_contents( root )
        paths = []
        for content_file in contents:
            paths.append( content_file.path )
            
        return paths
    
    except UnknownObjectException:
        # such root folder doesnt exist yet
        return []
    
def load_file_from_github( src ):
    
    # Read file from persistent
    # storage --- private repository.
    
    # help:
    # https://medium.com/geekculture/files-on-heroku-cd09509ed285
    
    repo = login_into_repo( 'co1111k2_storage' )

    data = repo.get_contents(src)
    
    return data.decoded_content.decode()
    
def write_file_to_github( dest, data ):
    
    # Save file to persistent
    # storage --- private repository.
    
    # help:
    # https://medium.com/geekculture/files-on-heroku-cd09509ed285
    
    repo = login_into_repo( 'co1111k2_storage' )
        
    commit_message = 'automatic send'
    
    repo.create_file( dest, commit_message, data, branch="master" )
    
def upload_stats_to_github( srcs ):
    
    # Uploads data gathered during the experiment to persistent
    # storage --- private repository.
    
    repo = login_into_repo( 'co1111k2_storage' )
    
    # get destinations from full paths
    dests = []
    for src in srcs:
        _,f = os.path.split(src)
        dests.append( 's/%s'%f ) # unix path separator
        
    commit_message = 'automatic upload'
    master_ref = repo.get_git_ref( 'heads/master' )
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    
    element_list = list()
    for iloc, src in enumerate(srcs):
        src_data = readf(src)
        element = InputGitTreeElement( dests[iloc], '100644', 'blob', src_data )
        element_list.append(element)
    
    tree = repo.create_git_tree( element_list, base_tree )
    parent = repo.get_git_commit( master_sha )
    commit = repo.create_git_commit( commit_message, tree, [parent] )
    master_ref.edit( commit.sha )
    
def upload_images_to_github( srcs ):
    
    # Uploads user generated pictures to persistent
    # storage --- private repository.
    
    # I expect all files passed here to be .png images.
    
    repo = login_into_repo( 'co1111k2_storage' ) #'co1111k2_images' )
    
    # get destinations from full paths
    dests = []
    for src in srcs:
        root,f = os.path.split(src)
        _,subfolder = os.path.split(root)
        dests.append( '%s/%s'%(subfolder,f) ) # unix path separator
      
    commit_message = 'automatic upload'
    
    for iloc, src in enumerate(srcs):
        src_data = read_base64_image_as_string(src)
        
        # i failed to upload binary images as actual binary images that
        # can be viewed html with <img src=...> tag ---
        # i can only upload .png files as base64 string.
        # decoding it with javascript is too problematic,
        # so uploaded images will not be used in the final product
        
        repo.create_file( dests[iloc], commit_message, src_data, branch="master" )

#---------------------------------------------------------------------------+++
# end 2022.04.10
# created