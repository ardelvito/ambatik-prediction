from flask import Flask, render_template, request, jsonify
# from keras.preprocessing import image
from werkzeug.utils import secure_filename
from werkzeug.utils import send_from_directory
import cv2 as cv
import tensorflow as tf
# import keras.utils as image
import numpy as np
import os

# try:
# 	import shutil
# 	shutil.rmtree('uploaded / image')
# 	cd uploaded
# 	mkdir image
# 	cd ..
# 	print()
# except:
# 	pass

model = tf.keras.models.load_model('ambatik-model.h5')
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploaded/'

@app.route('/')
def upload_f():
	return render_template('index.php')

def finds(filename):
	images = []
	# vals = ['Rime', 'Rainbow', 'Glaze', 'Fogsmog', 'Dew', 'Frost', 'Rain', 'Hail', 'Lightning', 'Sandstorm', 'Snow'] 
	vals = ['cendrawasih', 'geblek renteng', 'insang', 'kawung', 'mega mendung', 'parang', 'pring sedapur', 'simbut', 'sogan', 'truntum']
	path = "uploaded/" + filename
	
	# img = cv.imread(path)

	# img = cv.resize(img, (256, 256), interpolation = cv.INTER_AREA)

	# images.append(img)
	# images = np.array(images)

	img_width, img_height = 256, 256
	img = tf.keras.utils.load_img(path, target_size = (img_width, img_height))
	img = tf.keras.utils.img_to_array(img)
	img = np.expand_dims(img, axis = 0)

	pred = model.predict(img)
	
	pred_index = np.argmax(pred[0])
	result = {'types': vals[pred_index], 'accuracy': pred[0][pred_index] * 100}
	# result = (vals[pred_index] + ": " + str(pred[0][pred_index] * 100) + "%")

	# print(pred)
	# return str(vals[pred_index])
	return result 

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
		val = finds(f.filename)
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
		# return render_template('result.php', ss = val)
		return jsonify(val)
if __name__ == '__main__':
	app.run()
