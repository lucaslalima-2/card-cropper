# Libraries
import os

# Finds latest prediction dir
def find_latest_predict_dir(base="runs/detect"):
	predict_dirs = [int(d.lstrip("predict")) for d in os.listdir(base) if d.startswith("predict")]
	predict_dirs.sort(reverse=True)
	if predict_dirs:
		return os.path.join(base, "predict"+ str(predict_dirs[0]))
	return None