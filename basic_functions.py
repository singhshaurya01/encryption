from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def load_image(path): #------- STEP 1: Load image and get flattened image data.
    img = Image.open(path).convert("RGB")  # grayscale
    img_array = np.array(img)
    shape = img_array.shape
    flat = img_array.flatten() #3d->1d
    return flat, shape


def iv_to_x0_r(iv): #------- STEP 2: Get initial logistic maps condition, IV DEPENDENT.
    hash_digest = hashlib.sha256(iv).digest()
    
    x0_int = int.from_bytes(hash_digest[:8], byteorder='big')# ---- Use 8 bytes for x0
    x0 = (x0_int % 10**12) / 10**12  # Ensure in (0,1)

    r_int = int.from_bytes(hash_digest[8:16], byteorder='big')#---- Use next 8 bytes for r
    r = 3.6 + (r_int % 400000) / 1000000.0  # r in (3.6, 4.0)

    return x0, r



def logistic_map(r, x0, size): #------STEP 3: gets a chaotic keystream for encryption.
    x = x0
    seq = []
    for _ in range(size):
        x = r * x * (1 - x)
        seq.append(x)
    return (np.array(seq) * 256).astype(np.uint8)



def xor_with_chaotic(image_flat, chaotic_seq): # ------STEP 4: XOR IMAGE DATA with Chaotic Sequence (keystream)
    return np.bitwise_xor(image_flat, chaotic_seq[:len(image_flat)])



def aes_encrypt(data, key, iv): # ---------- STEP 5: encrypt the chaotic image data using CBC.
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data, AES.block_size))



def save_encrypted_image(ciphertext, shape, path): # ------ STEP 6: Save Image from Ciphertext.
    l, b, h = shape
    encrypted_pixels = np.frombuffer(ciphertext[:(l+1)*b*h], dtype=np.uint8).reshape(l+1, b, h)#bytes -> 2d array
                                                                                      #one extra line for IV.
    encrypted_img = Image.fromarray(encrypted_pixels)
    encrypted_img.save(path)
    
    
    
def aes_decrypt(ciphertext, key, iv): # ------- TO GET ORIGINAL IMAGE - DECRYPT AND XOR.
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(ciphertext)

