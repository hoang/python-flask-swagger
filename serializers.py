from flask_restplus import fields
from restplus import api

merge_docx_post = api.model('Merge docx post', {
    'contents': fields.List(
        fields.String()
    )
})

welcome_output = api.model('Welcome message output', {
    'message': fields.String(example="welcome to the jungle!"),
    'version': fields.Float(example="1.0")
})
