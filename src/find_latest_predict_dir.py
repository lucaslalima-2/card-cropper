# Libraries
import os

# Finds latest prediction dir
def find_latest_predict_dir(base="runs/detect"):
	# === old
	#predict_dirs = [int(d.lstrip("predict")) for d in os.listdir(base) if d.startswith("predict")]
	# === new
	predict_dirs = list()
	for d in os.listdir(base):
		if d=="predict": predict_dirs.append(0)
		elif d.startswith("predict"): predict_dirs.append(int(d.lstrip("predict")))
		else: pass

	predict_dirs.sort(reverse=True)

	if predict_dirs:
		return os.path.join(base, "predict"+ str(predict_dirs[0]))
	return None