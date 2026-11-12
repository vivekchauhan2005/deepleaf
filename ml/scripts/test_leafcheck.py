import sys
import os
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

MODEL_PATH = r"C:\project\deepleaf\ml\models\leaf_checker.keras"

IMG_SIZE = (224, 224)


def main():

    if len(sys.argv) != 2:
        print()
        print("Usage:")
        print(r'python ml\scripts\test_leafcheck.py "FULL_IMAGE_PATH"')
        print()
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.isfile(image_path):
        print()
        print("ERROR: Image file not found:")
        print(image_path)
        print()
        sys.exit(1)

    print()
    print("Loading Leaf Checker model...")

    # IMPORTANT:
    # preprocess_input is used in the Lambda layer
    # while loading the saved Keras model.
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={
            "preprocess_input": preprocess_input
        },
        compile=False
    )

    print("Model loaded successfully!")

    # Load image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    image_array = tf.keras.utils.img_to_array(image)

    image_array = tf.expand_dims(
        image_array,
        axis=0
    )

    # VGG19 preprocessing
    image_array = preprocess_input(image_array)

    prediction = model.predict(
        image_array,
        verbose=0
    )[0][0]

    # IMPORTANT:
    # image_dataset_from_directory sorted:
    # leaf = 0
    # non_leaf = 1

    if prediction >= 0.5:

        label = "NON-LEAF"

        confidence = float(prediction) * 100

    else:

        label = "LEAF"

        confidence = (1.0 - float(prediction)) * 100

    print()
    print("=" * 60)
    print("             DEEPLEAF LEAF CHECK")
    print("=" * 60)

    print(f"Image      : {os.path.basename(image_path)}")
    print(f"Result     : {label}")
    print(f"Confidence : {confidence:.2f}%")

    print("=" * 60)

    if label == "NON-LEAF":

        print()
        print("Please enter a plant leaf image.")
        print("Disease analysis will NOT be performed.")

    else:

        print()
        print("Leaf image confirmed.")
        print("Ready for disease analysis.")


if __name__ == "__main__":
    main()