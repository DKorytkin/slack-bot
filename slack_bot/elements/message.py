from slack_bot.elements.base import Base


class Context(Base):
    """
    {
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/mediumpriority.png",
                "alt_text": "palm tree"
            },
            {
                "type": "mrkdwn",
                "text": "*Medium Priority*"
            }
        ]
    }

    {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "*Author:* T. M. Schwartz"
            }
        ]
    }
    """


class Actions(Base):
    """
    {
        "type": "actions",
        "elements": [
            {
                "type": "conversations_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a conversation",
                    "emoji": true
                }
            },
            {
                "type": "channels_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a channel",
                    "emoji": true
                }
            },
            {
                "type": "users_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a user",
                    "emoji": true
                }
            },
            {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": true
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Excellent item 1",
                            "emoji": true
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Fantastic item 2",
                            "emoji": true
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Nifty item 3",
                            "emoji": true
                        },
                        "value": "value-2"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Pretty good item 4",
                            "emoji": true
                        },
                        "value": "value-3"
                    }
                ]
            }
        ]
    }
    """


class ActionDatePicker(Base):
    """
    {
        "type": "actions",
        "elements": [
            {
                "type": "datepicker",
                "initial_date": "1990-04-28",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": true
                }
            },
            {
                "type": "datepicker",
                "initial_date": "1990-04-28",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": true
                }
            }
        ]
    }
    """


class Divider(Base):
    """
    {
        "type": "divider"
    }
    """

    type = "divider"

    def to_dict(self):
        return {"type": self.type}


class Section(Base):
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*<fakelink.com|WEB-1098 Adjust borders on homepage graphic>*"
        },
        "accessory": {
            "type": "overflow",
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": ":white_check_mark: Mark as done",
                        "emoji": true
                    },
                    "value": "done"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": ":pencil: Edit",
                        "emoji": true
                    },
                    "value": "edit"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": ":x: Delete",
                        "emoji": true
                    },
                    "value": "delete"
                }
            ]
        }
    }
    """


class SectionText(Base):
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hey there 👋 I'm TaskBot."
        }
    }
    """

    type = "section"

    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {"type": self.type, "text": MarkdownText(self.text).to_dict()}


class SectionOverflow(Base):
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "This block has an overflow menu."
        },
        "accessory": {
            "type": "overflow",
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 1",
                        "emoji": true
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 2",
                        "emoji": true
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 3",
                        "emoji": true
                    },
                    "value": "value-2"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Option 4",
                        "emoji": true
                    },
                    "value": "value-3"
                }
            ]
        }
    }
    """


class MultiSelect(Base):
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Pick one or more items from the list"
        },
        "accessory": {
            "type": "multi_static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select items",
                "emoji": true
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Choice 1",
                        "emoji": true
                    },
                    "value": "value-0"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Choice 2",
                        "emoji": true
                    },
                    "value": "value-1"
                },
                {
                    "text": {
                        "type": "plain_text",
                        "text": "Choice 3",
                        "emoji": true
                    },
                    "value": "value-2"
                }
            ]
        }
    }
    """


class SectionWithImage(Base):
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You can add an image next to text in this block."
        },
        "accessory": {
            "type": "image",
            "image_url": "https://api.slack.com/img/blocks/bkb_template_images/plants.png",
            "alt_text": "plants"
        }
    }
    """

    type = "section"

    def __init__(self, text, image_url, alt_text="Image"):
        self.text = text
        self.image_url = image_url
        self.alt_text = alt_text

    def to_dict(self):
        return {
            "type": self.type,
            "text": MarkdownText(self.text).to_dict(),
            "accessory": Image(image_url=self.image_url, alt_text=self.alt_text).to_dict(),
        }


class MarkdownText(Base):
    """
    {
        "type": "mrkdwn",
        "text": "Awaiting Release"
    }
    """

    type = "mrkdwn"

    def __init__(self, text):
        self.text = text

    def to_dict(self):
        return {"type": self.type, "text": self.text}


class PlainText(MarkdownText):
    """
    "text": {
        "type": "plain_text",
        "text": ":white_check_mark: Mark as done",
        "emoji": true
    }
    """

    type = "plain_text"

    def to_dict(self):
        return {"type": self.type, "text": self.text, "emoji": True}


class Image(Base):
    """
    {
        "type": "image",
        "title": {
            "type": "plain_text",
            "text": "Example Image",
            "emoji": true
        },
        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/goldengate.png",
        "alt_text": "Example Image"
    }
    """

    type = "image"

    def __init__(self, image_url, title=None, alt_text="Image"):
        self.title = title
        self.image_url = image_url
        self.alt_text = alt_text

    def to_dict(self):
        data = {
            "type": self.type,
            "image_url": self.image_url,
            "alt_text": self.alt_text
        }
        if self.title:
            data["title"] = MarkdownText(self.title).to_dict()
        return data


class Button(Base):
    """
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "You can add a button alongside text in your message. "
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Button",
                "emoji": true
            },
            "value": "click_me_123"
        }
    }
    """

    type = "section"

    def __init__(self, text, button_name, button_value):
        self.text = text
        self.button_name = button_name
        self.button_value = button_value

    def to_dict(self):
        button = {
            "type": "button",
            "text": PlainText(self.button_name),
            "value": self.button_value
        }
        return {"type": self.type, "text": MarkdownText(self.text), "accessory": button}


class RadioButton(Base):
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


class Field(Base):
    """
    {
        "type": "section",
        "fields": [
            {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": true
            },
            {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": true
            },
            {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": true
            },
            {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": true
            },
            {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": true
            }
        ]
    }
    """

    type = "section"

    def __init__(self, *fields):
        self.fields = fields

    def to_dict(self):
        return {"type": self.type, "fields": [MarkdownText(field).to_dict() for field in self.fields]}
