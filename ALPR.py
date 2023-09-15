# Importing libraries and required functionalities.
import cv2
import re
from darknet import darknet

# Importing pillow function for image preprocessing.
from PIL import Image, ImageEnhance, ImageFilter

# Darknet object detector imports.
from darknet.darknet_images import load_images
from darknet.darknet_images import image_detection

#Importing OCR and initializing based on our requirements.
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='en', rec_algorithm='CRNN')

# Add absolute paths to important variables.
# Declaring important variables.
# Path of Configuration file of YOLOv4-tiny.
config_file = './darknet/cfg/yolov4-tiny-obj.cfg'
# Path of obj.data file.
data_file = './darknet/obj.data'
# Batch size of data passed to the detector.
batch_size = 1
# Path to trained YOLOv4 weights.
weights = './darknet/weights/yolov4-tiny-obj_best.weights'
# Confidence threshold.
threshold = 0.6

# Loading darknet network and classes along with the bbox.
network, class_names = darknet.load_network(
        config_file,
        data_file,
        weights,
        batch_size= batch_size
    )


#resize_bbox() for resizing the predicted bounding box coordinates back to bounding box coordinates according to the original image size.
def resize_bbox(detections, out_size, in_size):
    coord = []
    scores = []

    # Scaling the bounding boxes to the different size
    for det in detections:
        points = list(det[2])
        conf = det[1]
        xmin, ymin, xmax, ymax = darknet.bbox2points(points)
        y_scale = float(out_size[0]) / in_size[0]
        x_scale = float(out_size[1]) / in_size[1]
        ymin = int(y_scale * ymin)
        ymax = int(y_scale * ymax)
        xmin = int(x_scale * xmin) if int(x_scale * xmin) > 0 else 0
        xmax = int(x_scale * xmax)
        final_points = [xmin, ymin, xmax-xmin, ymax-ymin]
        scores.append(conf)
        coord.append(final_points)
        
    return coord, scores


#yolo_det() responsible for detecting the bounding boxes of the license plates from the input vehicle images.
def yolo_det(frame, config_file, data_file, batch_size, weights, threshold, network, class_names):
   
    # Preprocessing the input image.
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height))

    # Passing the image to the detector and store the detections
    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=threshold)
    darknet.free_image(darknet_image)

    # Resizing predicted bounding box from 416x416 to input image resolution
    out_size = frame.shape[:2]
    in_size = image_resized.shape[:2]
    coord, scores = resize_bbox(detections, out_size, in_size)

    return coord, scores


#crop() responsible for cropping out license plate using the bounding box coordinates image for OCR.
def crop(image, coordinates):
    top_left_x, top_left_y, width, height = coordinates

    #Caluculate top-left and bootom-right coordinates
    bottom_right_x = int(top_left_x + width)
    bottom_right_y = int(top_left_y + height)
    
    #Perform Cropping
    cr_img = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
    
    return cr_img


#heavy preprocessing of images
def heavy_prepocessing(cr_img, bbox, heavier=False):
    #Preprocessing Cropped Image
    cr_img_proc = Image.fromarray(cr_img)
    
    #depending on the situation the preprocessing strength maybe increased to aid heavy preprocessing 
    #(done by setting heavier to True)
    if heavier == False:
        #increase resolution
        cr_img_proc = cr_img_proc.resize((bbox[2]*2, bbox[3]*2), Image.BICUBIC)
        #decrease noise
        cr_img_proc = cr_img_proc.filter(ImageFilter.UnsharpMask(6))
        #increase contrast
        enhancer_contrast = ImageEnhance.Contrast(cr_img_proc)
        cr_img_proc = enhancer_contrast.enhance(3.5)
        #increase sharpness
        cr_img_proc = cr_img_proc.filter(ImageFilter.UnsharpMask(6, 16, 3))
    else:
        #increase resolution
        cr_img_proc = cr_img_proc.resize((bbox[2]*3, bbox[3]*3), Image.BICUBIC)
        #decrease noise
        cr_img_proc = cr_img_proc.filter(ImageFilter.UnsharpMask(8))
        #increase contrast
        enhancer_contrast = ImageEnhance.Contrast(cr_img_proc)
        cr_img_proc = enhancer_contrast.enhance(4.5)
        #increase sharpness
        cr_img_proc = cr_img_proc.filter(ImageFilter.UnsharpMask(6, 20, 3))

    #saving ocr output
    ocr_raw_output = ocr.ocr(cr_img, cls=False, det=True, rec=True)
        
    #Retrieving only plate number and the confidence score
    ocr_output = list(ocr_raw_output[0][0][1])
    
    #removing dots, dashes and spaces from plate number
    ocr_output[0] = filter_plate(ocr_output[0])
    
    return ocr_output


