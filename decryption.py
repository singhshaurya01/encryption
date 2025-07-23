# DECRYPTION

key = hashlib.sha256(b"secretkey").digest()
iv_number = 10    #ONLY TWO THINGS NEEDED FOR DECRYPTION.
 

#LOADING IMAGE
image_flat, shape = load_image("Encryption_files/woman_encrypted4.tiff")
ciphertext = image_flat.tobytes()
l, b, h = shape


#FETCHING IV AND CIPHERTEXT
iv = ciphertext[iv_number*b*h:(iv_number*b*h + 16)]
ciphertext = ciphertext[:iv_number*b*h] + ciphertext[(iv_number+1)*b*h:]


#GETTING x0 and r from IV for logistic map.
x0, r = iv_to_x0_r(iv)
chaotic_seq = logistic_map(r, x0, len(image_flat))


#decrypt cyphertext to plaintext. 
plaintext = aes_decrypt(ciphertext[:(l-1)*b*h], key, iv)

#Convert byte-stream to pixel data (1d)
pixels = np.frombuffer(plaintext, dtype=np.uint8)

#unchaos pixels to retrieve original pixels and reshape it to 3-D array.
pixels_unchaosed = xor_with_chaotic(pixels, chaotic_seq).reshape(l-1, b, h)



#Convert to image and save.
decrypted_path = "Encryption_files/woman_decrypted4.tiff"
decrypted_img = Image.fromarray(pixels_unchaosed)
decrypted_img.save(decrypted_path)


img = Image.open(decrypted_path)
img.show()
img.close()



#COMPARING ORIGINAL IMAGE AND DECRYPTED IMAGE.
with Image.open("Encryption_files/woman_decrypted4.tiff") as img:
    decrypted_pixels = np.array(img)
    
with Image.open("Encryption_files/woman.tiff") as img:
    original_pixels = np.array(img)
    
np.array_equal(decrypted_pixels, original_pixels)
