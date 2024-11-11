from flask import Flask,request,make_response,jsonify
import requests
import json
import re
import datetime
import pytz
import time
import certifi
import os
from PIL import Image, ImageDraw, ImageFont
import boto3

ca = certifi.where()

tz = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)

project_url = ""
api_password = ""

@app.route('/')
def index():
    return 'Flask API'

def return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}


def return_list(title,subtitle,options,descriptions,button_text,postback_text):
    options_list = []
    for option,description,postback in zip(options,descriptions,postback_text):
        options_list.append(
    {
                      "cells": [
                        {},
                        {
                          "text": option
                        },
                        {
                          "text": description
                        },
                        {
                            "text":postback
                        }
                        
                      ]
                    })
    return {"fulfillmentMessages": [
              {
                "platform": "ACTIONS_ON_GOOGLE",
                "simpleResponses": {
                  "simpleResponses": [
                    {
                      "textToSpeech": ""
                    }
                  ]
                }
              },
              {
                "platform": "ACTIONS_ON_GOOGLE",
                "tableCard": {
                  "title": title,
                  "subtitle": subtitle,
                  "columnProperties": [
                    {
                      "header": "Section Title",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Option Title",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Option Description",
                      "horizontalAlignment": "LEADING"
                    },
                    {
                      "header": "Postback text",
                      "horizontalAlignment": "LEADING"
                    }
                  ],
                  "rows": options_list,
                  "buttons": [
                    {
                      "title": button_text,
                      "openUriAction": {}
                    }
                  ]
                }
              },
              {
                "text": {
                  "text": [
                    ""
                  ]
                }
              }
            ]}

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


def return_text_and_suggestion_chip_with_context(text,suggestions,context_session,context_parameter_name,context_value):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}

def return_text_with_context(text,context_session,context_parameter_name,context_value):

    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": context_session+"/my_context",
        "lifespanCount": 25,
        "parameters": {
          context_parameter_name+".original":context_value,
          context_parameter_name:context_value
        }
      }
    ],}
    

def return_file_with_buttons(subtitle,text,url,suggestions):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "basicCard": {
          "subtitle": subtitle,
          "formattedText": text,
          "image": {
            "imageUri": url,
            "accessibilityText": "Please try again later"
          }
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      }
    ]}

def return_file_without_buttons(subtitle,text,url):
    
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "basicCard": {
          "subtitle": subtitle,
          "formattedText": text,
          "image": {
            "imageUri": url,
            "accessibilityText": "Please try again later"
          }
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
      }
    ]}



def return_text_and_suggestion_chip(text,suggestions):
    suggestion_list = []
    for suggestion in suggestions:
        suggestion_list.append({"title":suggestion})
    return {"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "suggestions": {
          "suggestions": suggestion_list
        }
      },
      {
        "text": {
          "text": [
            text
          ]
        }
      }
    ]}


def return_only_text(text):
    return {'fulfillmentMessages':[{"text":{"text":[text]}}]}

def return_text_and_media_in_two_message(message_text,media_url,media_type,media_text):
    return {"fulfillmentText": message_text,"fulfillmentMessages": [
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "simpleResponses": {
          "simpleResponses": [
            {
              "textToSpeech": message_text
            }
          ]
        }
      },
      {
        "platform": "ACTIONS_ON_GOOGLE",
        "basicCard": {
          "subtitle": media_type,
          "formattedText": media_text,
          "image": {
            "imageUri": media_url,
            "accessibilityText": media_type
          }
        }
      },
      {
        "text": {
          "text": [
            message_text
          ]
        }
      }
    ]}

def send_text_with_buttons(destination,text,buttons):
    button = []
    for but in buttons:
        button.append({"type":"reply","reply":{"id":but,"title":but}})
    
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": destination,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": text
            },
            "action": {
                "buttons": button
            }
        }
    }

    response = requests.post(project_url, headers=headers, json=data)


def send_image_with_text_project_api(destination,answer,media_url):
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": destination,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": answer
        }
    }
    
    payload = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": destination,
    "type": "image",
    "image":{ "link": media_url,
             "caption":answer}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password
    }

    response = requests.post(project_url, json=payload, headers=headers)
   
    
def send_image_with_text_and_buttons_project_api(destination,answer,media_url,buttons):
    
    button = []

    for but in buttons:
        button.append({"type":"reply","reply":{"id":but,"title":but}})
    
    payload = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": destination,
      "type": "interactive",
      "interactive": {
        "type": "button",
        "header": {
          "type": "image",
          "image": {
            "link": media_url
          }
        },
        "body": {
          "text": answer        },
        "action": {
          "buttons": button
        }
      }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password
    }

    response = requests.post(project_url, json=payload, headers=headers)

        
def send_text_project_api(destination,answer):
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": destination,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": answer
        }
    }
   
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password
    }

    response = requests.post(project_url, json=payload, headers=headers)

    
    
def send_video_with_text_and_buttons_project_api(whatsapp_mobile_number,text,media_url,buttons):
    
    button = []

    for but in buttons:
        button.append({"type":"reply","reply":{"id":but,"title":but}})

    payload = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": whatsapp_mobile_number,
      "type": "interactive",
      "interactive": {
        "type": "button",
        "header": {
          "type": "video",
          "video": {
            "link": media_url
          }
        },
        "body": {
          "text": text
        },
        "action": {
          "buttons": button
        }
      }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password
    }

    response = requests.post(project_url, json=payload, headers=headers)
    
def send_text_with_list(destination,header,body,footer,button_text,options):
    
    option = []
    for opt in options:
        option.append(
            {
              "id": opt,
              "title": opt,
              "description": ""
            }
        )

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password
    }

    data = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": destination,
      "type": "interactive",
      "interactive": {
        "type": "list",
        "header": {
          "type": "text",
          "text": header
        },
        "body": {
          "text": body
        },
        "footer": {
          "text": footer
        },
        "action": {
          "button": button_text,
          "sections": [
            {
              "title": "SECTION_1_TITLE",
              "rows": option
            }
          ]
        }
      }
    }

    response = requests.post(project_url, headers=headers, json=data)  

def send_pdf_with_text_and_buttons_project_api(whatsapp_mobile_number, text, media_url, buttons):
    
    button = []

    for but in buttons:
        button.append({"type":"reply","reply":{"id":but,"title":but}})

    payload = {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": whatsapp_mobile_number,
      "type": "interactive",
      "interactive": {
        "type": "button",
        "header": {
          "type": "document",  # Change from 'video' to 'document'
          "document": {
            "link": media_url  # URL to the PDF document
          }
        },
        "body": {
          "text": text
        },
        "action": {
          "buttons": button
        }
      }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-AiSensy-Project-API-Pwd": api_password  # Make sure the API password is set correctly
    }

    response = requests.post(project_url, json=payload, headers=headers)

def results():
    req = request.get_json(force=True)
    #print(req)
    
        
@app.route('/api/', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

if __name__ == '__main__':
    app.run()
    #app.run(host="0.0.0.0",port = 8000)
