from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from PIL import Image

from .train import model_construct
from .image_processing import process_image, process_batch_image

class DigitRecognitionAPI(ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        form_data = request.data.dict()
        data = form_data.get('image', None)
        if data is None:
            return Response("image is required")
        image = Image.open(data)
        x = process_image(image)
        if x is None:
            return Response("invalid image")

        model = model_construct()
        prediction = model.predict(x)[0]
        classes = ['1', '10', '100', '1000', '2', '20', '3', '30', '4', '40', '5', '50', '6', '60', '7', '70', '8', '80', '9', '90']
        result = [(prediction[i], classes[i]) for i in range(20)]
        result.sort(reverse=1)
        return Response(
            result
        )

    @action(
        methods=["post"],
        detail=False,
    )
    def batch(self, request):
        data = request.POST.getlist("image", [])
        if data is []:
            return Response("image is required")
        images = []
        for im in data:
            image = Image.open(im)
            images.append(image)
        x = process_batch_image(images)
        model = model_construct()
        predictions = model.predict(x)
        classes = ['1', '10', '100', '1000', '2', '20', '3', '30', '4', '40', '5', '50', '6', '60', '7', '70', '8', '80', '9', '90']
        response = {}
        for idx, prediction in enumerate(predictions):
            result = [(prediction[i], classes[i]) for i in range(20)]
            result.sort(reverse=1)
            response[data[idx]] = result[0][1]
        return Response(
            response
        )