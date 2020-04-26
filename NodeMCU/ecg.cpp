#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <WebSocketsServer.h>
#include <Hash.h>
#include <string.h>

const char *ssid = "dlink";
const char *password = "apple!Happy";
int EcgPin = A0;

//String WebPage = "<!DOCTYPE html><html><style>input[type=\"text\"]{width: 90%; height: 3vh;}input[type=\"button\"]{width: 9%; height: 3.6vh;}.rxd{height: 90vh;}textarea{width: 99%; height: 100%; resize: none;}</style><script>var Socket;function start(){Socket=new WebSocket('ws://' + window.location.hostname + ':81/'); Socket.onmessage=function(evt){document.getElementById(\"rxConsole\").value +=evt.data;}}function enterpressed(){Socket.send(document.getElementById(\"txbuff\").value); document.getElementById(\"txbuff\").value=\"\";}</script><body onload=\"javascript:start();\"> <div><input class=\"txd\" type=\"text\" id=\"txbuff\" onkeydown=\"if(event.keyCode==13) enterpressed();\"><input class=\"txd\" type=\"button\" onclick=\"enterpressed();\" value=\"Send\" > </div><br><div class=\"rxd\"> <textarea id=\"rxConsole\" readonly></textarea> </div></body></html>";
String WebPage = "<!DOCTYPE html><html><script>var Socket;function start(){Socket=new WebSocket('ws://' + window.location.hostname + ':81/'); </script><body onload=\"javascript:start();\"></body></html>";
String ecgResponse = "{ \"ecg\": %f}";

WebSocketsServer webSocket = WebSocketsServer(81);
ESP8266WebServer server(80);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length)
{
   if (type == WStype_TEXT)
   {
      for (int i = 0; i < length; i++)
         Serial.print((char)payload[i]);
      Serial.println();
   }
}

void setup()
{
   pinMode(EcgPin, INPUT);
   Serial.begin(9600);
   WiFi.begin(ssid, password);
   Serial.println("");

   while (WiFi.status() != WL_CONNECTED)
   {
      delay(500);
      Serial.print(".");
   }

   Serial.println("");
   Serial.print("Connected to ");
   Serial.println(ssid);
   Serial.print("IP address: ");
   Serial.println(WiFi.localIP());

   server.on("/", []() {
      server.send(200, "text/html", WebPage);
   });

   server.begin();

   webSocket.begin();
   webSocket.onEvent(webSocketEvent);
}

void loop()
{     
   String ecgData = String(analogRead(EcgPin));
   webSocket.loop();
   server.handleClient();   
   Serial.println(ecgData);
   webSocket.broadcastTXT(ecgData);
   delay(50);
   //  if (Serial.available() > 0){
   //    char c[] = {(char)Serial.read()};
   //    webSocket.broadcastTXT(c, sizeof(c));
   //  }
}