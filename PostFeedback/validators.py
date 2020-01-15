import logging
import jsonschema


from SharedCode.exceptions import ValidationError

FEEDBACK_JSONSCHEMA = {
    "type": "object",
    "properties": {
        "page": {"type": "string", "maxLength": 2047},
        "is_useful": {"type": "boolean"},
        "questions": {
            "type": "array",
            "items": {
                "question": {"type": "object"},
                "properties": {
                    "title": {"type": "string", "maxLength": 200},
                    "feedback": {"type": "string", "maxLength": 4000},
                },
                "additionalProperties": False,
            },
        },
    },
    "required": ["page", "is_useful"],
    "additionalProperties": False,
}


def validate_feedback(feedback_data):
    try:
        jsonschema.validate(feedback_data, FEEDBACK_JSONSCHEMA)
    except jsonschema.ValidationError as e:
        logging.error(f"Validation error {e.message}")
        raise ValidationError(e.message)
    except jsonschema.SchemaError as e:
        logging.error(f"Schema error {e.message}")
        raise ValidationError(e.message)