#light preprocessing of images
def light_prepocessing(cr_img, bbox):
    #Preprocessing Cropped Image
    cr_img_proc = Image.fromarray(cr_img)
    #decrease noise
    cr_img_proc = cr_img_proc.filter(ImageFilter.UnsharpMask(5))
    #increase contrast
    enhancer_contrast = ImageEnhance.Contrast(cr_img_proc)
    cr_img_proc = enhancer_contrast.enhance(2)
    #increase sharpness
    cr_img_proc = cr_img_proc.filter(ImageFilter.UnsharpMask(2, 6, 3))

    #saving ocr output
    ocr_raw_output = ocr.ocr(cr_img, cls=False, det=True, rec=True)
        
    #Retrieving only plate number and the confidence score
    ocr_output = list(ocr_raw_output[0][0][1])
    
    #removing dots, dashes and spaces from plate number
    ocr_output[0] = filter_plate(ocr_output[0])
    
    return ocr_output


#function removing dots, dashes and spaces from plate number
def filter_plate(plate_num):
    #var to hold filtered plate number
    plate_num_filtered = ""
    #removeing dots, dashes and spaces from plate number
    for char in plate_num:
        if char.isupper() or char.isdigit():
            plate_num_filtered += char 
    
    return plate_num_filtered


#checking plate formats(LLLNNNN OR LLLNLNN OR LLLNNLN) standard in brazil
def check_plate_format(plate_num):
    # Define the formats to match against
    format1 = r'[A-Z]{3}[0-9]{4}'
    format2 = r'[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}'
    format3 = r'[A-Z]{3}[0-9]{2}[A-Z]{1}[0-9]{1}'

    # Check if the plate number matches either format
    if re.match(format1, plate_num) or re.match(format2, plate_num) or re.match(format3, plate_num):
        return True
    else:
        return False


#modifying the plate number based on plate formats to catch common errors
def plate_format_filters(plate_num):
    modified_plate_num = ""

    for i in range(len(plate_num)):#note that the length for plate_num should be seven
        #addressing common errors in the first 3 characters of the license plate
        if i < 3:
            if plate_num[i] == '0':
                modified_plate_num += 'O'
            elif plate_num[i] == '1':
                modified_plate_num += 'I'
            elif plate_num[i] == '3':
                modified_plate_num += 'B'
            elif plate_num[i] == '6':
                modified_plate_num += 'G'
            elif plate_num[i] == '8':
                modified_plate_num += 'B'
            else:
                modified_plate_num += plate_num[i]
        #leaving the character at index 4 of the license plate unmodified due to plate format
        elif i == 4:
            modified_plate_num += plate_num[i]
        #leaving the character at index 5 of the license plate unmodified due to plate format
        elif i == 5:
            modified_plate_num += plate_num[i]
        #addressing the remaining characters of the license plate
        else:
            if plate_num[i] == 'O':
                modified_plate_num += '0'
            elif plate_num[i] == 'I':
                modified_plate_num += '1'
            elif plate_num[i] == 'l':
                modified_plate_num += '1'
            elif plate_num[i] == 'G':
                modified_plate_num += '6'
            elif plate_num[i] == 'g':
                modified_plate_num += '9'
            else:
                modified_plate_num += plate_num[i]

    return modified_plate_num

    
