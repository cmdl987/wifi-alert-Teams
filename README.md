# Wifi-Alert-Teams

Wifi-Alert-Teams take a quick snapshot of the wifi networks around you, and warns you when a specific wifi network is active at a specific time, sending a personalized message to a Microsoft Teams group. 


## Getting started

To obtain the full code you can clone the git repository:
```
git clone https://github.com/cmdl987/Wifi-Alerter-Teams
```

## Get Teams Webhook
Prior to sending a message to the Microsoft Teams channel, it is necessary to get a webhook URL.
This link will allow you to send an HTTP post request with a personal content that will vary attending on the SSID and the content we are selected.
First at all, you need to add the Incoming Webhook app in your Microsoft Teams application.

Once it is installed, you will need to decide in which chanel you want to post notification. Over the group channel, click on "More options" button and select "Connectors". It will find all the connectors available. Click on "Configure" over the Incoming Webhook app.

The configuration box will opens and you will need to enter a webhook name. Also, you can add a profile picture from your computer.

After click on the "Create" button, the URL with the webhook connector will appear, being able to copy it.


### Files generated

After running the code for the very first time, it will create two .csv files, both located at root:
- config.csv: it defines the user parameters in the correct format to run the scheduler launcher.
- logs.csv: it saves the information every time the detector is triggered by the scheduler.

### Config files
Both .json files could be edited in order to personalize the content message it would be sent via post request.
While "content.json" contains the default message, "personalized_content.json" file could be modified, adding comments and images from url, always respecting the name/value pairs structure. 