def send_drop_box(source, rezult):
    
    CHUNK_SIZE = 150 * 1024 * 1024
    
    try:
        file_size = os.path.getsize(source)
        f = open(source, 'rb')
    except:
        print("Exception, file not detected", source)
        return 0
    
    if file_size <= CHUNK_SIZE:
        try:
            
            dbx.files_upload(f.read(), rezult, mode=WriteMode('overwrite'))
            
        except:
            print("Exception ", rezult)
  
    else:
               
        upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                   offset=f.tell())
        commit = dropbox.files.CommitInfo(path=rezult)
        
        try:
            while f.tell() < file_size:
                
                if ((file_size - f.tell()) <= CHUNK_SIZE) :
                    dbx.files_upload_session_finish(f.read(CHUNK_SIZE),
                                                    cursor,
                                                    commit)
                else:
                    dbx.files_upload_session_append(f.read(CHUNK_SIZE),
                                                    cursor.session_id,
                                                    cursor.offset)
                    cursor.offset = f.tell()  
        except:
            print("Exception", source)
    
    f.close()
    del f