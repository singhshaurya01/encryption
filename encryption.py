# with Image.open("Encryption_files/woman.tiff") as img:
#     img.show()
    
# Load (STEP 1)
image_flat, shape = load_image("Encryption_files/woman.tiff")
l, b, h = shape

key = hashlib.sha256(b"secretkey").digest()
iv = AES.get_random_bytes(b*h)
iv_number = 10 # ANY NUMBER BETWEEN (0, b-16). Puri line will be for IV.


#Get r and x0 (STEP 2)
x0, r = iv_to_x0_r(iv[:16])


# Generate chaotic sequence (IV DEPENDENT) (STEP 3)
chaotic_seq = logistic_map(r, x0, len(image_flat)) # ------ remember normal pixel data is XORD to get normal chaotic pixel data.
                                                   # ----- no byte strings is used here, only pixel flattened array.
                                                    
# Chaotic XOR (STEP 4)
chaotic_image = xor_with_chaotic(image_flat, chaotic_seq)


# AES Encrypt and add IV (STEP 5)
ciphertext = aes_encrypt(chaotic_image.tobytes(), key, iv[:16])
ciphertext = ciphertext[:iv_number*b*h] + iv + ciphertext[iv_number*b*h:] #Adding IV line to ciphertext.


# Save the image and view (STEP 6)
save_encrypted_image(ciphertext, shape, "Encryption_files/woman_encrypted4.tiff")

with Image.open("Encryption_files/woman_encrypted4.tiff") as img:
    img.show()
