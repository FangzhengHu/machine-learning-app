# USAGE
# Start the server:
# 	python app.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'

# import the necessary packages
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import tensorflow as tf

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None


def load_model():
	global model
	model = ResNet50(weights="imagenet")
	global graph
	graph = tf.get_default_graph()


def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	return image


def predictions_gen(preds, top=5):
	"""
	:param preds: Numpy tensor encoding a batch of predictions.
	:param top: Integer, how many top-guesses to return.
	:return: A list of lists of top class prediction tuples
			`(class_name, class_description, score)`.
	"""
	results = imagenet_utils.decode_predictions(preds, top)
	predictions = []

	# loop over the results and add them to the list of
	# returned predictions
	for (imagenetID, label, prob) in results[0]:
		r = {"label": label, "probability": float(prob)}
		predictions.append(r)
	return predictions


@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# read the image in PIL format
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))

			# preprocess the image and prepare it for classification
			image = prepare_image(image, target=(224, 224))

			# classify the input image and then initialize the list
			# of predictions to return to the client
			with graph.as_default():
				preds = model.predict(image)
				data["predictions"] = predictions_gen(preds)

				# indicate that the request was a success
				data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	app.run(host='0.0.0.0')
