/*global WebSocket, JSON, $, window, console, alert*/
"use strict";
/**
 * Function calls across the background TCP socket. Uses JSON RPC + a queue.
 * (I've added this extra logic to simplify expanding this)
 */
var tweet_id;
var dataset;
tweet_id = 0;
dataset = 'none';

var client = {
    queue: {},
    // Connects to Python through the websocket
    connect: function (port) {
        var self = this;
        this.socket = new WebSocket("wss://" + window.location.hostname + ":" + port + "/websocket");

        this.socket.onopen = function () {
            console.log("Connected!");
        };

        this.socket.onmessage = function (messageEvent) {
            var router, current, updated, jsonRpc;

            jsonRpc = JSON.parse(messageEvent.data);
            router = self.queue[jsonRpc.id];
            delete self.queue[jsonRpc.id];
            self.result = jsonRpc.result;

            // If there's an error, display it in an alert window
            if (jsonRpc.error) {
                alert(jsonRpc.result);

            // If the response is from "count", do stuff
            } else if (router === "count") {
                document.getElementById("tweet").textContent = jsonRpc.text;
                document.getElementById("tweet_img").src = jsonRpc.img_url;
                tweet_id = jsonRpc.tweet_id
                dataset = jsonRpc.dataset

            // If the response is from anything else, it's currently unsupported
            } else {
                alert("Unsupported function: " + router);
            }
        };
    },

    // Generates a unique identifier for request ids
    // Code from http://stackoverflow.com/questions/105034/
    // how-to-create-a-guid-uuid-in-javascript/2117523#2117523
    uuid: function () {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    },

    // Placeholder function. It adds one to things.
    count: function (data) {
        var uuid = this.uuid();
        this.socket.send(JSON.stringify({method: "count", id: uuid, params: {tweet_id: window.tweet_id, label: data, dataset: window.dataset, annotator_info: 'ip'}}));
        this.queue[uuid] = "count";
    }
};

