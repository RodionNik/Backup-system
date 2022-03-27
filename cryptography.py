from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes

recipient_key = RSA.import_key(open("public_key.pem").read())
private_key = RSA.import_key(open("private_key.pem").read())
size_private_key = private_key.size_in_bytes()

#cipher block
CHUNK_SIZE = 150*1024*1024

def encripted_file(source, result):
      
    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    session_key = get_random_bytes(16)
    enc_session_key = cipher_rsa.encrypt(session_key)
    
    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    
    file_out = open(result, "wb")
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce)]
          
    f = open(source, 'rb')
    while True:
        data = f.read(CHUNK_SIZE)  
        if not data:
            break
        ciphertext = cipher_aes.encrypt(data)
        file_out.write(ciphertext)
        
    tag = cipher_aes.digest()
    file_out.write(tag)
    
    file_out.close()
    f.close()
	
	
def decripted_file(source, result):
    
    file_in = open(source, "rb")
    file_size = Path(source).stat().st_size
    
    #size_private_key = private_key.size_in_bytes()
    enc_session_key, nonce = [ file_in.read(x) for x in (size_private_key, 16) ]
    #len_ciphertext = file_size - size_private_key - 16 - 16
    
    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    file_out = open(result, "wb")
    
    while True:
        
        if file_size - file_in.tell() <= CHUNK_SIZE - 16 :
            #CHUNK_SIZE = file_size - file_in.tell() - 16 
            data = file_in.read(file_size - file_in.tell() - 16 )
            block_ciphertext = cipher_aes.decrypt(data)
            file_out.write(block_ciphertext)
            break
    
        data = file_in.read(CHUNK_SIZE)  
        if not data:
            break
            
        block_ciphertext = cipher_aes.decrypt(data)
        file_out.write(block_ciphertext)
    
    tag = file_in.read()
    
    try:
        cipher_aes.verify(tag)
        print("Success, file decripted")
    except:
        print("Failure, the file has been modified")
        
    file_out.close() 