#plate_recognition() performs ALPR on images. Responsible for performing detection, and recognition
def plate_recognition(input): 
    try:
        # Reading the image and performing YOLOv4 detection. 
        img = cv2.imread(input)
        bboxes, scores = yolo_det(img, config_file, data_file, batch_size, 
                                  weights, threshold, network, class_names)

        # Extracting bounding box coordinate.
        bbox = []
        for coord in bboxes:
            bbox = [coord[0], coord[1], coord[2], coord[3]]
    except:
        return []
    
    try:
        #Cropping main license plate image
        cr_img = crop(img, bbox)

        #Performing OCR on cropped image
        ocr_raw_output = ocr.ocr(cr_img, cls=False, det=True, rec=True)
        
        #Retrieving only plate number and the confidence score
        ocr_output = list(ocr_raw_output[0][0][1])
    except:
        ocr_output = []

    #Logic to preprocess image based on braziliam license plate formats(LLL-NNNN OR LLL-NLNN) and confidence score
    #Checking if ocr returned anything
    if len(ocr_output) != 0:
        
        #checking if the ocr output contains a plate number string
        if type(ocr_output[0]) == str:
            
            #removing dots, dashes and spaces from plate number
            ocr_output[0] = filter_plate(ocr_output[0])
            
            #checking if the plate number has a length of 7 (length of a brazilian license plate)
            if len(ocr_output[0]) == 7:
                
                if round(100 * (ocr_output[1])) >= 80 and len([char for char in ocr_output[0] if char.isupper()]):
                    
                    #light preprocessing if ocr confidence score >= 80 and the plate number has 3 or 4 letters
                    ocr_output = light_prepocessing(cr_img, bbox)
                    
                else:                    
                    #heavy preprocessing if ocr confidence score < 80
                    ocr_output = heavy_prepocessing(cr_img, bbox)
                    
                #checking plate formats formats(LLL-NNNN OR LLL-NLNN) standard in brazil
                if check_plate_format(ocr_output[0]) == True:
                    
                    #check if the confidence score is >=80
                    if round(100 * (ocr_output[1])) >= 80:
                        pass
                    
                    else:
                        #ocr failed test...plate number rejected
                        ocr_output = []
                
                else:
                    
                    #appling plate filters based on plate formats to catch common errors
                    ocr_output[0] = plate_format_filters(ocr_output[0])
                    
                    #checking plate formats formats(LLL-NNNN OR LLL-NLNN) standard in brazil
                    if check_plate_format(ocr_output[0]) == True:

                        #check if the confidence score is >=80
                        if round(100 * (ocr_output[1])) >= 80:
                            pass

                        else:
                            #ocr failed test...plate number rejected
                            ocr_output = []

                    else:
                        #heavy preprocessing to increase chances of format check pass
                        ocr_output = heavy_prepocessing(cr_img, bbox, heavier=True)
                        
                        #appling plate filters based on plate formats to catch common errors
                        ocr_output[0] = plate_format_filters(ocr_output[0])
                        
                        #checking plate formats formats(LLL-NNNN OR LLL-NLNN) standard in brazil
                        if check_plate_format(ocr_output[0]) == True:

                            #check if the confidence score is >=80
                            if round(100 * (ocr_output[1])) >= 80:
                                pass

                            else:
                                #ocr failed test...plate number rejected
                                ocr_output = []

                        else:
                            #ocr failed test...plate number rejected
                            ocr_output = []
            
            else:
                #heavy preprocessing to increase chances of format check pass
                ocr_output = heavy_prepocessing(cr_img, bbox, heavier=True)
                
                #checking if the plate number has a length of 7 (length of a brazilian license plate)
                #also checking is the plate number has 3 or 4 letters only
                if len(ocr_output[0]) == 7 and len([char for char in ocr_output[0] if char.isupper()]):
                    
                    #checking plate formats formats(LLL-NNNN OR LLL-NLNN) standard in brazil
                    if check_plate_format(ocr_output[0]) == True:

                        #check if the confidence score is >=80
                        if round(100 * (ocr_output[1])) >= 80:
                            pass

                        else:
                            #ocr failed test...plate number rejected
                            ocr_output = []

                    else:
                        #ocr failed test...plate number rejected
                        ocr_output = []
                
                else:
                    #ocr failed test...plate number rejected
                    ocr_output = []
        
        else:
            pass
        
    else:
        pass
    
    #gathering lincense plate detector info into a list: [plate_number, confidence, top_left_coords, bottom_right_coords]
    try:
        #changing confidence output (example: from 0.95 to 95)
        ocr_output[1] = round(100 * (ocr_output[1]))
    except:
        ocr_output = []

    try:           
        #Calculating top left and bottom right coordinates
        top_left_x, top_left_y, width, height = bbox
        bottom_right_x = int(top_left_x + width)
        bottom_right_y = int(top_left_y + height)

        #Adding the coordinates to the result
        ocr_output.append([top_left_x, top_left_y])
        ocr_output.append([bottom_right_x, bottom_right_y])
    except:
        ocr_output = []

    return ocr_output
