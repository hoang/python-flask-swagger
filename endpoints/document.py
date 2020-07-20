from flask import send_file, request
from restplus import api
from flask_restplus import Resource
from serializers import merge_docx_post
import logging
from docxcompose.composer import Composer
from docx import Document
import base64
import fitz
from util import generate_temp_folder

log = logging.getLogger(__name__)
ns = api.namespace('document', description='Operations related to document')


@ns.route('/sign-pdf')
class PdfUtilCollection(Resource):

    def get(self):
        input_file = "tempFiles/pdfFinal.pdf"
        signature_file = "tempFiles/signature.jpg"

        temp_folder = generate_temp_folder()
        output_file = temp_folder + "/signed.pdf"

        image_rect = fitz.Rect(150, 150, 300, 300)
        file_handler = fitz.open(input_file)
        first_page = file_handler[0]
        first_page.insertImage(image_rect, filename=signature_file)
        file_handler.save(output_file)

        return None, 201


@ns.route('/merge-docx')
class MergeDocxCollection(Resource):

    @api.expect(merge_docx_post)
    @api.response(200, 'Success')
    @api.produces([
        """application/vnd.openxmlformats-officedocument
        .wordprocessingml.document"""
    ])
    @api.response(400, 'Bad Request')
    def post(self):
        """
        Merge multiple docx documents into one
        """
        log.info("received a request to merge docx")
        contents = request.json['contents']
        if len(contents) < 2:
            return {"message": "contents must be at least 2 elements"}, 400

        tempFolder = generate_temp_folder()
        ext = '.docx'

        for i, content in enumerate(contents):
            base64_decode = base64.b64decode(content)
            fp = open(tempFolder + "/file" + str(i) + ext, "wb")
            fp.write(base64_decode)
            fp.close()

        for i in range(len(contents)):
            doc = Document(tempFolder + '/file' + str(i) + ext)
            if i == 0:
                composer = Composer(doc)
            else:
                composer.append(doc)

        output_file = tempFolder + '/final' + ext
        composer.save(output_file)
        return send_file(output_file, as_attachment=True)
