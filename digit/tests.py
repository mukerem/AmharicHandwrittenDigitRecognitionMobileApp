import os
import requests
# from digit.noise import detect_noise

import json
root_path = '/home/andalus/Documents/MSc/Thesis/Hand written/Dataset/Digits/'
f = open("/home/andalus/Documents/MSc/Thesis/Hand written/Dataset/Crop/major_noise.json", "r")
major = json.load(f)
f.close()
f = open("/home/andalus/Documents/MSc/Thesis/Hand written/Dataset/Crop/minor_noise.json", "r")
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



url = "http://127.0.0.1:8001/api/digit/recognition/batch/"
root_path = '/home/andalus/Documents/MSc/Thesis/Hand written/Dataset/Digits/'
all_files = []
result = {}
all_images = []
original_answer= {}
for root, dirs, files in os.walk(root_path):
    if root == root_path:
        continue
    num = os.path.basename(os.path.normpath(root))
    for file in files[:3]:
        if file.endswith(".jpg"):
            path = os.path.join(root, file)
            # if detect_noise(path):
            #     continue
            all_images.append(path)
            original_answer[path] = num
            
image = {"image": all_images}
response = requests.post(url=url, data=image)
for image, predict in response.json().items():
    ans = original_answer[image]
    success, fail = result.get(ans, (0,0))
    result[ans] = (success + (ans == predict), fail + (ans != predict))
result = list(result.items())
total_success = 0
total = 0
result.sort(key = lambda data: int(data[0]))
for num, val in result:
    success, fail = val
    acc = 100.0 * success / (success + fail)
    print("%-10s %-10d %-10d %-10d %-10.2f" % (num, success, fail, success + fail, acc))
    total_success += success
    total += success + fail
print(f"average accuracy is %.2f" % ( 100.0 * total_success / total))
print(f"accurate dataset is %d" %  total_success)
print(f"total dataset is %d" % total)

