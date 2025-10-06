# card-cropper
# Problem
I have been trying to sell my baseball card collection on eBay. The photo-cropping process has been a painful one.
My printer (HP Envy 6055) allows for relatively quick scans. It packages all scans into a folder that I can save.
It would be convenient if I could feed that folder into a script and have code auto-crop them. This would make posting to eBay faster.

# Training command:
* yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=50 imgsz=640



# Future Updates
After accumulating many scans, train an AI model to crop batches full for me. 
Currently I am only scanning one card, one side at a time.
If I could do batches of 9 at a time, I could speed up this process.
But, through image recognition, AI would help define where a card starts and ends amongst a batch scan.