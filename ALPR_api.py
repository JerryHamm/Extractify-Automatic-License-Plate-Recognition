from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

#importing plate_detect function from the Automatic License Plate Recognition(ALPR)
from ALPR import plate_recognition

app = FastAPI()


@app.post("/ALPR")
async def license_plate_recognition(file: UploadFile):
    #save the uploaded image to a temporary file
    with open("temp_image.jpg", "wb") as buffer:
        buffer.write(await file.read())

    #running the ALPR
    ALPR_result = plate_recognition('temp_image.jpg')

    #return the JSON response
    return JSONResponse(ALPR_result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)