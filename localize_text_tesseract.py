# Uso HEIMDALL-EYE RECONOCIMIENTO DE LETRAS , MATRICULAS 
# python localize_text_tesseract.py --image apple_support.png


# Importamos los Modulos necesarios 
from pytesseract import Output
import pytesseract
import argparse
import cv2

# Contruimos el analizador de Argumentos y Analizamos esos Argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf", type=int, default=0,
	help="mininum confidence value to filter weak text detection")
args = vars(ap.parse_args())

# Cargamos la imagen de entrada y la convertimos de RGB A BGR 
# Usamos Tesseract para localizar cada area de texto en la entrada de la imagen
image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

# Recorremos cada una de las localizaciones individuales dentro de la imagen
for i in range(0, len(results["text"])):
	# Extraemos la coordenadas del cuadro delimitador de la region de texto 
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]

	# Extraemos el texto de OCR junto con la confianza de la localizacion del texto
	text = results["text"][i]
	conf = int(results["conf"][i])

	# Filtramos localizaciones de texto de confianza debil
	if conf > args["min_conf"]:
		# Mostramos el texto en la terminal
		print("Confianza: {}".format(conf))
		print("Texto: {}".format(text))
		print("")

		# Eliminamos el texto que no sea ASCII para que podamos dibujar el texto en la imagen
		# Usando OpenCV dibujamos el texto en el Frame con el texto itsel
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			1.2, (0, 0, 255), 3)

#Mostramos el Frame en Pantalla
cv2.imshow("Image", image)
cv2.waitKey(0)