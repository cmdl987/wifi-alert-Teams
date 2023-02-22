# Wifi-Alert-Teams
![wifi-alert-logo](https://user-images.githubusercontent.com/59370680/220681919-df76e8ba-b0f8-4bcd-86c3-ae2217b58bd7.png)


Wifi-Alert-Teams take a quick snapshot of the wifi networks around you, and warns you when a specific wifi network is 
active at a specific time, sending a personalized message to a Microsoft Teams group channel.


----

## Getting started

To obtain the full code you can clone the git repository:
```
git clone https://github.com/cmdl987/Wifi-Alerter-Teams
```

## Get Incoming Webhook

An incoming webhook lets external applications to share content in Microsoft Teams channels. The webhooks are used as 
tools to track and notify. The webhook provide a unique URL, to send a JSON payload with a message in card format. 
These cards are user interface containers that include content and actions.

To add an Incoming Webhook to a Teams channel, follow these steps:
1) Open the Microsoft Teams application and click on the 'Apps'. Enter "webhook" on the text area and select the 
Incoming Webhook app.

![teams_1](https://user-images.githubusercontent.com/59370680/220617418-7b59ad70-31cf-45e1-8f89-4f5fa9d2790b.png)

2) Click on 'Add to team' button in order to select the Teams channel in which you want to add the webhook and 'Set up a connector'.

![teams_2](https://user-images.githubusercontent.com/59370680/220617423-29f286f4-071d-43f3-82f1-d6d56f46e0db.png)
![teams_3](https://user-images.githubusercontent.com/59370680/220617425-e963026a-33c0-4c75-b49c-99d8f7c73aeb.png)

3) Provide a name and upload an image for your webhook if necessary. Then push 'Create' button. 

![teams_4](https://user-images.githubusercontent.com/59370680/220617428-45ea0454-f0c6-4aaa-8867-c88d611260a3.png)

4) Copy and save the unique webhook URL present in the dialog. This URL maps to the channel you selected previously and
need to be copied when asked. It will send an HTTP post request with a personal content that will vary attending on the 
SSID and the content we are selected.

![teams_5](https://user-images.githubusercontent.com/59370680/220617430-2474f128-6dc0-4a89-b3f9-1b14b9670f13.png)


---
## Files generated

### Config.csv & logs.csv
After running the code for the very first time, it will create two .csv files, both located at root:
- **config.csv**: it defines the user parameters in the correct format to run the scheduler launcher. Parameters:
    
  - ts : timestamp with the last saved configuration.
  - SSID_list : target SSID to detect.
  - alarm_time : time when the detector script will be launched.
  - webhook : webhook URL copied by the user.


- **logs.csv**: it saves the information every time the detector is triggered by the scheduler. Parameters:
  - config_time : datetime whit the latest configuration.
  - date : date of the log
  - time_alarm : time when the detector script was programed to be launched.
  - SSIDs_target : SSIDs to be detected.
  - SSIDs_detected : SSIDs that were detected.
  - webhook : webhook URL where the content was sent.
  - delivery_status : *bool*, checks if the message was correctly delivered. 

### JSON files
Both .json files could be edited in order to personalize the content message it would be sent via post request.

While 'content.json' contains the default message, 'personalized_content.json' file could be modified, 
adding title, an image from a URL, and a location for every SSID you want to personalize.

The message displayed would be similar to this one:

![teams_6](https://user-images.githubusercontent.com/59370680/220617435-d35ce7c4-a1e3-4b2f-b445-7b395dff77dd.png)