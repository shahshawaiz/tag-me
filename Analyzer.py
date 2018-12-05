# imports
import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
from PIL import Image
from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util

# constants for model name and remote path for downloadg 
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# init detection graph script
detection_graph = tf.Graph()

# get detault graph
with detection_graph.as_default():

  # get ref to graph def
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid: # read frozen graph in rb mode 

    # serialized frozen graph 
    serialized_graph = fid.read()

    # parse graph def
    od_graph_def.ParseFromString(serialized_graph) # copy frozen graph meta to prior initliazed tf def
    tf.import_graph_def(od_graph_def, name='') # import graph to tf session

# init url opener
opener = urllib.request.URLopener()

# download base file
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)

# get tar handle
tar_file = tarfile.open(MODEL_FILE)

# iterate tar items
for file in tar_file.getmembers():

  # get filename
  file_name = os.path.basename(file.name)

  # if frozen_inference_graph then extract 
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())

# load image to np
def load_image_into_numpy_array(image):

  # get image dim 
  (im_width, im_height) = image.size

  # init np with same dim and copy
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# analyze image
def run_inference_for_single_image(image, graph):

  # get default graph
  with graph.as_default():

    # get session
    with tf.Session() as sess:

      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'

        # set tensor dict, if tensor name exists
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)

      #  if tensor is detection mask ?
      if 'detection_masks' in tensor_dict:

        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])

        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)

        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)

      # get image tensor ?
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]

  return output_dict

def demo(image_np):

  # List of the strings that is used to add correct label for each box.
  PATH_TO_LABELS = os.path.join('object_detection', 'data', 'mscoco_label_map.pbtxt')

  # get category labels
  category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

  # run recognition
  output_dict = run_inference_for_single_image(image_np, detection_graph)

  # print labels
  labels = vis_util.get_labels(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)

  print(labels)

# get image
PATH_TO_TEST_IMAGES_DIR = 'test_images'
image_path = os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image1.jpg')
image = Image.open(image_path)
image_np = load_image_into_numpy_array(image)

demo(image_np)
