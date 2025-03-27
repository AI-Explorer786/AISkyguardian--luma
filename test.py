# import cv2

# image_path = "C:/Users/b2732/OneDrive/Documents/GitHub/AISkyguardian--luma/image.jpg"
# img = cv2.imread(image_path)

# if img is None:
#     print("Error: Image not found at", image_path)
# else:
#     print("Image loaded successfully!")
import cv2

image_path = "C:\\Users\\b2732\\OneDrive\\Documents\\GitHub\\AISkyguardian--luma\\image.jpg"
img = cv2.imread(image_path)

if img is None:
    print("❌ Error: Image not found or unable to load")
else:
    print("✅ Image loaded successfully!")
    cv2.imshow("Test Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

