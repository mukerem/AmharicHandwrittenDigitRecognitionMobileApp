
import json
root_path = '/home/andalus/Documents/MSc/Thesis/Hand written/Dataset/Digits/'
f = open("/home/andalus/Documents/MSc/Thesis/Hand written/Crop/major_noise.json", "r")
major = json.load(f)
f.close()
f = open("/home/andalus/Documents/MSc/Thesis/Hand written/Crop/minor_noise.json", "r")
minor = json.load(f)
f.close()
all_minor_noise = []
all_major_noise = []
for num in major:
    for image in major[num]:
        path = f"{root_path}{num}/{image}.jpg"
        all_major_noise.append(path)

for num in minor:
    for image in minor[num]:
        path = f"{root_path}{num}/{image}.jpg"
        all_minor_noise.append(path)

def detect_noise(img):
    if img in all_major_noise:
        return True
    if img in all_minor_noise:
        return True
    return False
