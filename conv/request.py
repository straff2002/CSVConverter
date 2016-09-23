dir(request.FILES) = ['__class__', '__cmp__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__eq__', 
'__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', 
'__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', 
'__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_iteritems', '_iterlists', '_itervalues', 'appendlist', 
'clear', 'copy', 'dict', 'fromkeys', 'get', 'getlist', 'has_key', 'items', 'iteritems', 'iterkeys', 'iterlists', 'itervalues', 'keys', 
'lists', 'pop', 'popitem', 'setdefault', 'setlist', 'setlistdefault', 'update', 'values', 'viewitems', 'viewkeys', 'viewvalues'] 





dir(request) = ['COOKIES', 'FILES', 'GET', 'META', 'POST', 'REQUEST', '__class__', '__delattr__', '__dict__', 
'__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__module__', '__new__', '__reduce__', 
'__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_encoding', 
'_files', '_get_files', '_get_post', '_get_request', '_get_scheme', '_initialize_handlers', '_load_post_and_files', 
'_mark_post_parse_error', '_messages', '_post', '_post_parse_error', '_read_started', '_set_post', '_stream', 
'_upload_handlers', 'body', 'build_absolute_uri', 'close', 'csrf_processing_done', 'encoding', 'environ', 'get_full_path', 
'get_host', 'get_signed_cookie', 'is_ajax', 'is_secure', 'method', 'parse_file_upload', 'path', 'path_info', 'read', 
'readline', 'readlines', 'resolver_match', 'scheme', 'session', 'upload_handlers', 'user', 'xreadlines'] 





request.FILES.get('fileupload') = X1Contacts (copy).csv 



request.FILES.getlist('fileupload') = [<InMemoryUploadedFile: X1Contacts.csv (text/csv)>, 
<InMemoryUploadedFile: X1Contacts (copy).csv (text/csv)>] 


dir(request.FILES.get('fileupload')) = ['DEFAULT_CHUNK_SIZE', '__bool__', '__class__', '__delattr__', '__dict__', '__doc__', 
'__enter__', '__exit__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__len__', '__module__', 
'__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', 
'__subclasshook__', '__unicode__', '__weakref__', '_get_closed', '_get_name', '_get_size', '_get_size_from_underlying_file', 
'_name', '_set_name', '_set_size', '_size', 'charset', 'chunks', 'close', 'closed', 'content_type', 'content_type_extra', 
'encoding', 'field_name', 'file', 'fileno', 'flush', 'isatty', 'multiple_chunks', 'name', 'newlines', 
'open', 'read', 'readinto', 'readline', 'readlines', 'seek', 'size', 'softspace', 'tell', 'truncate', 'write', 'writelines', 'xreadlines'] 



request.POST = <QueryDict: {u'csrfmiddlewaretoken': [u'k1EB6tyTCX0LGqdnkDoNqtBMPPgjt32r'], u'fileupload': [u'', u'', u'', u'', u'', u'', u'', u''], u'config_file': [u'upload']}>


p = ['SessionMiddleware', 'CommonMiddleware', 'CsrfViewMiddleware', 'AuthenticationMiddleware', 'SessionAuthenticationMiddleware', 'MessageMiddleware', 'XFrameOptionsMiddleware', 'SecurityMiddleware', 'debug', 'request', 'auth', 'messages', 'SessionMiddleware', 'CommonMiddleware', 'CsrfViewMiddleware', 'AuthenticationMiddleware', 'SessionAuthenticationMiddleware', 'MessageMiddleware', 'XFrameOptionsMiddleware', 'SecurityMiddleware']
