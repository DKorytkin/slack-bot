

class Modal:
    """
    {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "My App",
            "emoji": true
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": true
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": true
        },
        "blocks: []
    }
    """


class Input:
    """
    {
        "type": "input",
        "element": {
            "type": "plain_text_input"
        },
        "label": {
            "type": "plain_text",
            "text": "Label",
            "emoji": true
        }
    }
    """


class Multiline:
    """
    {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "multiline": true
        },
        "label": {
            "type": "plain_text",
            "text": "Label",
            "emoji": true
        }
    }
    """


class DatePicker:
    """
    {
        "type": "input",
        "element": {
            "type": "datepicker",
            "initial_date": "1990-04-28",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a date",
                "emoji": true
            }
        },
        "label": {
            "type": "plain_text",
            "text": "Label",
            "emoji": true
        }
    }
    """


class Select:
    """
    {
        "type": "input",
        "element": {
            "type": "conversations_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a conversation",
                "emoji": true
            }
        },
        "label": {
            "type": "plain_text",
            "text": "Label",
            "emoji": true
        }
    }
    """


class MultiSelect:
    """
    {
        "type": "input",
        "element": {
            "type": "multi_users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select users",
                "emoji": true
            }
        },
        "label": {
            "type": "plain_text",
            "text": "Label",
            "emoji": true
        }
    }
    """


class RadioButton:
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "This is a section block with radio button accessory"
        },
        "accessory": {
            "type": "radio_buttons",
            "initial_option": {
                "text": {
                    "type": "plain_text",
                    "text": "Option 1"
                },
                "value": "option 1",
                "description": {
                    "type": "plain_text",
                    "text": "Description for option 1"
                }
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 1"
                    },
                    "value": "option 1",
                    "description": {
                        "type": "plain_text",
                        "text": "Description for option 1"
                    }
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 2"
                    },
                    "value": "option 2",
                    "description": {
                        "type": "plain_text",
                        "text": "Description for option 2"
                    }
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 3"
                    },
                    "value": "option 3",
                    "description": {
                        "type": "plain_text",
                        "text": "Description for option 3"
                    }
                }
            ]
        }
    }
    """